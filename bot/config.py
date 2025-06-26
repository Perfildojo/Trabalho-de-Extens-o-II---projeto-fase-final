import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not os.getenv("TELEGRAM_TOKEN"):
    raise ValueError("Token do Telegram não configurado! Crie um arquivo .env")

TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_PATH = Path(os.getenv("DATABASE_PATH", "./data/relatos.db"))

BAIRROS = [["Vergel do Lago"], ["Benedito Bentes"]]

OCORRENCIAS = [
    ['Tiroteio'], ['Roubo'], ['Briga'], ['Assalto'], ['Agressão'],
    ['Feminicídio'], ['Homicídio'], ['Estupro'], ['Atropelamento'],
    ['Sequestro'], ['Outros']
]

OPCOES_IMAGEM = [["Enviar imagem"], ["Não tenho imagem"]]