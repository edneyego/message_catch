from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer, Consumer
import json
import time

BOOTSTRAP_SERVERS = 'localhost:9092'
TOPICO_FILA = 'BRANCO'

# Criar tópico com 1 partição (comportamento de fila)
def criar_topico():
    admin = AdminClient({'bootstrap.servers': BOOTSTRAP_SERVERS})
    topic = NewTopic(TOPICO_FILA, num_partitions=1, replication_factor=1)
    fs = admin.create_topics([topic])
    for nome, f in fs.items():
        try:
            f.result()
            print(f'✅ Tópico criado: {nome}')
        except Exception as e:
            print(f'⚠️ {nome}: {e}')  # provavelmente já existe

# Enviar com garantia máxima
def enviar_mensagem():
    producer = Producer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'acks': 'all',
        'enable.idempotence': True,
    })

    def callback(err, msg):
        if err:
            print(f'❌ Erro ao enviar: {err}')
        else:
            print(f'📤 Enviado com sucesso: {msg.value().decode()}')

    mensagem = [{"codigoEstacao": "29050000", "data": "2025-08-05 07:45:00", "cota": 339, "chuva": 53.8, "cota2": -9999}, {"codigoEstacao": "29050000", "data": "2025-08-05 08:00:00", "cota": 339, "chuva": 53.8, "cota2": -9999}, {"codigoEstacao": "29050000", "data": "2025-08-05 08:15:00", "cota": 339, "chuva": 53.8, "cota2": -9999}, {"codigoEstacao": "29050000", "data": "2025-08-05 08:30:00", "cota": 339, "chuva": 53.8, "cota2": -9999}, {"codigoEstacao": "23700000", "data": "2025-08-05 07:45:00", "cota": 78, "chuva": 46.0, "cota2": -9999}, {"codigoEstacao": "23700000", "data": "2025-08-05 08:00:00", "cota": 78, "chuva": 46.0, "cota2": -9999}, {"codigoEstacao": "23700000", "data": "2025-08-05 08:15:00", "cota": 78, "chuva": 46.0, "cota2": -9999}, {"codigoEstacao": "23700000", "data": "2025-08-05 08:30:00", "cota": 78, "chuva": 46.0, "cota2": -9999}, {"codigoEstacao": "27500000", "data": "2025-08-05 07:45:00", "cota": 307, "chuva": 246.8, "cota2": -9999}, {"codigoEstacao": "27500000", "data": "2025-08-05 08:00:00", "cota": 307, "chuva": 246.8, "cota2": -9999}, {"codigoEstacao": "27500000", "data": "2025-08-05 08:15:00", "cota": 307, "chuva": 246.8, "cota2": -9999}, {"codigoEstacao": "27500000", "data": "2025-08-05 08:30:00", "cota": 307, "chuva": 246.8, "cota2": -9999}, {"codigoEstacao": "18390000", "data": "2025-08-05 07:45:00", "cota": 490, "chuva": 267.2, "cota2": -9999}, {"codigoEstacao": "18390000", "data": "2025-08-05 08:00:00", "cota": 489, "chuva": 267.2, "cota2": -9999}, {"codigoEstacao": "18390000", "data": "2025-08-05 08:15:00", "cota": 489, "chuva": 267.2, "cota2": -9999}, {"codigoEstacao": "18390000", "data": "2025-08-05 08:30:00", "cota": 488, "chuva": 267.2, "cota2": -9999}, {"codigoEstacao": "15560000", "data": "2025-08-05 07:30:00", "cota": 676, "chuva": 367.0, "cota2": -9999}, {"codigoEstacao": "15560000", "data": "2025-08-05 07:45:00", "cota": 676, "chuva": 367.0, "cota2": -9999}, {"codigoEstacao": "15560000", "data": "2025-08-05 08:00:00", "cota": 676, "chuva": 367.0, "cota2": -9999}, {"codigoEstacao": "15560000", "data": "2025-08-05 08:15:00", "cota": 676, "chuva": 367.0, "cota2": -9999}, {"codigoEstacao": "19500000", "data": "2025-08-05 07:45:00", "cota": 206, "chuva": 1450.2, "cota2": -9999}, {"codigoEstacao": "19500000", "data": "2025-08-05 08:00:00", "cota": 204, "chuva": 1450.2, "cota2": -9999}, {"codigoEstacao": "19500000", "data": "2025-08-05 08:15:00", "cota": 205, "chuva": 1450.2, "cota2": -9999}, {"codigoEstacao": "19500000", "data": "2025-08-05 08:30:00", "cota": 206, "chuva": 1450.2, "cota2": -9999}, {"codigoEstacao": "30300000", "data": "2025-08-05 07:45:00", "cota": 531, "chuva": 1273.0, "cota2": -9999}, {"codigoEstacao": "30300000", "data": "2025-08-05 08:00:00", "cota": 531, "chuva": 1273.0, "cota2": -9999}, {"codigoEstacao": "30300000", "data": "2025-08-05 08:15:00", "cota": 531, "chuva": 1273.0, "cota2": -9999}, {"codigoEstacao": "30300000", "data": "2025-08-05 08:30:00", "cota": 531, "chuva": 1273.0, "cota2": -9999}, {"codigoEstacao": "28850000", "data": "2025-08-05 08:00:00", "cota": 270, "chuva": 73.6, "cota2": -9999}, {"codigoEstacao": "28850000", "data": "2025-08-05 08:15:00", "cota": 270, "chuva": 73.6, "cota2": -9999}, {"codigoEstacao": "28850000", "data": "2025-08-05 08:30:00", "cota": 270, "chuva": 73.6, "cota2": -9999}, {"codigoEstacao": "28850000", "data": "2025-08-05 08:45:00", "cota": 270, "chuva": 73.6, "cota2": -9999}, {"codigoEstacao": "18650000", "data": "2025-08-05 07:30:00", "cota": -9999, "chuva": 14.0, "cota2": -9999}, {"codigoEstacao": "18650000", "data": "2025-08-05 07:45:00", "cota": -9999, "chuva": 14.0, "cota2": -9999}, {"codigoEstacao": "18650000", "data": "2025-08-05 08:00:00", "cota": -9999, "chuva": 14.0, "cota2": -9999}, {"codigoEstacao": "18650000", "data": "2025-08-05 08:15:00", "cota": -9999, "chuva": 14.0, "cota2": -9999}, {"codigoEstacao": "15150000", "data": "2025-08-05 07:45:00", "cota": 423, "chuva": 67.2, "cota2": -9999}, {"codigoEstacao": "15150000", "data": "2025-08-05 08:00:00", "cota": 423, "chuva": 67.2, "cota2": -9999}, {"codigoEstacao": "15150000", "data": "2025-08-05 08:15:00", "cota": 423, "chuva": 67.2, "cota2": -9999}, {"codigoEstacao": "15150000", "data": "2025-08-05 08:30:00", "cota": 423, "chuva": 67.2, "cota2": -9999}, {"codigoEstacao": "30080000", "data": "2025-08-05 07:45:00", "cota": 488, "chuva": 1407.8, "cota2": -9999}, {"codigoEstacao": "30080000", "data": "2025-08-05 08:00:00", "cota": 487, "chuva": 1407.8, "cota2": -9999}, {"codigoEstacao": "30080000", "data": "2025-08-05 08:15:00", "cota": 487, "chuva": 1407.8, "cota2": -9999}, {"codigoEstacao": "30080000", "data": "2025-08-05 08:30:00", "cota": 487, "chuva": 1407.8, "cota2": -9999}, {"codigoEstacao": "17900000", "data": "2025-08-05 07:45:00", "cota": 665, "chuva": 1166.4, "cota2": -9999}, {"codigoEstacao": "17900000", "data": "2025-08-05 08:00:00", "cota": 664, "chuva": 1166.4, "cota2": -9999}, {"codigoEstacao": "17900000", "data": "2025-08-05 08:15:00", "cota": 665, "chuva": 1166.4, "cota2": -9999}, {"codigoEstacao": "17900000", "data": "2025-08-05 08:30:00", "cota": 665, "chuva": 1166.4, "cota2": -9999}, {"codigoEstacao": "17050001", "data": "2025-08-05 07:45:00", "cota": 712, "chuva": 822.4, "cota2": -9999}, {"codigoEstacao": "17050001", "data": "2025-08-05 08:00:00", "cota": 711, "chuva": 822.4, "cota2": -9999}, {"codigoEstacao": "17050001", "data": "2025-08-05 08:15:00", "cota": 711, "chuva": 822.4, "cota2": -9999}, {"codigoEstacao": "17050001", "data": "2025-08-05 08:30:00", "cota": 710, "chuva": 822.4, "cota2": -9999}]
                
    json_data = json.dumps(mensagem)

    producer.produce(TOPICO_FILA, value=json_data.encode(), callback=callback)
    producer.flush()

# Consumir com commit manual (só após sucesso)
def consumir_mensagem():
    consumer = Consumer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([TOPICO_FILA])
    print("⏳ Aguardando mensagem...")

    msg = consumer.poll(timeout=10.0)
    if msg is None:
        print("⚠️ Nenhuma mensagem.")
        return
    if msg.error():
        print("Erro:", msg.error())
        return

    try:
        conteudo = json.loads(msg.value().decode())
        print(f"📥 Mensagem recebida: {conteudo}")
        # Simula processamento
        time.sleep(1)
        print("✅ Processado com sucesso. Confirmando...")
        consumer.commit(msg)
    except Exception as e:
        print("❌ Erro no processamento:", e)
    finally:
        consumer.close()

if __name__ == "__main__":
    criar_topico()
    enviar_mensagem()
    #time.sleep(1)
    #consumir_mensagem()
