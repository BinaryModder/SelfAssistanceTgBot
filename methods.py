import os
from dotenv import load_dotenv
from models import User , MessageHistr
from database import InitDatabase
from gigachat import GigaChat



load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
GIGACHAT_TOKEN = os.getenv("GIGACHAT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")



session = InitDatabase(DATABASE_URL)
giga = GigaChat(credentials=GIGACHAT_TOKEN, verify_ssl_certs=False)



async def user_registration(user_id , username , first_name , last_name) :
    
    try:
        query = session.query(User).filter(User.user_id == user_id).first()
        
        if query is None :
            new_user_form = User(
                user_id = user_id,
                username = username,
                first_name =first_name,
                last_name = last_name,
                responses = 20
            )
            session.add(new_user_form)
            session.commit()

            return True #   Регистрация прошла успешно

        elif query is not None :
            
            return False #   Регистрация не требуется 

    except Exception as ex:
        print(ex)


async def save_user_message(user_id , user_text) :

    try:

         newMessage = MessageHistr(
            user_id = user_id,
            message_text = user_text
         )
         session.add(newMessage)
         session.commit()

    except Exception as ex:
         print(ex)
        


async def sent_neuro_result(user_id , user_message) -> str:

    try:
         query = session.query(User).filter(User.user_id == user_id).first()
         
         if (query is not None and query.responses >= 1) :
            

                query.responses -= 1
                session.commit()


                response = giga.chat(user_message)
                return response.choices[0].message.content
            





         else: return 'Ваш запас запросов исчерпан'




    except Exception as ex:
        print(ex)
        return 'none'

