from explainable_graphrag.pipeline.pipeline import GraphRAGPipeline

from explainable_graphrag.kg.graph_manager import GraphManager
from explainable_graphrag.kg.node_mapper import NodeMapper

from explainable_graphrag.retrieval.entity_extractor import EntityExtractor
from explainable_graphrag.retrieval.sapbert_linker import SapBERTLinker
from explainable_graphrag.retrieval.subgraph_retriever import SubgraphRetriever
from explainable_graphrag.retrieval.evidence_builder import EvidenceBuilder

from explainable_graphrag.llm.model import SmallLLM


def build_pipeline():

    ####################################################
    # 1. Load Knowledge Graph
    ####################################################

    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()



    ####################################################
    # 2. Node Mapper
    ####################################################

    mapper = NodeMapper(
        graph
    )



    ####################################################
    # 3. Entity Extractor
    ####################################################

    extractor = EntityExtractor()



    ####################################################
    # 4. Entity Linker
    ####################################################

    linker = SapBERTLinker(
        graph
    )



    ####################################################
    # 5. Subgraph Retriever
    ####################################################

    retriever = SubgraphRetriever(
        graph
    )



    ####################################################
    # 6. Evidence Builder
    ####################################################

    evidence_builder = EvidenceBuilder(
        mapper
    )



    ####################################################
    # 7. LLM
    ####################################################

    llm = SmallLLM(
        model_name="Qwen/Qwen2.5-0.5B-Instruct"
    )


    llm.load()



    ####################################################
    # 8. Pipeline
    ####################################################

    pipeline = GraphRAGPipeline(

        graph=graph,

        mapper=mapper,

        extractor=extractor,

        linker=linker,

        retriever=retriever,

        evidence_builder=evidence_builder,

        llm=llm,

    )


    return pipeline



def test_pipeline():


    pipeline = build_pipeline()



    question = (
        "What are the major risk factors and complications of Type 2 diabetes"
    )



    result = pipeline.run(
        question
    )



    print("\n")
    print("=" * 80)
    print("FINAL PIPELINE RESULT")
    print("=" * 80)



    print("\nQUESTION:")
    print(
        result["question"]
    )



    print("\nEXTRACTED MENTIONS:")

    for mention in result["mentions"]:

        print(
            mention
        )



    print("\nLINKED ENTITIES:")

    for entity in result["linked_entities"]:

        print(
            entity
        )



    print("\nNODE IDS:")

    for node in result["node_ids"]:

        print(
            node
        )



    print("\nSUBGRAPH:")

    print(
        "Nodes:",
        result["subgraph"].number_of_nodes()
    )


    print(
        "Edges:",
        result["subgraph"].number_of_edges()
    )



    print("\nEVIDENCE:")

    print(
        result["evidence"]
    )



    print("\nPROMPT:")

    print(
        result["prompt"]
    )



    print("\nANSWER:")

    print(
        result["answer"]
    )



    ####################################################
    # Assertions
    ####################################################

    assert result is not None

    assert "answer" in result

    assert result["answer"] is not None

    assert "linked_entities" in result

    assert "subgraph" in result