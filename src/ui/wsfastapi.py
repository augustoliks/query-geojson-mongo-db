from fastapi import (
    Request,
    FastAPI,
    status
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import domain
from domain.exceptions import DomainBaseException
from domain import valueobjects
from domain import entities


def configure_routers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: DomainBaseException):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"detail": str(exc)})
        )

    @app.post("/employer")
    async def create_employer(employer: entities.Employer):
        return domain.create_new_employer(employer)

    @app.get("/employer")
    async def get_employer(point: valueobjects.Point):
        return domain.get_employer_most_nearest(point)


def create_app():
    app = FastAPI()
    configure_routers(app)