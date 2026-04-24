from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import DataError
from uuid import UUID
from datetime import datetime


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "type": "validation_error",
                "detail": exc.errors()
            },
            "message": "Error de validación en los datos proporcionados",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def integrity_exception_handler(request: Request, exc: IntegrityError):
    error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    if "unique constraint" in error_msg.lower() or "duplicate" in error_msg.lower():
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "success": False,
                "error": {
                    "type": "duplicate_error",
                    "detail": "El recurso ya existe"
                },
                "message": "Violación de restricción única. El email ya está registrado.",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "type": "integrity_error",
                "detail": error_msg
            },
            "message": "Error de integridad en la base de datos",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def data_error_exception_handler(request: Request, exc: DataError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": {
                "type": "data_error",
                "detail": str(exc.orig) if hasattr(exc, 'orig') else str(exc)
            },
            "message": "Formato de datos inválido",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": {
                "type": "value_error",
                "detail": str(exc)
            },
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def uuid_error_exception_handler(request: Request, exc: Exception):
    if "UUID" in str(type(exc).__name__) or "invalid token" in str(exc).lower():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "error": {
                    "type": "invalid_uuid",
                    "detail": "El ID proporcionado no es un UUID válido"
                },
                "message": "ID de recurso inválido",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    raise exc


def register_exception_handlers(app):
    from fastapi import FastAPI
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_exception_handler)
    app.add_exception_handler(DataError, data_error_exception_handler)
    app.add_exception_handler(ValueError, value_error_exception_handler)