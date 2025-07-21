import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.serialization.StringDeserializer;
import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class ConsumerSeguro {
    public static void main(String[] args) {
        String topico = "fila-segura-java";

        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "grupo-seguro-java");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Collections.singletonList(topico));

        System.out.println("⏳ Aguardando mensagens...");

        try {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(10));
            for (ConsumerRecord<String, String> record : records) {
                System.out.printf("📥 Recebido: %s%n", record.value());

                // Simular processamento
                Thread.sleep(1000);

                // Confirmar apenas após sucesso
                consumer.commitSync(Collections.singletonMap(
                        new TopicPartition(record.topic(), record.partition()),
                        new OffsetAndMetadata(record.offset() + 1)
                ));
                System.out.println("✅ Mensagem comitada com sucesso.");
            }
        } catch (Exception e) {
            System.err.println("❌ Erro: " + e.getMessage());
        } finally {
            consumer.close();
        }
    }
}