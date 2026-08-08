from __future__ import annotations

import networkx as nx

from networkx.algorithms.approximation import steiner_tree

from explainable_graphrag.utils.logger import get_logger
from explainable_graphrag.utils.timer import Timer


logger = get_logger(__name__)


class SubgraphRetriever:
    """
    Retrieve evidence subgraph from ontology graph.

    Strategy:

    1. Split query nodes by connected components.
    2. Multiple query nodes in component:
        -> Steiner Tree retrieval.
    3. Single query node:
        -> Return node + all connected triples.
    """

    def __init__(
        self,
        graph: nx.MultiDiGraph,
    ):
        self.graph = graph


    ##############################################################
    # Add node with all connected triples
    ##############################################################

    def _add_node_with_neighbors(
        self,
        evidence: nx.MultiDiGraph,
        node: str,
    ):
        """
        Add node and all connected relations.

        Example:

        A -- relation --> B

        Adds:

        (A, relation, B)

        """

        ##################################################
        # Add center node
        ##################################################

        evidence.add_node(
            node,
            **self.graph.nodes[node]
        )


        ##################################################
        # Outgoing triples
        ##################################################

        for source, target, key, data in self.graph.out_edges(
            node,
            keys=True,
            data=True,
        ):
            logger.info(source , target , key ,data)

            evidence.add_node(
                target,
                **self.graph.nodes[target]
            )


            evidence.add_edge(
                source,
                target,
                key=key,
                **data
            )


        ##################################################
        # Incoming triples
        ##################################################

        for source, target, key, data in self.graph.in_edges(
            node,
            keys=True,
            data=True,
        ):

            evidence.add_node(
                source,
                **self.graph.nodes[source]
            )


            evidence.add_edge(
                source,
                target,
                key=key,
                **data
            )


    ##############################################################
    # Add Steiner tree edges
    ##############################################################

    def _add_tree(
        self,
        evidence: nx.MultiDiGraph,
        tree: nx.Graph,
    ):
        """
        Convert undirected Steiner tree
        back to original KG triples.
        """

        for node in tree.nodes():

            evidence.add_node(
                node,
                **self.graph.nodes[node]
            )


        for u, v in tree.edges():

            ##################################################
            # Original direction
            ##################################################

            if self.graph.has_edge(
                u,
                v
            ):

                for key, data in self.graph[u][v].items():

                    evidence.add_edge(
                        u,
                        v,
                        key=key,
                        **data
                    )


            ##################################################
            # Reverse direction
            ##################################################

            elif self.graph.has_edge(
                v,
                u
            ):

                for key, data in self.graph[v][u].items():

                    evidence.add_edge(
                        v,
                        u,
                        key=key,
                        **data
                    )


    ##############################################################
    # Main retrieval
    ##############################################################

    def retrieve(
        self,
        node_ids: list[str],
    ) -> nx.MultiDiGraph:


        logger.info("=" * 60)
        logger.info("START SUBGRAPH RETRIEVAL")


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
            "Valid nodes : %d",
            len(valid_nodes)
        )


        evidence = nx.MultiDiGraph()


        if not valid_nodes:

            logger.warning(
                "No valid nodes found"
            )

            return evidence



        ##################################################
        # Undirected graph
        ##################################################

        undirected = nx.Graph(
            self.graph.to_undirected()
        )


        ##################################################
        # Connected components
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
        # Process every component
        ##################################################

        for node in valid_nodes:


            component = next(
                (
                    c
                    for c in components
                    if node in c
                ),
                None
            )


            if component is None:

                continue



            component_id = id(component)


            if component_id in processed:

                continue


            processed.add(
                component_id
            )



            ##################################################
            # Query nodes inside component
            ##################################################

            component_queries = [
                n
                for n in valid_nodes
                if n in component
            ]



            logger.info(
                "--------------------------------"
            )

            logger.info(
                "Component size : %d",
                len(component)
            )

            logger.info(
                "Query nodes : %s",
                component_queries
            )



            ##################################################
            # CASE 1:
            # Single node
            ##################################################

            if len(component_queries) == 1:


                self._add_node_with_neighbors(
                    evidence,
                    component_queries[0]
                )


                logger.info(
                    "Neighborhood triples added"
                )


                continue



            ##################################################
            # CASE 2:
            # Multiple nodes
            ##################################################

            component_graph = (
                undirected
                .subgraph(component)
                .copy()
            )


            try:

                logger.info(
                    "Building Steiner Tree"
                )


                with Timer(
                    logger,
                    "Steiner Tree"
                ):

                    tree = steiner_tree(
                        component_graph,
                        component_queries
                    )


                self._add_tree(
                    evidence,
                    tree
                )


                logger.info(
                    "Steiner evidence added"
                )



            ##################################################
            # Fallback
            ##################################################

            except Exception as e:


                logger.warning(
                    "Steiner failed: %s",
                    e
                )


                logger.warning(
                    "Using triple fallback"
                )


                for query_node in component_queries:

                    self._add_node_with_neighbors(
                        evidence,
                        query_node
                    )



        ##################################################
        # Final
        ##################################################

        logger.info("=" * 60)

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


        logger.info("=" * 60)


        return evidence