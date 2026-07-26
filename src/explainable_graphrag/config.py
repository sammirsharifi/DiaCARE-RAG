from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

ONTOLOGY_PATH = PROJECT_ROOT / "kg" / "diabetes_large.owl"

CACHE_DIR = PROJECT_ROOT / "cache"

LOG_DIR = PROJECT_ROOT / "logs"

GRAPH_CACHE = CACHE_DIR / "graph.pkl"

MAPPER_CACHE = CACHE_DIR / "mapper.pkl"

EMBEDDING_CACHE = CACHE_DIR / "sapbert_embeddings.npy"

LABEL_CACHE = CACHE_DIR / "sapbert_labels.pkl"

SAPBERT_MODEL = "cambridgeltl/SapBERT-from-PubMedBERT-fulltext"

LLM_MODEL = "microsoft/Phi-3-mini-4k-instruct"