from explainable_graphrag.llm.model import SmallLLM
from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)



def test_llm_generation():


    llm = SmallLLM()


    llm.load()


    prompt = """

Evidence:

Obesity leadsTo Insulin Resistance.

Insulin Resistance causes Type 2 Diabetes.


Question:

What relationship exists between obesity and type 2 diabetes?


Answer using only the evidence.
Explain your reasoning and mention the supporting evidence.

"""


    answer = llm.generate(
        prompt
    )


    logger.info("=" * 70)

    logger.info(
        "LLM ANSWER:"
    )

    logger.info(
        answer
    )

    logger.info("=" * 70)


    assert len(answer) > 20