import os
from dotenv import load_dotenv

load_dotenv()  # Carrega o .env

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPICOS = os.getenv("KAFKA_TOPICOS", "").split(",")
