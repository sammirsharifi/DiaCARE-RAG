from explainable_graphrag.utils.logger import get_logger

logger = get_logger(__name__)


class NodeMapper:
    """
    Utility class for mapping ontology node IDs and human-readable labels.

    Responsibilities
    ----------------
    - Node ID -> Label
    - Label -> Node ID
    - Node ID -> Node attributes
    """

    def __init__(self, graph):
        """
        Parameters
        ----------
        graph : networkx.MultiDiGraph
            Ontology graph.
        """

        logger.info("Initializing NodeMapper...")

        self.graph = graph

        # Node ID -> Human Label
        self.id_to_label_map = {}

        # Human Label -> Node ID
        self.label_to_id_map = {}

        # Node ID -> Complete node attributes
        self.node_info_map = {}

        for node, data in graph.nodes(data=True):

            label = str(
                data.get("label", node)
            ).strip()

            self.id_to_label_map[node] = label

            self.label_to_id_map[label.lower()] = node

            self.node_info_map[node] = data

        logger.info(
            f"NodeMapper initialized with "
            f"{len(self.id_to_label_map)} nodes."
        )

    ##################################################################

    def id_to_label(self, node_id: str) -> str:
        """
        Convert a node ID into its human-readable label.

        Parameters
        ----------
        node_id : str

        Returns
        -------
        str
        """

        return self.id_to_label_map.get(
            node_id,
            node_id,
        )

    ##################################################################

    def label_to_id(self, label: str):
        """
        Convert a label into its ontology node ID.

        Parameters
        ----------
        label : str

        Returns
        -------
        str | None
        """

        return self.label_to_id_map.get(
            label.lower()
        )

    ##################################################################

    def get_node(self, node_id: str):
        """
        Return all attributes associated with a node.

        Parameters
        ----------
        node_id : str

        Returns
        -------
        dict
        """

        return self.node_info_map.get(
            node_id,
            {}
        )

    ##################################################################

    def search(self, keyword: str):
        """
        Search ontology labels using a keyword.

        Parameters
        ----------
        keyword : str

        Returns
        -------
        list[tuple]
            (node_id, label)
        """

        keyword = keyword.lower()

        results = []

        for node, label in self.id_to_label_map.items():

            if keyword in label.lower():

                results.append(
                    (
                        node,
                        label,
                    )
                )

        logger.info(
            f"Search '{keyword}' -> "
            f"{len(results)} result(s)."
        )

        return results