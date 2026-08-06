from explainable_graphrag.serving.service_container import ServiceContainer
from explainable_graphrag.serving.medical_router import MedicalRouter



def test_router_creation():

    container = ServiceContainer(
        "kg/Diabetes_large.owl"
    )


    router = MedicalRouter(
        container.llm
    )


    assert router is not None