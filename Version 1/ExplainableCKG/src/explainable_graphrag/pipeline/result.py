from dataclasses import dataclass
from typing import Any



@dataclass
class PipelineResult:
    """
    Standard response object
    returned to UI.
    """


    answer: str


    route: str


    evidence: Any = None


    metadata: dict | None = None