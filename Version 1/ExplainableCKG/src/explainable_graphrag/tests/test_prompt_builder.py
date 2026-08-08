from explainable_graphrag.llm.prompt_builder import (
    PromptBuilder,
)

from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)



def test_prompt_builder():


    builder = PromptBuilder()


    question = (
        "What complications can obesity cause?"
    )


    evidence = (
        "Obesity leadsTo Insulin Resistance.\n"
        "Insulin Resistance causes Type 2 Diabetes."
    )


    prompt = builder.build(
        question,
        evidence,
    )


    logger.info("=" * 80)
    logger.info("GENERATED PROMPT")
    logger.info("=" * 80)


    logger.info(
        prompt
    )


    logger.info("=" * 80)


    assert len(prompt) > 0

    assert question in prompt

    assert evidence in prompt