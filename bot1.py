import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Defina seu Token, Canal e Grupo
TOKEN = '7399832505:AAGG9WfCeFkvGhnZi5w75uGFb_LEDdqjUO0'  # Substitua pelo token do seu bot
CHANNEL_ID = '-1002496076026'  # Substitua pelo ID do seu canal (ID numérico)
GROUP_ID = '-1002434125800'  # Substitua pelo ID do seu grupo (ID numérico)

# Habilitar logs para ver o que está acontecendo
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Função para capturar qualquer tipo de mensagem (texto, foto, vídeo, etc.)
async def forward_to_group(update: Update, context: CallbackContext):
    try:
        # Verifica se a atualização contém uma mensagem efetiva e se ela vem do canal
        if update.effective_message and update.effective_message.chat.id == int(CHANNEL_ID):
            print(f"Mensagem recebida do canal com ID: {update.effective_message.chat.id}")

            # Verifica o tipo de conteúdo da mensagem (texto, foto, vídeo, etc.)
            if update.effective_message.text:
                message = update.effective_message.text  # Captura o texto da mensagem
                await context.bot.send_message(chat_id=GROUP_ID, text=message)
                print(f"Mensagem de texto enviada para o grupo: {message}")
            elif update.effective_message.photo:
                # Captura a foto e envia para o grupo
                photo = update.effective_message.photo[-1].file_id  # Pegando a maior resolução da foto
                await context.bot.send_photo(chat_id=GROUP_ID, photo=photo)
                print(f"Foto enviada para o grupo.")
            elif update.effective_message.video:
                # Captura o vídeo e envia para o grupo
                video = update.effective_message.video.file_id
                await context.bot.send_video(chat_id=GROUP_ID, video=video)
                print(f"Vídeo enviado para o grupo.")
            else:
                print("Tipo de mensagem não suportado.")
        else:
            print(
                f"A mensagem não veio do canal especificado. ID do chat: {update.effective_message.chat.id if update.effective_message else 'Não há mensagem'}")
    except Exception as e:
        logger.error(f"Erro ao tentar repostar a mensagem: {e}")


# Função para iniciar o bot
def main():
    # Criação do Application com o seu token
    application = Application.builder().token(TOKEN).build()

    # Registra um handler para pegar qualquer tipo de mensagem do canal
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO, forward_to_group))

    # Inicia o bot (sem asyncio.run()!)
    application.run_polling()


if __name__ == '__main__':
    main()  # Chama diretamente a função main
