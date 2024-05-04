import logging

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from mangum import Mangum

from app.classification.api_v1 import classification_v1_router
from app.classification.text_classification import USER_MESSAGE_MAX_LENGTH
from app.utils.error import BusinessException

app = FastAPI()
app.include_router(classification_v1_router)

# Simple logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, err: BusinessException):
    """
    Method handle errors.
    - Log as error if server or subsystem has a problem
    - Log client errors as info.
    """
    if err.code >= 500:
        logger.error("Call failed for: %s with error: %s", request.url, err)
        logger.exception("message")
    else:
        logger.info(
            "Call failed for: %s with code: %s , msg: %s",
            request.url,
            err.code,
            err.message,
        )
    return JSONResponse(
        status_code=err.code,
        content=err.get_result(),
    )


@app.get("/health")
def check_health():
    return {"health": "OK"}


class Operation:
    def __init__(
        self,
        name: str,
        url: str,
        method: str,
        description: str,
        query_params: dict | None = None,
        request_body: dict | None = None,
        reponse_body: dict | None = None,
    ):
        self.name = name
        self.url = url
        self.method = method
        self.query_params = query_params
        self.description = description
        self.request_body = request_body
        self.response_body = reponse_body


class Operations:
    def __init__(self, operations: list[Operation]):
        self.operations = operations


@app.get("/")
def get_operations():
    """
    Build the list of operations with name, url and description.
    Operations represent the endpoints that are provided by the service.
    """
    healthCheckOperation = Operation(
        "health",
        "{baseUrl}/health",
        "GET",
        "Endpoint to check if API is ready for requests",
    )

    classificationOperation = Operation(
        "text_classification",
        "{baseUrl}/classification/v1",
        "POST",
        "Classify a text for ok, hate_speech, sexual_harassment, spam. The support languages are German, French, Spanish, and Italian",
        None,
        {
            "text": "Text that has to be classified with max character of: {}".format(
                USER_MESSAGE_MAX_LENGTH
            )
        },
        {
            "language": "'German' | 'French' | 'Spanish' | 'Italian'",
            "text_class": "'ok' | 'sexual harassment' | 'hate speech' | 'spam'",
            "intensity": "'strong' | 'moderate' | 'low'",
            # action: ActionEnum,
            "explanation": "Explation of classification.",
        },
    )

    operations = Operations(operations=[healthCheckOperation, classificationOperation])
    return JSONResponse(content=jsonable_encoder(operations))


handler = Mangum(app=app)
