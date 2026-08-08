from explainable_graphrag.pipeline.result import PipelineResult

from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)


class MedicalService:
    """
    Executes medical GraphRAG pipeline.

    Flow:
    Question
        |
        Entity Linking
        |
        Graph Retrieval
        |
        Evidence Building
        |
        Prompt Construction
        |
        LLM Generation
    """

    def __init__(
        self,
        container,
    ):

        self.container = container



    def answer(
        self,
        question: str,
    ) -> PipelineResult:


        logger.info(
            "Starting medical pipeline"
        )


        ##################################################
        # Entity Linking
        ##################################################

        node_ids = (
            self.container.linker.link(
                question
            )
        )


        logger.info(
            "Linked nodes: %d",
            len(node_ids)
        )



        ##################################################
        # Retrieve Evidence Graph
        ##################################################

        evidence_graph = (
            self.container.retriever.retrieve(
                node_ids
            )
        )


        logger.info(
            "Evidence graph nodes: %d",
            evidence_graph.number_of_nodes()
        )


        logger.info(
            "Evidence graph edges: %d",
            evidence_graph.number_of_edges()
        )



        ##################################################
        # Build Evidence Text
        ##################################################

        evidence = (
            self.container.evidence_builder.build(
                evidence_graph
            )
        )



        ##################################################
        # Build Prompt
        ##################################################

        prompt = (
            self.container.prompt_builder.build(
                question,
                evidence
            )
        )



        ##################################################
        # Generate Answer
        ##################################################

        answer = (
            self.container.llm.generate(
                prompt
            )
        )



        ##################################################
        # Prepare UI Response
        ##################################################

        metadata = {

            "retrieved_nodes":
                list(
                    evidence_graph.nodes()
                ),

            "number_of_nodes":
                evidence_graph.number_of_nodes(),

            "number_of_edges":
                evidence_graph.number_of_edges()

        }



        return PipelineResult(

            answer=answer,

            route="MEDICAL",

            evidence=evidence,

            metadata=metadata

        )