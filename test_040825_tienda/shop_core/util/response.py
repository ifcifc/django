from enum import Enum
from typing import Any, Dict, Tuple, Union, Optional

from django.http import JsonResponse


# Enum con los posibles estados de una respuesta
class ResponseStatus(Enum):
    SUCCESS = "success"  # Operación exitosa
    FAIL = "fail"  # Fallo controlado (input inválido, datos no encontrados)
    ERROR = "error"  # Error inesperado (excepciones, fallos internos)
    PENDING = "pending"  # Operación en curso o pendiente
    UNAUTHORIZED = "unauthorized"  # Falta de autenticación/autorización
    NOT_FOUND = "not_found"  # Recurso no encontrado


# Función para construir una respuesta JSON estandarizada
def make_response(
    status: ResponseStatus,
    message: str,
    data: Optional[dict|list|tuple|str] = None,
    status_code: int = 200,
) -> JsonResponse:
    """
    Crea una respuesta JSON estandarizada para ser utilizada en endpoints de una API.

    Args:
        status (ResponseStatus): Estado de la respuesta (SUCCESS, FAIL, etc.).
        message (str): Mensaje descriptivo de la operación.
        data (Any, optional): Datos o errores adicionales. Si es una colección, se incluye 'total'.
        status_code (int, optional): Código de estado HTTP.

    Returns:
        JsonResponse: Objeto JSON serializado con estructura estándar:
    """

    if not isinstance(status, ResponseStatus):
        raise TypeError(f"status debe de ser de tipo ResponseStatus. type: {type(status).__name__}")

    if not isinstance(message, str):
        raise TypeError(f"message debe de ser de tipo str. type: {type(message).__name__}")
    
    if data is not None and not isinstance(data, (dict, list, tuple, str)):
        raise TypeError(f"data debe de ser de tipo dict, list, tuple o str. type: {type(data).__name__}")
    
    if status_code is not None and not isinstance(status_code, int):
        raise TypeError(f"status_code debe de ser de tipo int. type: {type(status_code).__name__}")

    response = {"status": status.value, "message": message or ""}

    if data is not None:
        key = (
            "data"
            if status == ResponseStatus.SUCCESS or status == ResponseStatus.PENDING
            else "error"
        )
        response[key] = data    
        if isinstance(data, (list, set, tuple)):
            response["total"] = len(data)

    return JsonResponse(response, status=status_code)
