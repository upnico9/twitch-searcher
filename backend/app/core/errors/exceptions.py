from fastapi import HTTPException
from typing import Any, Dict, Optional

class AppException(HTTPException):
    def __init__(
        self, 
        status_code: int, 
        detail: str,
        error_code: str = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class ResourceNotFoundException(AppException):
    def __init__(self, resource_name: str, resource_id: Any = None):
        detail = f"{resource_name} not found"
        if resource_id:
            detail += f" with id: {resource_id}"
        super().__init__(
            status_code=404, 
            detail=detail,
            error_code="RESOURCE_NOT_FOUND"
        )

class ExternalServiceException(AppException):
    def __init__(self, service_name: str, detail: str = None):
        super().__init__(
            status_code=503,
            detail=f"{service_name} service unavailable: {detail or 'Unknown error'}",
            error_code="EXTERNAL_SERVICE_ERROR"
        )

class ValidationException(AppException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )

class DatabaseException(AppException):
    def __init__(self, operation: str, detail: str = None):
        super().__init__(
            status_code=500,
            detail=f"Database {operation} failed: {detail or 'Unknown error'}",
            error_code="DATABASE_ERROR"
        )