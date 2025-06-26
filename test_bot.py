import pytest
from telegram import Update, Message, Chat, PhotoSize
from telegram.ext import CallbackContext
from bot.handlers import start, bairro, ocorrencia, rua, salvar_imagem
from bot.config import bairros, ocorrencias

# Mock de objetos do Telegram
@pytest.fixture
def update():
    update = Update(
        update_id=1,
        message=Message(
            message_id=1,
            chat=Chat(id=1, type="private"),
            text="",
        )
    )
    return update

@pytest.fixture
def context():
    return CallbackContext()

# Teste: Comando /start
async def test_start(update, context):
    update.message.text = "/start"
    result = await start(update, context)
    assert result == 0  # BAIRRO

# Teste: Seleção de bairro
async def test_bairro(update, context):
    update.message.text = "Vergel do Lago"
    context.user_data = {}
    result = await bairro(update, context)
    assert result == 1  # OCORRENCIA
    assert context.user_data["bairro"] == "Vergel do Lago"