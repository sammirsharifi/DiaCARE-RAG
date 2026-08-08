from __future__ import annotations

import pickle
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from explainable_graphrag.utils.logger import get_logger
from explainable_graphrag.utils.timer import Timer
from explainable_graphrag.utils.progress import progress

logger = get_logger(__name__)


class SapBERTLinker:
    """
    Medical Entity Linking using SapBERT.

    Features
    --------
    ✓ GPU Support
    ✓ Embedding Cache
    ✓ Top-K Retrieval
    ✓ Similarity Threshold
    ✓ Batch Linking
    """

    def __init__(
        self,
        graph,
        cache_dir: str = "cache",
        model_name: str = "cambridgeltl/SapBERT-from-PubMedBERT-fulltext",
    ):

        self.graph = graph

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        logger.info("=" * 60)
        logger.info("Initializing SapBERT Linker")
        logger.info(f"Device : {self.device}")

        with Timer(logger, "Loading SapBERT Model"):

            self.model = SentenceTransformer(
                model_name,
                device=self.device,
            )

        self.nodes = []
        self.labels = []

        logger.info("Collecting ontology labels...")

        with Timer(logger, "Collect Labels"):

            for node, data in progress(

                graph.nodes(data=True),

                total=graph.number_of_nodes(),

                desc="Ontology Labels",

                unit="node",

            ):

                label = data.get("label", node)

                self.nodes.append(node)

                self.labels.append(
                    str(label).strip()
                )

        logger.info(
            f"Collected {len(self.labels)} labels."
        )

        cache_path = Path(cache_dir)
        cache_path.mkdir(exist_ok=True)

        self.cache_file = (
            cache_path /
            "sapbert_embeddings.pkl"
        )

        self.embeddings = self._load_embeddings()

        logger.info("=" * 60)

    ##########################################################################

    def _load_embeddings(self):

        if self.cache_file.exists():

            logger.info(
                "Loading cached ontology embeddings..."
            )

            with Timer(logger, "Load Embedding Cache"):

                with open(
                    self.cache_file,
                    "rb",
                ) as f:

                    embeddings = pickle.load(f)

            return embeddings

        logger.info(
            "Encoding ontology concepts..."
        )

        with Timer(logger, "Encode Ontology"):

            embeddings = self.model.encode(

                self.labels,

                batch_size=64,

                show_progress_bar=True,

                convert_to_numpy=True,

            )

        logger.info(
            "Saving embedding cache..."
        )

        with open(
            self.cache_file,
            "wb",
        ) as f:

            pickle.dump(
                embeddings,
                f,
            )

        logger.info(
            f"Embeddings cached in {self.cache_file}"
        )

        return embeddings

    ##########################################################################

    def link(

        self,

        mention: str,

        top_k: int = 5,

        threshold: float = 0.60,

    ) -> Dict:

        logger.info(
            f"Linking entity : '{mention}'"
        )

        with Timer(logger, "Entity Linking"):

            query_embedding = self.model.encode(

                [mention],

                convert_to_numpy=True,

            )

            scores = cosine_similarity(

                query_embedding,

                self.embeddings,

            )[0]

            ranking = np.argsort(scores)[::-1]

            matches = []

            for idx in ranking:

                score = float(scores[idx])

                if score < threshold:
                    break

                matches.append(

                    {

                        "node": self.nodes[idx],

                        "label": self.labels[idx],

                        "score": round(score, 4),

                    }

                )

                if len(matches) >= top_k:
                    break

        logger.info(
            f"Found {len(matches)} candidate(s)."
        )

        return {

            "mention": mention,

            "matches": matches,

        }

    ##########################################################################

    def batch_link(

        self,

        mentions: List[str],

        top_k: int = 5,

        threshold: float = 0.60,

    ) -> List[Dict]:

        logger.info(
            f"Batch Linking ({len(mentions)} entities)"
        )

        outputs = []

        with Timer(logger, "Batch Entity Linking"):

            query_embeddings = self.model.encode(

                mentions,

                convert_to_numpy=True,

            )

            similarity = cosine_similarity(

                query_embeddings,

                self.embeddings,

            )

            iterator = zip(
                mentions,
                similarity,
            )

            for mention, scores in progress(

                iterator,

                total=len(mentions),

                desc="Entity Linking",

                unit="entity",

            ):

                ranking = np.argsort(
                    scores
                )[::-1]

                matches = []

                for idx in ranking:

                    score = float(scores[idx])

                    if score < threshold:
                        break

                    matches.append(

                        {

                            "node": self.nodes[idx],

                            "label": self.labels[idx],

                            "score": round(score, 4),

                        }

                    )

                    if len(matches) >= top_k:
                        break

                outputs.append(

                    {

                        "mention": mention,

                        "matches": matches,

                    }

                )

        logger.info(
            f"Finished Batch Linking ({len(outputs)} entities)."
        )

        return outputs