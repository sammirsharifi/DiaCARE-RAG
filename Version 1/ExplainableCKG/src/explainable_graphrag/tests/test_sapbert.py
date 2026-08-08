from explainable_graphrag.kg.graph_manager import GraphManager
from explainable_graphrag.retrieval.sapbert_linker import SapBERTLinker
from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)


def test_sapbert_initialization():

    # -----------------------------
    # Load Knowledge Graph
    # -----------------------------
    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()


    logger.info(
        "========== SAPBERT INFORMATION =========="
    )


    # -----------------------------
    # Initialize SapBERT
    # -----------------------------
    linker = SapBERTLinker(
        graph
    )


    logger.info(
        f"Device : {linker.device}"
    )

    logger.info(
        f"Ontology Labels : {len(linker.labels)}"
    )

    logger.info(
        f"Embedding Shape : {linker.embeddings.shape}"
    )


    logger.info(
        "=========================================="
    )


    # -----------------------------
    # Assertions
    # -----------------------------

    assert linker is not None

    assert len(linker.labels) > 0

    assert linker.embeddings is not None

    assert len(linker.embeddings) == len(
        linker.labels
    )



def test_sapbert_entity_linking():


    # Load graph

    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()


    # Initialize linker

    linker = SapBERTLinker(
        graph
    )


    # Example medical mention

    mention = "type 2 diabetes"


    result = linker.link(
        mention,
        top_k=5,
        threshold=0.5
    )


    logger.info(
        "========== ENTITY LINKING RESULT =========="
    )

    logger.info(
        f"Mention : {result['mention']}"
    )


    for match in result["matches"]:

        logger.info(
            f"""
            Node  : {match['node']}
            Label : {match['label']}
            Score : {match['score']}
            """
        )


    logger.info(
        "============================================"
    )


    # Assertions

    assert result is not None

    assert "matches" in result

    assert isinstance(
        result["matches"],
        list
    )



def test_sapbert_batch_linking():


    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()


    linker = SapBERTLinker(
        graph
    )


    mentions = [

        "diabetes",

        "high blood glucose",

        "insulin resistance"

    ]


    results = linker.batch_link(
        mentions,
        top_k=3,
        threshold=0.5
    )


    logger.info(
        "========== BATCH LINKING =========="
    )


    for item in results:

        logger.info(
            f"{item['mention']}"
        )

        for match in item["matches"]:

            logger.info(
                f" --> {match['label']} ({match['score']})"
            )


    logger.info(
        "===================================="
    )


    assert len(results) == len(mentions)