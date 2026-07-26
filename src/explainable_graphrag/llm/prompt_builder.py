from __future__ import annotations

from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)


class PromptBuilder:
    """
    Build prompts for the language model
    using user questions and retrieved medical evidence.
    """


    def __init__(self):
        """
        Initialize PromptBuilder.
        """

        logger.info(
            "Initializing PromptBuilder..."
        )


    ##############################################################

    def build(
        self,
        question: str,
        evidence: str,
    ) -> str:
        """
        Create an instruction prompt.

        Parameters
        ----------
        question:
            User medical question.

        evidence:
            Evidence extracted from knowledge graph.

        Returns
        -------
        str
            Generated LLM prompt.
        """


        logger.info(
            "Building LLM prompt..."
        )


        prompt = f"""
You are a medical assistant specialized in diabetes.

Answer the question using only the provided knowledge graph evidence.

If the evidence is insufficient, clearly state that the information is not available.

Evidence:

{evidence}


Question:

{question}


Answer:
"""


        logger.info(
            "Prompt created successfully."
        )


        return prompt