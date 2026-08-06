from pydantic import BaseModel


class ChatRequest(BaseModel):

    question: str



class EvidenceResponse(BaseModel):

    answer: str

    route: str

    evidence: object | None = None

    metadata: dict | None = None