import telebot
from dotenv import load_dotenv
import os
from gtm import get_image_class

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start','help'])
def start_command(message):
    chat_id = message.chat.id

    text = (f'Привет,{message.from_user.first_name}!\n\n'
            'Я-бот, который класифицирует изображения по классам\n')if message.text == '/start'else ''
    
    text += 'отправь мне фотографию фрукта и я постараюсь её определить к какому фрукту относится данное фото'
    
    bot.send_message(chat_id,text)

@bot.message_handler(content_types = ['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    if not message.photo:
        return bot.send_message(chat_id,'Ты не загрузил фото!')
    
    temp_message = bot.send_message(chat_id,'Подожди идёт обработка фото...')
    file_info = bot.get_file(message.photo [-1].file_id)
    file_path = file_info.file_path
    file_name = file_path.split('/')[-1]

    downloaded_file = bot.download_file(file_path)
    with open (f'images/{file_name}','wb') as new_file:
        new_file.write(downloaded_file)

    class_name,percentage_probability = get_image_class(f'images/{file_name}')
    bot.delete_message(chat_id,temp_message.id)
    bot.send_message(chat_id,f'С вероятноти{percentage_probability}%на фото { class_name.lower()}')

    if percentage_probability >= 75:
        os.remove(f'images'/{file_name})

bot.infinity_polling()