from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .text_classification import classify

classification_v1_router = APIRouter(
    prefix="/classification/v1",
    tags=["classification"],
    responses={404: {"description": "Not found"}},
)


class Message(BaseModel):
    text: str
    # action_level: str | None = None
    # strictness_level: str | None = None


@classification_v1_router.post("/")
async def classifiy_text_endpoint(message: Message):
    # Evaluate message
    classificationResult = await classify(message.text)
    response_json = jsonable_encoder(classificationResult)

    return JSONResponse(content=response_json)
