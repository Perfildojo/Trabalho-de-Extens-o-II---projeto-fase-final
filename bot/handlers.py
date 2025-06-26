from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from bot.database import salvar_ocorrencia
from bot.config import BAIRROS, OCORRENCIAS, OPCOES_IMAGEM
from bot.validators import validar_bairro, validar_ocorrencia
import logging

# Configuração de logging
logger = logging.getLogger(__name__)

# Estados da conversa
BAIRRO, OCORRENCIA, RUA, IMAGEM = range(4)

async def start(update: Update, context: CallbackContext) -> int:
    """Inicia a conversa e pede o bairro"""
    try:
        keyboard = ReplyKeyboardMarkup(BAIRROS, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Olá! Eu sou o bot Mapa do Medo!\nQual o bairro da ocorrência?",
            reply_markup=keyboard
        )
        return BAIRRO
    except Exception as e:
        logger.error(f"Erro no handler start: {e}")
        await update.message.reply_text("❌ Ocorreu um erro. Tente novamente mais tarde.")
        return ConversationHandler.END

async def bairro(update: Update, context: CallbackContext) -> int:
    """Recebe o bairro e pede o tipo de ocorrência"""
    try:
        bairro = validar_bairro(update.message.text)
        context.user_data["bairro"] = bairro
        
        keyboard = ReplyKeyboardMarkup(OCORRENCIAS, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Qual a ocorrência?", reply_markup=keyboard)
        return OCORRENCIA
        
    except ValueError as e:
        await update.message.reply_text(f"❌ {str(e)}\nPor favor, selecione um bairro válido.")
        return BAIRRO
    except Exception as e:
        logger.error(f"Erro no handler bairro: {e}")
        await update.message.reply_text("❌ Ocorreu um erro. Voltando ao início.")
        return await start(update, context)

async def ocorrencia(update: Update, context: CallbackContext) -> int:
    """Recebe o tipo de ocorrência e pede a rua"""
    try:
        ocorrencia = validar_ocorrencia(update.message.text)
        context.user_data["ocorrencia"] = ocorrencia
        
        await update.message.reply_text("Digite o nome da rua onde ocorreu o incidente:")
        return RUA
        
    except ValueError as e:
        await update.message.reply_text(f"❌ {str(e)}\nPor favor, selecione uma ocorrência válida.")
        return OCORRENCIA
    except Exception as e:
        logger.error(f"Erro no handler ocorrencia: {e}")
        await update.message.reply_text("❌ Ocorreu um erro. Voltando ao início.")
        return await start(update, context)

async def rua(update: Update, context: CallbackContext) -> int:
    """Recebe a rua e pergunta sobre imagem"""
    try:
        rua = update.message.text.strip()
        if not rua:
            await update.message.reply_text("❌ Por favor, informe o nome da rua.")
            return RUA
            
        context.user_data["rua"] = rua
        keyboard = ReplyKeyboardMarkup(OPCOES_IMAGEM, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("Deseja enviar uma imagem da ocorrência?", reply_markup=keyboard)
        return IMAGEM
        
    except Exception as e:
        logger.error(f"Erro no handler rua: {e}")
        await update.message.reply_text("❌ Ocorreu um erro. Voltando ao início.")
        return await start(update, context)

async def salvar_imagem(update: Update, context: CallbackContext) -> int:
    """Processa a imagem (se enviada) e salva os dados"""
    try:
        if update.message.text == "Não tenho imagem":
            context.user_data["imagem"] = None
        else:
            # Verifica se realmente é uma imagem
            if not update.message.photo:
                await update.message.reply_text("❌ Por favor, envie uma imagem válida.")
                return IMAGEM
                
            photo_file = await update.message.photo[-1].get_file()
            caminho_imagem = f"data/images/{photo_file.file_id}.jpg"
            await photo_file.download_to_drive(caminho_imagem)
            context.user_data["imagem"] = caminho_imagem
        
        await finalizar_registro(update, context)
        return ConversationHandler.END
        
    except Exception as e:
        logger.error(f"Erro no handler salvar_imagem: {e}")
        await update.message.reply_text("❌ Ocorreu um erro ao processar a imagem. Tente novamente.")
        return IMAGEM

async def finalizar_registro(update: Update, context: CallbackContext) -> None:
    """Finaliza o registro e salva os dados"""
    try:
        dados = {
            "bairro": context.user_data.get("bairro"),
            "ocorrencia": context.user_data.get("ocorrencia"),
            "rua": context.user_data.get("rua"),
            "imagem": context.user_data.get("imagem")
        }
        
        # Verificação final dos dados
        if not dados["bairro"] or not dados["ocorrencia"]:
            raise ValueError("Dados incompletos")
            
        salvar_ocorrencia(**dados)
        await update.message.reply_text(
            "✅ Registro concluído! Sua contribuição ajudará a melhorar a segurança no bairro."
        )
        
    except Exception as e:
        logger.error(f"Erro no finalizar_registro: {e}")
        await update.message.reply_text(
            "❌ Falha ao salvar o registro. Por favor, tente novamente mais tarde."
        )
        raise

async def cancelar(update: Update, context: CallbackContext) -> int:
    """Cancela a conversa"""
    try:
        await update.message.reply_text("Operação cancelada. Use /start para começar novamente.")
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Erro no handler cancelar: {e}")
        return ConversationHandler.END