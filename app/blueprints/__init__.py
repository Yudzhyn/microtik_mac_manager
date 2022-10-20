# exceptions
from requests.exceptions import ConnectionError

# response templates
from dataclasses import dataclass

# type hints
from typing import Optional, Any, Dict


# - Response Templates --------------------------------------------------------

@dataclass
class ResponseTemplate:
    success: bool = False
    error: Optional[str] = None


# - Constants -----------------------------------------------------------------

ERROR_RESPONSE_MESSAGES: Dict[Any, str] = {
    ConnectionError: "Помилка при під'єднанні на сервер. Проблема з мережею.",
    KeyError: "Ключ є не правильний або не існує в запиті."
}

# - Blueprints ----------------------------------------------------------------

from .locations_routers import locations_blueprint
