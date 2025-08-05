from fastapi import FastAPI
from contextlib import asynccontextmanager
from threading import Thread
import uvicorn

from application.services.message_service import MessageService
from infrastructure.kafka.kafka_consumer_adapter import KafkaMessageConsumerAdapter


message_service = MessageService(consumer=KafkaMessageConsumerAdapter())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Início da aplicação
    thread = Thread(target=message_service.iniciar_consumo, daemon=True)
    thread.start()

    yield  # Libera a execução do servidor

    # Encerramento da aplicação (se necessário)
    # Ex: fechar DB, consumidores Kafka, etc.


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
