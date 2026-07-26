from __future__ import annotations

import networkx as nx

from explainable_graphrag.kg.node_mapper import NodeMapper
from explainable_graphrag.utils.logger import get_logger
from explainable_graphrag.utils.timer import Timer


logger = get_logger(__name__)


class EvidenceBuilder:
    """
    Convert retrieved evidence subgraph into
    human-readable medical evidence text.
    """


    def __init__(
        self,
        mapper: NodeMapper,
    ):
        """
        Initialize EvidenceBuilder.

        Parameters
        ----------
        mapper:
            NodeMapper instance for converting
            node ids into human labels.
        """

        self.mapper = mapper


    ##############################################################

    def build(
        self,
        graph: nx.MultiDiGraph,
    ) -> str:
        """
        Convert evidence graph into text.

        Parameters
        ----------
        graph:
            Retrieved evidence subgraph.

        Returns
        -------
        str
            Human-readable evidence.
        """


        logger.info(
            "Building evidence text..."
        )


        with Timer(
            logger,
            "Evidence Building",
        ):


            evidence_lines = []


            ######################################################
            # Convert edges to statements
            ######################################################

            for u, v, data in graph.edges(
                data=True
            ):


                source = self.mapper.id_to_label(
                    u
                )


                target = self.mapper.id_to_label(
                    v
                )


                relation = data.get(
                    "relation",
                    "related_to"
                )


                statement = (

                    f"{source} "
                    f"{relation} "
                    f"{target}"

                )


                evidence_lines.append(
                    statement
                )



        evidence_text = "\n".join(
            evidence_lines
        )


        logger.info(
            f"Generated Evidence Statements : {len(evidence_lines)}"
        )


        return evidence_text