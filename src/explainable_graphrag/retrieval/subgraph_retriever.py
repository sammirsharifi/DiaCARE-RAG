from __future__ import annotations

import networkx as nx

from networkx.algorithms.approximation import steiner_tree

from explainable_graphrag.utils.logger import get_logger
from explainable_graphrag.utils.timer import Timer


logger = get_logger(__name__)


class SubgraphRetriever:
    """
    Retrieve evidence subgraph from ontology graph.

    Supports disconnected query entities by
    processing each connected component separately.
    """


    def __init__(
        self,
        graph: nx.MultiDiGraph,
    ):

        self.graph = graph



    ##############################################################

    def retrieve(
        self,
        node_ids: list[str],
    ) -> nx.MultiDiGraph:
        """
        Retrieve evidence graph.

        Parameters
        ----------
        node_ids:
            Linked ontology node ids.

        Returns
        -------
        nx.MultiDiGraph
            Evidence subgraph.
        """


        logger.info(
            "=" * 60
        )

        logger.info(
            "START SUBGRAPH RETRIEVAL"
        )


        ##################################################
        # Validate nodes
        ##################################################

        valid_nodes = [

            node

            for node in node_ids

            if node in self.graph

        ]


        logger.info(
            "Requested nodes : %d",
            len(node_ids)
        )


        logger.info(
            "Valid nodes     : %d",
            len(valid_nodes)
        )


        evidence = nx.MultiDiGraph()


        if not valid_nodes:

            logger.warning(
                "No valid nodes found."
            )

            return evidence



        ##################################################
        # Convert graph
        ##################################################

        undirected = nx.Graph(
            self.graph.to_undirected()
        )


        ##################################################
        # Find connected components
        ##################################################

        components = list(
            nx.connected_components(
                undirected
            )
        )


        logger.info(
            "Graph components : %d",
            len(components)
        )



        processed = set()



        ##################################################
        # Process every component separately
        ##################################################

        for node in valid_nodes:


            component = None


            for c in components:

                if node in c:

                    component = c
                    break



            if component is None:

                logger.warning(
                    "No component found for node %s",
                    node
                )

                continue



            component_key = id(component)



            if component_key in processed:

                continue



            processed.add(
                component_key
            )



            ##################################################
            # Query nodes inside this component
            ##################################################

            component_query_nodes = [

                n

                for n in valid_nodes

                if n in component

            ]



            logger.info(
                "Processing component"
            )


            logger.info(
                "Component size : %d",
                len(component)
            )


            logger.info(
                "Query nodes    : %d",
                len(component_query_nodes)
            )



            ##################################################
            # Single node case
            ##################################################

            if len(component_query_nodes) == 1:

                node = component_query_nodes[0]

                # Add the node
                evidence.add_node(
                    node,
                    **self.graph.nodes[node]
                )

                # Outgoing edges
                for _, neighbor, key, data in self.graph.out_edges(
                    node,
                    keys=True,
                    data=True,
                ):
                    evidence.add_node(
                        neighbor,
                        **self.graph.nodes[neighbor]
                    )
                    evidence.add_edge(
                        node,
                        neighbor,
                        key=key,
                        **data,
                    )

                # Incoming edges
                for neighbor, _, key, data in self.graph.in_edges(
                    node,
                    keys=True,
                    data=True,
                ):
                    evidence.add_node(
                        neighbor,
                        **self.graph.nodes[neighbor]
                    )
                    evidence.add_edge(
                        neighbor,
                        node,
                        key=key,
                        **data,
                    )

                logger.info(
                    "Single node with neighborhood added : %s",
                    node
                )

                continue




            ##################################################
            # Steiner tree
            ##################################################

            logger.info(
                "Building Steiner Tree..."
            )


            component_graph = (
                undirected
                .subgraph(component)
                .copy()
            )



            try:

                with Timer(
                    logger,
                    "Steiner Tree"
                ):

                    tree = steiner_tree(

                        component_graph,

                        component_query_nodes

                    )



            except Exception as e:


                logger.warning(
                    "Steiner failed: %s",
                    e
                )


                continue




            ##################################################
            # Add nodes
            ##################################################

            for node in tree.nodes():


                evidence.add_node(

                    node,

                    **self.graph.nodes[node]

                )



            ##################################################
            # Add edges
            ##################################################

            for u, v in tree.edges():



                # original direction

                if self.graph.has_edge(
                    u,
                    v
                ):


                    for _, data in self.graph[u][v].items():


                        evidence.add_edge(

                            u,

                            v,

                            **data

                        )




                # reverse direction

                elif self.graph.has_edge(
                    v,
                    u
                ):


                    for _, data in self.graph[v][u].items():


                        evidence.add_edge(

                            v,

                            u,

                            **data

                        )



        ##################################################
        # Final result
        ##################################################

        logger.info(
            "=" * 60
        )


        logger.info(
            "FINAL EVIDENCE GRAPH"
        )


        logger.info(
            "Nodes : %d",
            evidence.number_of_nodes()
        )


        logger.info(
            "Edges : %d",
            evidence.number_of_edges()
        )


        logger.info(
            "=" * 60
        )



        return evidence