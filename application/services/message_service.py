from domain.ports.message_repository import MessageConsumerPort


class MessageService:
    def __init__(self, consumer: MessageConsumerPort):
        self._consumer = consumer

    def iniciar_consumo(self):
        self._consumer.consumir()
