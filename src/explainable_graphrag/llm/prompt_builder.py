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

Answer the question using the provided knowledge graph evidence as the primary source of information.

Generate a comprehensive, coherent, and well-integrated answer.
Do not simply list or summarize individual evidence pieces separately.
Instead, combine the relevant knowledge graph evidence with your general language understanding to create a single, natural, and complete explanation.

The final answer should:
- Be written as one connected explanation rather than fragmented sections.
- Integrate relationships between different concepts found in the evidence.
- Explain the medical mechanisms, associations, and connections clearly.
- Provide enough details for the reader to fully understand the topic.
- Avoid repeating the same information from different evidence sources.

Use the knowledge graph evidence whenever relevant.
Do not ignore available evidence or answer only from your internal knowledge.

At the end of the answer, provide a brief transparency note indicating the approximate contribution used for generating the response:

Evidence utilization assessment:
- Supported by knowledge graph evidence: High/Medium/Low
- Additional general medical reasoning used: High/Medium/Low

The contribution percentages are only an approximate estimation of how much each source influenced the generated answer.

If the provided knowledge graph evidence is insufficient to answer the question, clearly state:
"The provided knowledge graph evidence is insufficient to answer this question."

Knowledge Graph Evidence:

{evidence}


Question:

{question}


Answer:
"""


        logger.info(
            "Prompt created successfully."
        )


        return prompt