from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from explainable_graphrag.serving.service_container import ServiceContainer
from explainable_graphrag.utils.logger import get_logger


logger = get_logger(__name__)



app = FastAPI(
    title="ExplainableCKG API",
    version="1.0.0",
)



# =====================================================
# CORS Configuration
# =====================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)



# =====================================================
# Request / Response Models
# =====================================================

class ChatRequest(BaseModel):

    question: str



class ChatResponse(BaseModel):

    answer: str

    evidence: str | dict | list | None = None

    metadata: dict = {}



# =====================================================
# Service Initialization
# =====================================================

container = ServiceContainer(
    "src/explainable_graphrag/kg/Diabetes_large.owl"
)



# =====================================================
# Routes
# =====================================================

@app.get("/")
def root():

    return {
        "status": "running",
        "service": "ExplainableCKG"
    }




@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest
):

    logger.info(
        "Received question: %s",
        request.question
    )


    result = container.ask(
        request.question
    )


    logger.info(
        "Result keys: %s",
        result.keys()
    )


    logger.info(
        "Evidence: %s",
        result.get("evidence")
    )



    return ChatResponse(

        answer=result["answer"],

        evidence=result.get("evidence"),

        metadata=result.get("metadata", {})

    )