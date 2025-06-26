from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from bot.handlers import start, bairro, ocorrencia, rua, salvar_imagem, cancelar
from bot.config import TOKEN
from bot.database import inicializar_banco
import logging
from pathlib import Path

# Configuração de estados
BAIRRO, OCORRENCIA, RUA, IMAGEM = range(4)

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Inicialização do banco com tratamento de erro
        logger.info("Inicializando banco de dados...")
        inicializar_banco()
        
        # Criação da aplicação
        logger.info("Criando aplicação do bot...")
        app = Application.builder().token(TOKEN).build()
        
        # Configuração do ConversationHandler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                BAIRRO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bairro)],
                OCORRENCIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, ocorrencia)],
                RUA: [MessageHandler(filters.TEXT & ~filters.COMMAND, rua)],
                IMAGEM: [
                    MessageHandler(filters.PHOTO, salvar_imagem),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, salvar_imagem)
                ],
            },
            fallbacks=[CommandHandler("cancel", cancelar)],
        )
        
        app.add_handler(conv_handler)
        
        # Adiciona handler para erros
        app.add_error_handler(error_handler)
        
        logger.info("Bot iniciado com sucesso. Aguardando mensagens...")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"Falha ao iniciar o bot: {e}")
        raise

async def error_handler(update: object, context) -> None:
    """Log de erros e notificação ao usuário"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    if update and hasattr(update, 'message'):
        await update.message.reply_text(
            "⚠️ Ocorreu um erro inesperado. "
            "Por favor, tente novamente mais tarde."
        )

if __name__ == "__main__":
    main()