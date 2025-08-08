import os
from database import User , MessageHistr, InitDatabase
from dotenv import load_dotenv
from gigachat import GigaChat
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GIGACHAT_TOKEN = os.getenv("GIGACHAT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
giga = GigaChat(credentials=GIGACHAT_TOKEN, verify_ssl_certs=False)
session = InitDatabase(DATABASE_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    try:

        db_user = session.query(User).filter_by(telegram_id = user.id)

        if not db_user:
            new_user_form = User(
                telegram_id = user.id,
                username = user.username,
                first_name = user.first_name,
                last_name = user.last_name or ""
            )
        
            session.add(new_user_form)
            session.commit()

            await update.message.reply_text(f"Привет , {user.username}. Я нейросеть созданная Артемом , задай мне вопрос и я на него отвечу !")
        elif db_user:
            await update.message.reply_text(f"Снова привет , {user.username}. Я нейросеть созданная Артемом , задай мне вопрос и я на него отвечу !")
    except Exception as ex:
        await update.message.reply_text(f'Извините , произошла ошибка , мы уже работаем над ней. Ошибка : {ex}')



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_message = update.message.text
    user_text = update.message.text
    chat_id = update.effective_chat.id

    try:

        newMessage = MessageHistr(
            user_id = user.id,
            message_text = user_text
        )
        
        session.add(newMessage)
        session.commit()

        
        processing_message = await update.message.reply_text ("Секундочку ⏳")

        await context.bot.send_chat_action(chat_id = chat_id,
                                       action = ChatAction.TYPING) # Работает с багом! (Продолжает "печатает даже после отправки разельтата")
        
        response = giga.chat(user_message)
        neuro_reply = response.choices[0].message.content
        

        if processing_message:
            await context.bot.edit_message_text(chat_id = chat_id,
                                            message_id = processing_message.id,
                                            text = neuro_reply)


    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен...")
    app.run_polling()
