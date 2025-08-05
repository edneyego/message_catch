from confluent_kafka import Consumer

from domain.models import Mensagem
from domain.ports.message_repository import MessageConsumerPort
from infrastructure.kafka.kafka_settings import BOOTSTRAP_SERVERS, TOPICOS
import json


class KafkaMessageConsumerAdapter(MessageConsumerPort):
    def __init__(self):
        self._consumer = Consumer({
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'group.id': 'grupo-consumidor-service',
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest'
        })
        self._consumer.subscribe(TOPICOS)

    def consumir(self) -> None:
        print("🎧 Consumidor Kafka iniciado...")

        while True:
            msg = self._consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print("❌ Erro:", msg.error())
                continue

            try:
                conteudo = json.loads(msg.value().decode())
                mensagem = Mensagem(topico=msg.topic(), dados=conteudo)
                self._processar_mensagem(mensagem)
                self._consumer.commit(msg)
            except Exception as e:
                print("❌ Erro ao processar mensagem:", e)

    def _processar_mensagem(self, mensagem: Mensagem):
        # Lógica de negócio (ou chamar um caso de uso) pode ser feita aqui
        print(f"📥 [{mensagem.topico}] Mensagem recebida: {mensagem.dados}")
