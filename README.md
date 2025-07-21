# 📬 message_catch

Projeto responsável por orquestrar o ambiente de mensageria com **Apache Kafka**, utilizando Docker Compose. Este projeto suporta:

- **Tópicos** (broadcast para múltiplos consumidores)
- **Filas simuladas** (1 partição + 1 grupo → comportamento de fila)
- **Entrega garantida (estilo SQS)** via commit manual e idempotência

---

## 🚀 Subindo o ambiente Kafka

```bash
docker-compose up -d
```

### Serviços disponíveis:

| Serviço   | Porta       | Descrição                     |
|-----------|-------------|-------------------------------|
| Kafka     | 9092        | Broker de mensageria          |
| Zookeeper | 2181        | Coordenação dos brokers       |
| Kafdrop   | 19000       | Interface web para tópicos    |

---

## 📦 Tópicos utilizados

| Nome               | Tipo                  | Partições | Uso                                      |
|--------------------|-----------------------|-----------|------------------------------------------|
| `topico-dados`     | Broadcast             | 3         | Múltiplos grupos consomem a mesma mensagem |
| `fila-dados`       | Fila simulada         | 1         | Apenas um grupo consome cada mensagem      |
| `fila-segura`      | Fila com garantia     | 1         | Commit manual após processamento           |
| `fila-segura-java` | Fila com garantia     | 1         | Versão para testes em Java 8               |

---

## 🐍 Exemplo em Python

### ✅ Requisitos

Instalar dependências:

```bash
pip install confluent_kafka
```

### 📄 Scripts

| Arquivo                      | Descrição                                            |
|-----------------------------|------------------------------------------------------|
| `kafka_teste.py`            | Cria tópicos e envia para `topico-dados` e `fila-dados` |
| `garantia_entrega_kafka.py` | Exemplo com entrega garantida (estilo SQS)          |

### ▶️ Executar

```bash
python kafka_teste.py
python garantia_entrega_kafka.py
```

---

## ☕ Exemplo em Java 8

### ✅ Dependência Maven

Adicionar ao `pom.xml`:

```xml
<dependency>
  <groupId>org.apache.kafka</groupId>
  <artifactId>kafka-clients</artifactId>
  <version>3.7.0</version>
</dependency>
```

### 📄 Arquivos

| Arquivo              | Descrição                                           |
|----------------------|-----------------------------------------------------|
| `ProducerSeguro.java` | Producer com `acks=all` e idempotência              |
| `ConsumerSeguro.java` | Consumer com `enable.auto.commit=false` e commit manual |

### ▶️ Compilar e Executar

```bash
javac -cp kafka-clients-3.7.0.jar:. ProducerSeguro.java
java -cp kafka-clients-3.7.0.jar:. ProducerSeguro

javac -cp kafka-clients-3.7.0.jar:. ConsumerSeguro.java
java -cp kafka-clients-3.7.0.jar:. ConsumerSeguro
```

> Ajuste o caminho do JAR `kafka-clients` conforme o seu ambiente.

---

## ✅ Garantia de entrega estilo SQS

Para garantir que uma mensagem só seja considerada "entregue" após o processamento:

- Producer:
  - `acks=all`
  - `enable.idempotence=true`
- Consumer:
  - `enable.auto.commit=false`
  - Commit manual com `commit()` somente após sucesso
- Tópico com 1 partição garante ordem e entrega sequencial
- Kafka redeliverá a mensagem se não houver commit

---

## 📚 Referências

- Apache Kafka: [https://kafka.apache.org/documentation](https://kafka.apache.org/documentation)
- Confluent Kafka Python: [https://docs.confluent.io/platform/current/clients/confluent-kafka-python](https://docs.confluent.io/platform/current/clients/confluent-kafka-python)
- Kafka Java Client Configs: [https://kafka.apache.org/documentation/#consumerconfigs](https://kafka.apache.org/documentation/#consumerconfigs)
- Kafdrop: [https://github.com/obsidiandynamics/kafdrop](https://github.com/obsidiandynamics/kafdrop)

---
