from explainable_graphrag.pipeline.result import PipelineResult



def test_result():

    result = PipelineResult(

        answer="test",

        route="MEDICAL",

        evidence=[]

    )


    assert result.answer == "test"

    assert result.route == "MEDICAL"