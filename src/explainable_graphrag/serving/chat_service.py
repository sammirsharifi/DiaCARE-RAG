from explainable_graphrag.serving.medical_service import MedicalService
from explainable_graphrag.pipeline.result import PipelineResult

from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)


class ChatService:
    """
    Main entry point for user conversations.

    Responsibilities:
    1. Receive user question.
    2. Decide routing using MedicalRouter.
    3. Send medical questions to GraphRAG pipeline.
    4. Send general questions directly to LLM.
    """


    def __init__(
        self,
        container,
    ):

        self.container = container

        self.medical_service = MedicalService(
            container
        )



    def ask(
        self,
        question: str,
    ) -> PipelineResult:


        logger.info(
            "New question received"
        )


        ##################################################
        # Route decision using LLM Router
        ##################################################

        is_medical = (
            self.container.router.is_medical(
                question
            )
        )


        ##################################################
        # Medical GraphRAG path
        ##################################################

        if is_medical:

            logger.info(
                "Medical pipeline selected"
            )


            result = (
                self.medical_service.answer(
                    question
                )
            )


            return result



        ##################################################
        # General LLM path
        ##################################################

        logger.info(
            "General LLM selected"
        )


        answer = (
            self.container.llm.generate(
                question
            )
        )


        return PipelineResult(

            answer=answer,

            route="GENERAL",

            evidence=None,

            metadata={

                "router":
                "LLM"

            }

        )