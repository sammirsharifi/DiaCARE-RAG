from explainable_graphrag.pipeline.pipeline import GraphRAGPipeline


from explainable_graphrag.kg.graph_manager import GraphManager
from explainable_graphrag.kg.node_mapper import NodeMapper


from explainable_graphrag.retrieval.sapbert_linker import SapBERTLinker


from explainable_graphrag.llm.model import SmallLLM



def build_pipeline():


    graph = GraphManager(
        "kg/Diabetes_large.owl"
    ).load()



    mapper = NodeMapper(
        graph
    )



    linker = SapBERTLinker(
        graph
    )



    llm = SmallLLM(
        model_name=
        "Qwen/Qwen2.5-0.5B-Instruct"
    )


    llm.load()



    pipeline = GraphRAGPipeline(

        graph=graph,

        mapper=mapper,

        linker=linker,

        llm=llm,

    )


    return pipeline





def test_pipeline():


    pipeline = build_pipeline()



    question = (
        "What are the main risk factors "
        "for type 2 diabetes?"
    )



    result = pipeline.run(
        question
    )



    print(
        "\n========== PIPELINE RESULT =========="
    )


    print(
        "QUESTION:"
    )

    print(
        result["question"]
    )


    print(
        "\nENTITIES:"
    )

    print(
        result["entities"]
    )


    print(
        "\nSUBGRAPH:"
    )

    print(
        "Nodes:",
        result["subgraph"].number_of_nodes()
    )


    print(
        "Edges:",
        result["subgraph"].number_of_edges()
    )


    print(
        "\nPROMPT:"
    )

    print(
        result["prompt"]
    )


    print(
        "\nANSWER:"
    )

    print(
        result["answer"]
    )



    assert result is not None

    assert "answer" in result

    assert result["answer"] is not None