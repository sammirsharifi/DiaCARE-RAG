from explainable_graphrag.kg.graph_manager import GraphManager
from explainable_graphrag.kg.node_mapper import NodeMapper

from explainable_graphrag.retrieval.sapbert_linker import SapBERTLinker
from explainable_graphrag.retrieval.subgraph_retriever import SubgraphRetriever
from explainable_graphrag.retrieval.evidence_builder import EvidenceBuilder
from explainable_graphrag.retrieval.entity_extractor import EntityExtractor
from explainable_graphrag.llm.model import SmallLLM
from explainable_graphrag.llm.prompt_builder import PromptBuilder

from explainable_graphrag.utils.logger import get_logger

from explainable_graphrag.serving.medical_router import MedicalRouter


logger = get_logger(__name__)


class ServiceContainer:
    """
    Holds all long-lived resources.

    Everything is loaded once when backend starts.
    """

    def __init__(
        self,
        owl_path: str,
    ):

        logger.info(
            "Initializing Service Container"
        )


        # ----------------------------
        # Knowledge Graph
        # ----------------------------

        self.graph = GraphManager(
            owl_path
        ).load()



        # ----------------------------
        # Node Mapper
        # ----------------------------

        self.mapper = NodeMapper(
            self.graph
        )

        # ----------------------------
        # Entity Extraction
        # ----------------------------

        self.extractor = EntityExtractor()

        # ----------------------------
        # Entity Linking
        # ----------------------------

        self.linker = SapBERTLinker(
            self.graph
        )



        # ----------------------------
        # Graph Retrieval
        # ----------------------------

        self.retriever = SubgraphRetriever(
            self.graph
        )


        self.evidence_builder = EvidenceBuilder(
            self.mapper
        )



        # ----------------------------
        # LLM
        # ----------------------------

        logger.info(
            "Initializing LLM"
        )

        self.llm = SmallLLM()

        # IMPORTANT:
        # Load model once when backend starts
        self.llm.load()


        self.prompt_builder = PromptBuilder()


        """
        # ----------------------------
        # Medical Router
        # ----------------------------
        
        self.router = MedicalRouter(
            self.llm
        )
        """


        logger.info(
            "Service Container Ready"
        )



    ############################################################
    # Main Chat Interface
    ############################################################

    def ask(
        self,
        question: str,
    ):

        logger.info(
            "Received question: %s",
            question
        )

        """
        # ---------------------------------
        # Decide medical / non-medical
        # ---------------------------------

        medical = self.router.is_medical(
            question
        )


        logger.info(
            "Medical question: %s",
            medical
        )

        

        

        # ---------------------------------
        # Normal Chat
        # ---------------------------------

        if not medical:

            answer = self.llm.generate(
                question
            )


            return {
                "answer": answer,
                "medical": False,
                "evidence": None,
            }

        
        """
        # ---------------------------------
        # Medical Pipeline
        # ---------------------------------


        # ---------------------------------
        # Entity Extraction
        # ---------------------------------

        mentions = self.extractor.extract(
            question
        )


        logger.info(
            "Extracted mentions: %s",
            mentions
        )



        # ---------------------------------
        # Entity Linking
        # ---------------------------------

        linked_entities = []


        for mention in mentions:

            result = self.linker.link(
                mention
            )


            matches = result.get(
                "matches",
                []
            )


            for match in matches:

                linked_entities.append(
                    {
                        "mention": mention,
                        "node": match["node"],
                        "label": match["label"],
                        "score": match["score"],
                    }
                )



        logger.info(
            "Linked entities: %s",
            linked_entities
        )



        linked_nodes = [

            entity["node"]

            for entity in linked_entities

        ]



        # Graph Retrieval

        evidence_graph = self.retriever.retrieve(
            linked_nodes
        )



        # Build textual evidence

        evidence = self.evidence_builder.build(
            evidence_graph
        )



        # Build final prompt

        prompt = self.prompt_builder.build(
            question,
            evidence
        )



        # Generate answer

        answer = self.llm.generate(
            prompt
        )



        return {

            "answer": answer,

            "medical": True,

            "evidence": evidence,

            "nodes": list(
                evidence_graph.nodes()
            ),

            "edges": list(
                evidence_graph.edges()
            )

        }