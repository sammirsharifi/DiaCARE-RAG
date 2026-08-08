from explainable_graphrag.kg.graph_manager import GraphManager
from explainable_graphrag.kg.node_mapper import NodeMapper

from explainable_graphrag.retrieval.subgraph_retriever import (
    SubgraphRetriever,
)

from explainable_graphrag.retrieval.evidence_builder import (
    EvidenceBuilder,
)

from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)


def test_evidence_builder():


    ##############################################################

    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()


    mapper = NodeMapper(
        graph
    )


    retriever = SubgraphRetriever(
        graph
    )


    builder = EvidenceBuilder(
        mapper
    )


    ##############################################################

    query_nodes = [

        "73211009",

        "44054006",

        "230690007",

    ]


    ##############################################################

    evidence_graph = retriever.retrieve(
        query_nodes
    )


    ##############################################################

    evidence_text = builder.build(
        evidence_graph
    )


    ##############################################################

    logger.info("=" * 80)
    logger.info("GENERATED EVIDENCE")
    logger.info("=" * 80)


    logger.info(
        evidence_text
    )


    logger.info("=" * 80)


    ##############################################################

    assert len(evidence_text) > 0