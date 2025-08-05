from pydantic import BaseModel
from typing import Any


class Mensagem(BaseModel):
    topico: str
    dados: dict[str, Any]
