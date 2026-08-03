from pathlib import Path
import pickle

from explainable_graphrag.kg.load_graph import DiabetesGraph
from explainable_graphrag.kg.build_graph import OntologyGraphBuilder

from explainable_graphrag.utils.logger import get_logger
from explainable_graphrag.utils.timer import Timer


logger = get_logger(__name__)


class GraphManager:
    """
    Manage loading and caching of the ontology graph.

    Workflow
    --------
    1. Check whether a cached graph already exists.
    2. If it exists, load it from disk.
    3. Otherwise:
        - Load the OWL ontology.
        - Build the NetworkX graph.
        - Save the graph into cache.
    4. Return the graph.
    """

    def __init__(
        self,
        owl_path: str,
        cache_dir: str = "cache",
    ):
        """
        Parameters
        ----------
        owl_path : str
            Path to the ontology (.owl) file.

        cache_dir : str
            Directory used to store graph cache.
        """

        self.owl_path = owl_path

        cache_dir = Path(cache_dir)
        cache_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.cache_file = (
            cache_dir /
            "ontology_graph.pkl"
        )

    ####################################################################

    def load(self):
        """
        Load the ontology graph.

        Returns
        -------
        networkx.MultiDiGraph
            The constructed ontology graph.
        """

        # --------------------------------------------------------------
        # Load graph from cache.
        # --------------------------------------------------------------

        if self.cache_file.exists():

            logger.info(
                "Loading graph from cache..."
            )

            with Timer(
                logger,
                "Load Graph Cache",
            ):

                with open(
                    self.cache_file,
                    "rb",
                ) as f:

                    graph = pickle.load(f)

            logger.info(
                "Graph loaded successfully."
            )

            logger.info(
                f"Graph type: {type(graph)}"
            )

            logger.info(
                f"Is MultiGraph: {graph.is_multigraph()}"
            )

            return graph

        # --------------------------------------------------------------
        # Build graph from ontology.
        # --------------------------------------------------------------

        logger.info(
            "Cache not found. Building graph from ontology..."
        )

        with Timer(
            logger,
            "Build Graph",
        ):

            kg = DiabetesGraph(
                self.owl_path
            )

            builder = OntologyGraphBuilder(
                kg.onto
            )

            graph = builder.build()

        # --------------------------------------------------------------
        # Save graph for future runs.
        # --------------------------------------------------------------

        logger.info(
            "Saving graph cache..."
        )

        with open(
            self.cache_file,
            "wb",
        ) as f:

            pickle.dump(
                graph,
                f,
            )

        logger.info(
            f"Graph cached successfully: {self.cache_file}"
        )

        return graph