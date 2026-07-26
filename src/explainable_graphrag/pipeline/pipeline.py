from explainable_graphrag.utils.logger import get_logger

logger = get_logger(__name__)


class GraphRAGPipeline:
    """
    End-to-End GraphRAG pipeline.

    Flow:

    Question
        |
        v
    Entity Linking
        |
        v
    Graph Retrieval
        |
        v
    Prompt Construction
        |
        v
    LLM Generation
    """

    def __init__(
        self,
        graph,
        mapper,
        linker,
        llm,
    ):

        self.graph = graph
        self.mapper = mapper
        self.linker = linker
        self.llm = llm


    def run(
        self,
        question: str,
    ):

        logger.info(
            "========== PIPELINE START =========="
        )

        logger.info(
            f"Question: {question}"
        )


        # -------------------------------
        # 1. Entity Linking
        # -------------------------------

        logger.info(
            "Step 1: Entity Linking"
        )


        entities = self.linker.link(
            question
        )


        logger.info(
            f"Entities: {entities}"
        )


        # -------------------------------
        # 2. Graph Retrieval
        # -------------------------------

        logger.info(
            "Step 2: Graph Retrieval"
        )


        subgraph = self._retrieve_subgraph(
            entities
        )


        logger.info(
            f"Subgraph nodes: {subgraph.number_of_nodes()}"
        )


        # -------------------------------
        # 3. Prompt
        # -------------------------------

        logger.info(
            "Step 3: Prompt Building"
        )


        prompt = self._build_prompt(
            question,
            subgraph
        )


        logger.info(
            prompt
        )


        # -------------------------------
        # 4. LLM
        # -------------------------------

        logger.info(
            "Step 4: LLM Generation"
        )


        answer = self.llm.generate(
            prompt
        )


        logger.info(
            "========== PIPELINE END =========="
        )


        return {

            "question": question,

            "entities": entities,

            "subgraph": subgraph,

            "prompt": prompt,

            "answer": answer,

        }



    def _retrieve_subgraph(
        self,
        entities,
    ):

        nodes = []


        for entity in entities:


            if isinstance(entity, dict):

                node_id = entity.get(
                    "node_id"
                )

            else:

                node_id = entity



            if node_id in self.graph:

                nodes.append(
                    node_id
                )


        return self.graph.subgraph(
            nodes
        )



    def _build_prompt(
        self,
        question,
        subgraph,
    ):


        evidence = []


        for u, v, data in subgraph.edges(
            data=True
        ):

            relation = data.get(
                "relation",
                "related_to"
            )


            evidence.append(
                f"{u} -- {relation} --> {v}"
            )


        evidence_text = "\n".join(
            evidence
        )


        return f"""
You are a medical assistant.

Use only the knowledge graph evidence.

Question:
{question}


Evidence:
{evidence_text}


Answer:
"""