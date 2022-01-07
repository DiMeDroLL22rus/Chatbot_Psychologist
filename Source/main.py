"""Телеграм чат-бот психолог PsylogBot."""
import os
import logging
from google.cloud import dialogflow
from aiogram import Bot, Dispatcher, executor, types
from config import telegram_token

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'psylogbot.json'

session_client = dialogflow.SessionsClient()

PROJECT_ID = 'psylogbot-mipg'
SESSION_ID = 'sessions'
LANGUAGE_CODE = 'ru'
SESSION = session_client.session_path(PROJECT_ID, SESSION_ID)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=telegram_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Реагирование на команду старт."""
    await bot.send_message(message.from_user.id, """
Давай пообщаемся?
Напиши "Привет!"

Автор: @dimedroll22rus
""")


@dp.message_handler()
async def psylogbot_dialogflow(message: types.Message):
    """Использование Dialogflow"""
    text_input = dialogflow.TextInput(text=message.text,
                                      language_code=LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=SESSION,
                                            query_input=query_input)
    if response.query_result.fulfillment_text:
        await bot.send_message(message.from_user.id,
                               response.query_result.fulfillment_text)
    else:
        await bot.send_message(message.from_user.id, "Я тебя не понимаю")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
