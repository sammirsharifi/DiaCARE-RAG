from __future__ import annotations

import networkx as nx

from networkx.algorithms.approximation import steiner_tree

from explainable_graphrag.utils.logger import get_logger
from explainable_graphrag.utils.timer import Timer


logger = get_logger(__name__)


class SubgraphRetriever:
    """
    Build an approximate evidence subgraph connecting
    ontology entities using Steiner Tree.
    """


    def __init__(
        self,
        graph: nx.MultiDiGraph,
    ):
        """
        Initialize subgraph retriever.

        Parameters
        ----------
        graph:
            Ontology knowledge graph.
        """

        self.graph = graph


    ##############################################################

    def retrieve(
        self,
        node_ids: list[str],
    ) -> nx.MultiDiGraph:
        """
        Retrieve evidence subgraph connecting query entities.

        Parameters
        ----------
        node_ids:
            Ontology node identifiers.

        Returns
        -------
        nx.MultiDiGraph
            Evidence subgraph.
        """


        logger.info(
            "Starting evidence subgraph retrieval..."
        )


        ##########################################################
        # Validate nodes
        ##########################################################

        valid_nodes = [

            node

            for node in node_ids

            if node in self.graph

        ]


        logger.info(
            f"Requested Nodes : {len(node_ids)}"
        )

        logger.info(
            f"Valid Nodes     : {len(valid_nodes)}"
        )


        if len(valid_nodes) < 2:

            raise ValueError(
                "At least two valid ontology nodes are required."
            )


        ##########################################################
        # Prepare graph for Steiner
        ##########################################################

        logger.info(
            "Preparing graph for Steiner Tree..."
        )


        undirected = nx.Graph(
            self.graph.to_undirected()
        )


        ##########################################################
        # Find connected component
        ##########################################################

        logger.info(
            "Finding query connected component..."
        )


        with Timer(
            logger,
            "Connected Component Search",
        ):


            query_component = None


            for component in nx.connected_components(
                undirected
            ):

                if all(
                    node in component
                    for node in valid_nodes
                ):

                    query_component = component

                    break



        if query_component is None:

            raise ValueError(
                "Query nodes are not in the same connected component."
            )


        logger.info(
            f"Component Nodes : {len(query_component)}"
        )


        undirected = undirected.subgraph(
            query_component
        ).copy()



        ##########################################################
        # Steiner Tree
        ##########################################################

        logger.info(
            "Building approximate Steiner tree..."
        )


        with Timer(
            logger,
            "Steiner Tree",
        ):

            tree = steiner_tree(
                undirected,
                valid_nodes,
            )



        ##########################################################
        # Recover directed evidence graph
        ##########################################################

        logger.info(
            "Recovering directed evidence graph..."
        )


        evidence = nx.MultiDiGraph()



        ##########################################################
        # Add nodes
        ##########################################################

        for node in tree.nodes():

            evidence.add_node(

                node,

                **self.graph.nodes[node],

            )



        ##########################################################
        # Add edges
        ##########################################################

        for u, v in tree.edges():


            ######################################################
            # Original direction
            ######################################################

            if self.graph.has_edge(u, v):


                for _, edge_data in self.graph[u][v].items():


                    if isinstance(edge_data, dict):

                        evidence.add_edge(

                            u,

                            v,

                            **edge_data,

                        )


                    else:

                        evidence.add_edge(

                            u,

                            v,

                            relation=edge_data,

                        )



            ######################################################
            # Reverse direction
            ######################################################

            elif self.graph.has_edge(v, u):


                for _, edge_data in self.graph[v][u].items():


                    if isinstance(edge_data, dict):

                        evidence.add_edge(

                            v,

                            u,

                            **edge_data,

                        )


                    else:

                        evidence.add_edge(

                            v,

                            u,

                            relation=edge_data,

                        )



        ##########################################################

        logger.info(
            f"Evidence Nodes : {evidence.number_of_nodes()}"
        )


        logger.info(
            f"Evidence Edges : {evidence.number_of_edges()}"
        )


        return evidence