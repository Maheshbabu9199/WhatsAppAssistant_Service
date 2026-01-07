from abc import ABC, abstractmethod

from app.utils.logging_handler import CustomLogger

logger = CustomLogger.get_logger(__name__)


class LLMService(ABC):
    @abstractmethod
    async def generate_response(self, *args, **kwargs) -> str:
        pass
