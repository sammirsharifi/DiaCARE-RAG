from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)


class MedicalRouter:
    """
    Decide whether a question requires
    medical graph retrieval.
    
    Uses the same LLM as the chat system.
    """


    def __init__(
        self,
        llm,
    ):

        self.llm = llm



    def is_medical(
        self,
        question: str,
    ) -> bool:


        prompt = f"""
You are a medical query classifier.

Classify the following user question.

Return ONLY one word:

MEDICAL
or
GENERAL


Question:
{question}
"""


        result = self.llm.generate(
            prompt
        )


        result = result.strip().upper()


        logger.info(
            "Router decision: %s",
            result
        )


        return (
            "MEDICAL" in result
        )