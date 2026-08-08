from __future__ import annotations

import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

from explainable_graphrag.utils.logger import get_logger
from explainable_graphrag.utils.timer import Timer


logger = get_logger(__name__)


class SmallLLM:
    """
    Wrapper around Qwen instruction model.

    The LLM does not contain medical knowledge.
    Medical information comes only from retrieved evidence.
    """


    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-0.5B-Instruct",
    ):

        self.model_name = model_name


        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )


        self.tokenizer = None
        self.model = None



    ##############################################################

    def load(self):
        """
        Load tokenizer and model.
        """


        logger.info(
            f"Loading LLM: {self.model_name}"
        )


        with Timer(
            logger,
            "LLM Loading"
        ):


            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
            )


            self.model = AutoModelForCausalLM.from_pretrained(

                self.model_name,

                dtype=(
                    torch.float16
                    if self.device == "cuda"
                    else torch.float32
                ),

                low_cpu_mem_usage=True,

            )


            self.model.to(self.device)


            self.model.eval()



        logger.info(
            f"LLM loaded on {self.device}"
        )



    ##############################################################

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 256,
    ) -> str:
        """
        Generate answer using retrieved evidence only.
        """


        if self.model is None:

            raise RuntimeError(
                "LLM is not loaded. Call load() first."
            )



        logger.info(
            "Generating answer..."
        )



        with Timer(
            logger,
            "LLM Generation"
        ):


            messages = [

                {
                    "role": "system",

                    "content":
                    """
You are an evidence-based assistant.

Your task is to answer questions only using
the provided evidence.

Rules:
- Do not use your own medical knowledge.
- Do not guess.
- If evidence is insufficient, say:
  "The provided evidence is not sufficient."

Always explain which evidence supports your answer.
"""
                },


                {
                    "role": "user",

                    "content": prompt
                }

            ]



            formatted_prompt = (
                self.tokenizer.apply_chat_template(

                    messages,

                    tokenize=False,

                    add_generation_prompt=True,

                )
            )



            inputs = self.tokenizer(

                formatted_prompt,

                return_tensors="pt",

                truncation=True,

                max_length=2048,

            )



            inputs = {

                key: value.to(self.device)

                for key, value in inputs.items()

            }



            with torch.no_grad():

                outputs = self.model.generate(

                    **inputs,

                    max_new_tokens=max_new_tokens,

                    temperature=0.2,

                    top_p=0.9,

                    do_sample=True,

                    repetition_penalty=1.1,

                    pad_token_id=self.tokenizer.eos_token_id,

                )



            generated_tokens = outputs[0][
                inputs["input_ids"].shape[-1]:
            ]



            answer = self.tokenizer.decode(

                generated_tokens,

                skip_special_tokens=True,

            )



        logger.info(
            "Answer generated successfully."
        )


        return answer