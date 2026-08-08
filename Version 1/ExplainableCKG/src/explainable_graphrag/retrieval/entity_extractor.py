from typing import List

from transformers import pipeline

from explainable_graphrag.utils.logger import get_logger
from explainable_graphrag.utils.timer import Timer


logger = get_logger(__name__)


class EntityExtractor:
    """
    Medical Named Entity Recognition (NER).

    This class extracts biomedical entities from a user query.
    The extracted entities will later be linked to ontology nodes
    using SapBERT.
    """

    def __init__(
        self,
        model_name: str = "d4data/biomedical-ner-all",
    ):
        """
        Parameters
        ----------
        model_name : str
            HuggingFace NER model.
        """

        logger.info("Loading Biomedical NER model...")

        with Timer(logger, "Load Biomedical NER"):

            self.pipeline = pipeline(
                task="token-classification",
                model=model_name,
                aggregation_strategy="simple",
            )

        logger.info("Biomedical NER loaded successfully.")

    ##################################################################

    def extract(
        self,
        query: str,
    ) -> List[str]:
        """
        Extract biomedical entities from a query.

        Parameters
        ----------
        query : str

        Returns
        -------
        List[str]
        """

        logger.info(
            f"Extracting entities from query: {query}"
        )

        predictions = self.pipeline(query)

        entities = []
        seen = set()

        for prediction in predictions:

            entity = prediction["word"].strip()

            if not entity:
                continue

            key = entity.lower()

            if key in seen:
                continue

            seen.add(key)

            entities.append(entity)

        logger.info(
            f"{len(entities)} entity(s) extracted."
        )

        return entities