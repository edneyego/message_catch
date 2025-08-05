from abc import ABC, abstractmethod
from domain.models import Mensagem


class MessageConsumerPort(ABC):
    @abstractmethod
    def consumir(self) -> None:
        """Consome mensagens de um ou mais tópicos Kafka"""
        pass
