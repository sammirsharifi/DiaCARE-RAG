from explainable_graphrag.serving.service_container import ServiceContainer


def test_container():

    container = ServiceContainer(
        "kg/Diabetes_large.owl"
    )


    assert container.graph is not None
    assert container.llm is not None
    assert container.retriever is not None