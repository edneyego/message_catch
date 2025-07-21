import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import java.util.Properties;

public class ProducerSeguro {
    public static void main(String[] args) {
        String topico = "fila-segura-java";

        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.ACKS_CONFIG, "all");
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");

        Producer<String, String> producer = new KafkaProducer<>(props);

        String mensagem = "{\"evento\": \"umidade\", \"valor\": 80}";

        ProducerRecord<String, String> record = new ProducerRecord<>(topico, null, mensagem);

        producer.send(record, (metadata, exception) -> {
            if (exception == null) {
                System.out.printf("📤 Enviado: %s → %s@%d%n", mensagem, metadata.topic(), metadata.partition());
            } else {
                System.out.printf("❌ Erro: %s%n", exception.getMessage());
            }
        });

        producer.flush();
        producer.close();
    }
}