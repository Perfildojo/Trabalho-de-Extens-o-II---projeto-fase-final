import pytest
from unittest.mock import AsyncMock, patch
from bot.handlers import bairro, ocorrencia
from telegram import Update, Message, Chat

@pytest.fixture
def mock_update():
    update = AsyncMock(spec=Update)
    update.message = AsyncMock(spec=Message)
    update.message.text = "Vergel do Lago"
    update.message.chat = AsyncMock(spec=Chat)
    update.message.chat.id = 123
    return update

@pytest.mark.asyncio
async def test_bairro_valido(mock_update):
    context = AsyncMock()
    result = await bairro(mock_update, context)
    assert result == 1  # OCORRENCIA state
    context.user_data.__setitem__.assert_called_with("bairro", "Vergel do Lago")

@pytest.mark.asyncio
async def test_ocorrencia_valida(mock_update):
    mock_update.message.text = "Roubo"
    context = AsyncMock()
    context.user_data = {}
    
    result = await ocorrencia(mock_update, context)
    assert result == 2  # RUA state
    assert context.user_data["ocorrencia"] == "Roubo"
    