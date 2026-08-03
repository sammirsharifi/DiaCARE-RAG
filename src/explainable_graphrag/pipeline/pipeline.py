from __future__ import annotations

import networkx as nx

from explainable_graphrag.kg.node_mapper import NodeMapper

from explainable_graphrag.retrieval.entity_extractor import EntityExtractor
from explainable_graphrag.retrieval.sapbert_linker import SapBERTLinker
from explainable_graphrag.retrieval.subgraph_retriever import SubgraphRetriever
from explainable_graphrag.retrieval.evidence_builder import EvidenceBuilder

from explainable_graphrag.llm.model import SmallLLM

from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)


class GraphRAGPipeline:
    """
    End-to-End Explainable GraphRAG Pipeline.

    Flow:

    Question
        |
        v
    Entity Extraction
        |
        v
    SapBERT Entity Linking
        |
        v
    Ontology Node Retrieval
        |
        v
    Evidence Subgraph Retrieval
        |
        v
    Evidence Building
        |
        v
    Prompt Construction
        |
        v
    LLM Answer
    """


    def __init__(
        self,
        graph: nx.MultiDiGraph,
        mapper: NodeMapper,
        extractor: EntityExtractor,
        linker: SapBERTLinker,
        retriever: SubgraphRetriever,
        evidence_builder: EvidenceBuilder,
        llm: SmallLLM,
    ):

        self.graph = graph
        self.mapper = mapper
        self.extractor = extractor
        self.linker = linker
        self.retriever = retriever
        self.evidence_builder = evidence_builder
        self.llm = llm



    ############################################################
    # MAIN PIPELINE
    ############################################################

    def run(
        self,
        question: str,
    ):


        logger.info("=" * 80)
        logger.info("GRAPH RAG PIPELINE START")
        logger.info("=" * 80)


        logger.info(
            "QUESTION:\n%s",
            question
        )


        ########################################################
        # STEP 1 - ENTITY EXTRACTION
        ########################################################

        logger.info("")
        logger.info("STEP 1 - ENTITY EXTRACTION")


        mentions = self.extractor.extract(
            question
        )


        logger.info(
            "Extracted mentions : %d",
            len(mentions)
        )


        for idx, mention in enumerate(
            mentions,
            start=1
        ):

            logger.info(
                "%d) %s",
                idx,
                mention
            )



        ########################################################
        # STEP 2 - ENTITY LINKING
        ########################################################

        logger.info("")
        logger.info("STEP 2 - ENTITY LINKING")


        linked_entities = []


        for mention in mentions:


            logger.info(
                "Linking mention: %s",
                mention
            )


            result = self.linker.link(
                mention
            )


            matches = result.get(
                "matches",
                []
            )


            if not matches:


                logger.warning(
                    "No candidate for %s",
                    mention
                )


                continue



            logger.info(
                "Found %d candidates",
                len(matches)
            )



            #
            # Keep ALL SapBERT candidates
            #

            for idx, match in enumerate(
                matches,
                start=1
            ):


                logger.info(
                    "%d) Node=%s | Label=%s | Score=%.4f",
                    idx,
                    match["node"],
                    match["label"],
                    match["score"]
                )


                linked_entities.append(

                    {

                        "mention": mention,

                        "node": match["node"],

                        "label": match["label"],

                        "score": match["score"],

                    }

                )



        logger.info("")
        logger.info(
            "FINAL LINKED ENTITIES"
        )


        for entity in linked_entities:


            logger.info(
                "Mention=%s | Node=%s | Label=%s | Score=%.4f",
                entity["mention"],
                entity["node"],
                entity["label"],
                entity["score"]
            )



        ########################################################
        # Extract node ids
        ########################################################


        node_ids = [

            entity["node"]

            for entity in linked_entities

            if entity["node"] in self.graph

        ]


        logger.info(
            "Ontology nodes selected : %d",
            len(node_ids)
        )



        ########################################################
        # STEP 3 - SUBGRAPH RETRIEVAL
        ########################################################


        logger.info("")
        logger.info("STEP 3 - SUBGRAPH RETRIEVAL")



        if node_ids:


            subgraph = self.retriever.retrieve(
                node_ids
            )


        else:


            logger.warning(
                "No valid ontology nodes"
            )


            subgraph = nx.MultiDiGraph()



        logger.info(
            "Subgraph Nodes : %d",
            subgraph.number_of_nodes()
        )


        logger.info(
            "Subgraph Edges : %d",
            subgraph.number_of_edges()
        )



        ########################################################
        # STEP 4 - EVIDENCE BUILDING
        ########################################################


        logger.info("")
        logger.info("STEP 4 - EVIDENCE BUILDING")


        evidence = self.evidence_builder.build(
            subgraph
        )


        logger.info(
            "Evidence:"
        )


        logger.info(
            "\n%s",
            evidence
        )



        ########################################################
        # STEP 5 - PROMPT BUILDING
        ########################################################


        logger.info("")
        logger.info("STEP 5 - PROMPT BUILDING")


        prompt = self._build_prompt(

            question,

            evidence

        )


        logger.info(
            "Prompt:"
        )


        logger.info(
            "\n%s",
            prompt
        )



        ########################################################
        # STEP 6 - LLM
        ########################################################


        logger.info("")
        logger.info("STEP 6 - LLM GENERATION")


        answer = self.llm.generate(
            prompt
        )


        logger.info(
            "Answer:"
        )


        logger.info(
            "\n%s",
            answer
        )



        logger.info("=" * 80)
        logger.info("GRAPH RAG PIPELINE END")
        logger.info("=" * 80)



        return {

            "question": question,

            "mentions": mentions,

            "linked_entities": linked_entities,

            "node_ids": node_ids,

            "subgraph": subgraph,

            "evidence": evidence,

            "prompt": prompt,

            "answer": answer,

        }




    ############################################################
    # PROMPT BUILDER
    ############################################################


    def _build_prompt(
        self,
        question: str,
        evidence: str,
    ):


        return f"""
You are a medical assistant.

Answer ONLY using the provided knowledge graph evidence.

If evidence is insufficient, say that the knowledge graph
does not contain enough information.

Question:
{question}

Knowledge Graph Evidence:
{evidence}

Answer:
"""