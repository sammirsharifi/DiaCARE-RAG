from explainable_graphrag.retrieval.entity_extractor import EntityExtractor

from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)


def test_entity_extractor():

    logger.info("=" * 70)
    logger.info("EntityExtractor Test Started")
    logger.info("=" * 70)

    extractor = EntityExtractor()

    query = (
       " What are the main risk factors for type 2 diabetes?"
    )

    entities = extractor.extract(query)

    logger.info("Query")
    logger.info(query)

    logger.info("Extracted Entities")

    for entity in entities:

        logger.info(entity)

    assert isinstance(
        entities,
        list,
    )

    assert len(
        entities
    ) > 0

    logger.info("=" * 70)
    logger.info("EntityExtractor Test Passed")
    logger.info("=" * 70)