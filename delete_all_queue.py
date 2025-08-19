from confluent_kafka.admin import AdminClient
import sys
import time

BOOTSTRAP_SERVERS = "localhost:9092"


def deletar_todos_os_topicos():
    admin = AdminClient({"bootstrap.servers": BOOTSTRAP_SERVERS})

    # Lista todos os tópicos
    md = admin.list_topics(timeout=10)
    topicos = list(md.topics.keys())

    if not topicos:
        print("⚠️ Nenhum tópico encontrado no cluster.")
        return

    print(f"📋 Tópicos encontrados: {topicos}")

    # Atenção: por padrão o Kafka cria "__consumer_offsets" e outros internos
    topicos_para_deletar = [
        t for t in topicos if not t.startswith("__")
    ]

    if not topicos_para_deletar:
        print("⚠️ Nenhum tópico de usuário para deletar (apenas internos).")
        return

    print(f"🗑️ Deletando tópicos: {topicos_para_deletar}")

    fs = admin.delete_topics(topicos_para_deletar, operation_timeout=30)

    # Aguarda as futures terminarem
    for t, f in fs.items():
        try:
            f.result()  # vai levantar exceção se falhar
            print(f"✅ Tópico deletado: {t}")
        except Exception as e:
            print(f"❌ Falha ao deletar {t}: {e}")


if __name__ == "__main__":
    confirm = input(
        "⚠️ Isso vai DELETAR todos os tópicos do Kafka (exceto internos). Confirmar? (digite 'SIM'): "
    )
    if confirm.strip().upper() == "SIM":
        deletar_todos_os_topicos()
    else:
        print("❎ Operação cancelada.")
        sys.exit(0)
