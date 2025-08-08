import os
from database import User , MessageHistr, InitDatabase
from dotenv import load_dotenv
from gigachat import GigaChat
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загрузка токенов
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GIGACHAT_TOKEN = os.getenv("GIGACHAT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

giga = GigaChat(credentials=GIGACHAT_TOKEN, verify_ssl_certs=False)
session = InitDatabase(DATABASE_URL)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        user_text = update.message.text

        newMessage = MessageHistr(
            user_id = user.id,
            message_text = user_text
        )
        
        session.add(newMessage)
        session.commit()


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

            await update.message.reply_text(f"Привет , {user.username}")
        elif db_user:
            await update.message.reply_text(f"Снова привет , {user.username}")
    except Exception as ex:
        await update.message.reply_text(f'Извините , произошла ошибка , мы уже работаем над ней. Ошибка : {ex}')



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = giga.chat(user_message)
        bot_reply = response.choices[0].message.content
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен...")
    app.run_polling()
