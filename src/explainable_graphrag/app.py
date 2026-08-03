from pipeline.pipeline import ExplainableGraphRAG

pipeline = ExplainableGraphRAG()

pipeline.initialize()

pipeline.ask(
    "Does obesity increase diabetes risk?"
)