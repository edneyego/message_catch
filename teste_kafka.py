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

    mensagem = [{
                "codigoEstacao": "34311000",
                "data": "2025-08-22 06:45",
                "sensores": [
                    {
                        "sensor": "chuva_acumulada",
                        "valor": 14.0
                    },
                    {
                        "sensor": "chuva_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_display",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_manual",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_sensor",
                        "valor": -9999.0
                    },
                    {
                        "sensor": "vazao_adotada",
                        "valor": 0.0
                    }
                ]
            },
            {
                "codigoEstacao": "34311000",
                "data": "2025-08-22 07:00",
                "sensores": [
                    {
                        "sensor": "chuva_acumulada",
                        "valor": 14.0
                    },
                    {
                        "sensor": "chuva_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_display",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_manual",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_sensor",
                        "valor": -9999.0
                    },
                    {
                        "sensor": "vazao_adotada",
                        "valor": 0.0
                    }
                ]
            },
            {
                "codigoEstacao": "34311000",
                "data": "2025-08-22 07:15",
                "sensores": [
                    {
                        "sensor": "chuva_acumulada",
                        "valor": 14.0
                    },
                    {
                        "sensor": "chuva_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_display",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_manual",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_sensor",
                        "valor": -9999.0
                    },
                    {
                        "sensor": "vazao_adotada",
                        "valor": 0.0
                    }
                ]
            },
            {
                "codigoEstacao": "34311000",
                "data": "2025-08-22 07:30",
                "sensores": [
                    {
                        "sensor": "chuva_acumulada",
                        "valor": 14.0
                    },
                    {
                        "sensor": "chuva_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_display",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_manual",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_sensor",
                        "valor": -9999.0
                    },
                    {
                        "sensor": "vazao_adotada",
                        "valor": 0.0
                    }
                ]
            },
            {
                "codigoEstacao": "34311000",
                "data": "2025-08-22 07:45",
                "sensores": [
                    {
                        "sensor": "chuva_acumulada",
                        "valor": 14.0
                    },
                    {
                        "sensor": "chuva_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_display",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_manual",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_sensor",
                        "valor": -9999.0
                    },
                    {
                        "sensor": "vazao_adotada",
                        "valor": 0.0
                    }
                ]
            },
            {
                "codigoEstacao": "34311000",
                "data": "2025-08-22 08:00",
                "sensores": [
                    {
                        "sensor": "chuva_acumulada",
                        "valor": 14.0
                    },
                    {
                        "sensor": "chuva_adotada",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_adotada",
                        "valor": 213.0
                    },
                    {
                        "sensor": "cota_display",
                        "valor": 213.0
                    },
                    {
                        "sensor": "cota_manual",
                        "valor": 0.0
                    },
                    {
                        "sensor": "cota_sensor",
                        "valor": -9999.0
                    },
                    {
                        "sensor": "vazao_adotada",
                        "valor": 228.85
                    }
                ]
            }
        ]
                
    json_data = json.dumps(mensagem)

    producer.produce(TOPICO_FILA, value=json_data.encode(), callback=callback)
    producer.flush()

# Consumir com commit manual (só após sucesso)
def consumir_mensagem():
    consumer = Consumer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest',
        'group.id': 'grupo-medicoes'
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
    #criar_topico()
    enviar_mensagem()
    #time.sleep(1)
    #consumir_mensagem()
