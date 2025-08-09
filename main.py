import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction

from methods import user_registration , sent_neuro_result, save_user_message

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    user = update.effective_user
    
    result = await user_registration(user_id = user.id, username = user.username , first_name = user.first_name , last_name = user.last_name)
    
    if result == True:
            await update.message.reply_text(f'Привет {user.username}, задай мне любой вопрос и я дам тебе на него ответ !')
    elif result == False:
            await update.message.reply_text(f'Снова привет {user.username}, задай мне любой вопрос и я дам тебе на него ответ !')



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) :
    user = update.effective_user
    chat_id = update.effective_chat.id
    

    try:

        await save_user_message(user_id = user.id , user_text = update.message.text)

        
        processing_message = await update.message.reply_text ("Секундочку ⏳")

        await context.bot.send_chat_action(chat_id = chat_id,
                                       action = ChatAction.TYPING) # Работает с багом! (Продолжает "печатает даже после отправки разельтата")
        
        neuro_reply = await sent_neuro_result(user_id = update.effective_user.id , user_message = update.message.text)
        

        if processing_message :
            await context.bot.edit_message_text(chat_id = chat_id,
                                            message_id = processing_message.id,
                                            text = neuro_reply)


    except Exception as e :
        await update.message.reply_text(f"Ошибка: {e}")

if __name__ == "__main__" :
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот запущен...")
    app.run_polling()
