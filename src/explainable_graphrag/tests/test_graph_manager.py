from explainable_graphrag.kg.graph_manager import GraphManager
from explainable_graphrag.utils.logger import get_logger

logger = get_logger(__name__)


def test_graph_loading():

    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()

    logger.info("=" * 60)
    logger.info("GRAPH INFORMATION")
    logger.info("=" * 60)

    logger.info(
        f"Number of Nodes : {graph.number_of_nodes()}"
    )

    logger.info(
        f"Number of Edges : {graph.number_of_edges()}"
    )

    logger.info(
        f"Graph Type      : {type(graph).__name__}"
    )

    logger.info("=" * 60)

    assert graph is not None
    assert graph.number_of_nodes() > 0
    assert graph.number_of_edges() > 0


def test_relation_structure():

    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()

    logger.info("")
    logger.info("=" * 60)
    logger.info("RELATION STRUCTURE ANALYSIS")
    logger.info("=" * 60)

    relation_examples = {}

    for source, target, data in graph.edges(data=True):

        relation = data.get(
            "relation",
            "UNKNOWN",
        )

        if relation not in relation_examples:

            relation_examples[relation] = {

                "source": source,

                "target": target,

                "attributes": dict(data),

            }

    logger.info(
        f"Number of Relation Types : {len(relation_examples)}"
    )

    logger.info("")

    for relation in sorted(relation_examples):

        example = relation_examples[relation]

        logger.info("-" * 50)

        logger.info(
            f"Relation : {relation}"
        )

        logger.info(
            f"Example  : {example['source']} --> {example['target']}"
        )

        logger.info("Attributes:")

        for key, value in example["attributes"].items():

            logger.info(
                f"    {key} : {value}"
            )

    logger.info("=" * 60)

    assert len(relation_examples) > 0