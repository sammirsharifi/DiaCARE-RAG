from explainable_graphrag.kg.graph_manager import GraphManager
from explainable_graphrag.kg.node_mapper import NodeMapper

from explainable_graphrag.retrieval.subgraph_retriever import (
    SubgraphRetriever,
)

from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)


def test_subgraph_retrieval():

    ##############################################################
    # Load graph
    ##############################################################

    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()


    mapper = NodeMapper(graph)


    retriever = SubgraphRetriever(graph)


    ##############################################################
    # Query entities
    ##############################################################

    query_nodes = [

        "44054006",

        "C_Type2Diabetes",

        "DiabetesPedigreeFunction",

        "DiabeticPatient",

        "DiabeticGlucose"

    ]


    ##############################################################
    # Show input entities
    ##############################################################

    logger.info("=" * 80)
    logger.info("QUERY ENTITIES")
    logger.info("=" * 80)


    for node in query_nodes:

        logger.info(
            f"{node} --> {mapper.id_to_label(node)}"
        )


    ##############################################################
    # Retrieve evidence
    ##############################################################

    evidence = retriever.retrieve(
        query_nodes
    )


    ##############################################################
    # Evidence information
    ##############################################################

    logger.info("")
    logger.info("=" * 80)
    logger.info("EVIDENCE SUBGRAPH")
    logger.info("=" * 80)


    logger.info(
        f"Evidence Nodes : {evidence.number_of_nodes()}"
    )

    logger.info(
        f"Evidence Edges : {evidence.number_of_edges()}"
    )


    ##############################################################
    # Evidence nodes
    ##############################################################

    logger.info("")
    logger.info("-" * 80)
    logger.info("EVIDENCE NODES")
    logger.info("-" * 80)


    for node, data in evidence.nodes(data=True):

        label = mapper.id_to_label(node)


        logger.info(
            f"""
Node ID   : {node}
Label     : {label}
Metadata  : {data}
"""
        )


    ##############################################################
    # Evidence relations
    ##############################################################

    logger.info("")
    logger.info("-" * 80)
    logger.info("EVIDENCE RELATIONS")
    logger.info("-" * 80)


    for u, v, data in evidence.edges(data=True):

        source = mapper.id_to_label(u)

        target = mapper.id_to_label(v)


        relation = data.get(
            "relation",
            "UNKNOWN"
        )


        logger.info(
            f"{source}  --[{relation}]-->  {target}"
        )


    ##############################################################
    # Assertions
    ##############################################################

    assert evidence.number_of_nodes() > 0

    assert evidence.number_of_edges() > 0


    logger.info("=" * 80)
    logger.info("SUBGRAPH RETRIEVAL TEST PASSED")
    logger.info("=" * 80)