from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from app.core.schemas import StandardResponse


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Обработчик HTTPException - оборачивает в StandardResponse"""
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse(
            message=exc.detail,
            data=None
        ).model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Обработчик ошибок валидации - оборачивает в StandardResponse"""
    errors = exc.errors()
    error_messages = []
    for error in errors:
        field = " -> ".join(str(loc) for loc in error["loc"])
        error_messages.append(f"{field}: {error['msg']}")
    
    message = "Validation error: " + "; ".join(error_messages)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=StandardResponse(
            message=message,
            data={"errors": errors}
        ).model_dump()
    )
