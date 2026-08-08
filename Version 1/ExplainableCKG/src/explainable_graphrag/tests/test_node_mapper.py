from explainable_graphrag.kg.graph_manager import GraphManager
from explainable_graphrag.kg.node_mapper import NodeMapper

from explainable_graphrag.utils.logger import get_logger

logger = get_logger(__name__)


def test_node_mapper():

    logger.info("=" * 70)
    logger.info("NodeMapper Test Started")
    logger.info("=" * 70)

    # ----------------------------------------------------------
    # Load Graph
    # ----------------------------------------------------------

    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()

    # ----------------------------------------------------------
    # Initialize Mapper
    # ----------------------------------------------------------

    mapper = NodeMapper(graph)

    # ----------------------------------------------------------
    # Basic Graph Information
    # ----------------------------------------------------------

    logger.info(
        f"Graph Nodes : {graph.number_of_nodes()}"
    )

    logger.info(
        f"Graph Edges : {graph.number_of_edges()}"
    )

    logger.info(
        f"Mapped Nodes : {len(mapper.id_to_label_map)}"
    )

    # ----------------------------------------------------------
    # Test ID -> Label
    # ----------------------------------------------------------

    node_id = "73211009"

    label = mapper.id_to_label(
        node_id
    )

    logger.info(
        f"id_to_label('{node_id}') -> {label}"
    )

    assert label is not None

    # ----------------------------------------------------------
    # Test Label -> ID
    # ----------------------------------------------------------

    recovered_id = mapper.label_to_id(
        label
    )

    logger.info(
        f"label_to_id('{label}') -> {recovered_id}"
    )

    assert recovered_id == node_id

    # ----------------------------------------------------------
    # Test Node Attributes
    # ----------------------------------------------------------

    node_info = mapper.get_node(
        node_id
    )

    logger.info(
        "Node Attributes:"
    )

    for key, value in node_info.items():

        logger.info(
            f"    {key} : {value}"
        )

    assert isinstance(
        node_info,
        dict
    )

    # ----------------------------------------------------------
    # Test Search
    # ----------------------------------------------------------

    keyword = "diabetes"

    results = mapper.search(
        keyword
    )

    logger.info(
        f"Search('{keyword}') -> {len(results)} result(s)"
    )

    for node, label in results[:10]:

        logger.info(
            f"{node} -> {label}"
        )

    assert isinstance(
        results,
        list
    )

    logger.info("=" * 70)
    logger.info("NodeMapper Test Passed")
    logger.info("=" * 70)