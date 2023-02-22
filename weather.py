import requests
import asyncio
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ParseMode, InputTextMessageContent, \
    InlineQuery, InlineQueryResultArticle, InlineQueryResultPhoto
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import alive

API_TOKEN = '6294954320:AAEqMBxdPrOqsuxHJzYbDeAxlh8TYMCk68Y'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Показать погоду", callback_data='get_weather')
    keyboard.add(button)
    await message.answer("Привет! Я могу показать тебе погоду. Нажми на кнопку ниже.", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'get_weather')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите название города:")


@dp.message_handler()
async def process_message(message: types.Message):
    city_name = message.text

    msg = await message.reply("Ждите...")

    await asyncio.sleep(3)

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=ccf2c4fe8362482ec550fd4da455346f&units=metric&lang=ru'

    response = requests.get(url).json()

    if response['cod'] == 200:

        weather = response['weather'][0]['description']
        temperature = response['main']['temp']
        feels_like = response['main']['feels_like']
        humidity = response['main']['humidity']
        wind_speed = response['wind']['speed']
        message_text = f"🏙️ Сейчас в {city_name} {weather}.\n🌡️ Температура: {temperature}°C (ощущается как {feels_like}°C).\n💦 Влажность: {humidity}%.\n💨 Скорость ветра: {wind_speed} м/с."

        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Еще раз", callback_data='get_weather')
        keyboard.add(button)

        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=message_text,
                                    reply_markup=keyboard)
    else:
        message_text = "Не удалось получить данные о погоде."
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=message_text)

        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Еще раз", callback_data='get_weather')
        keyboard.add(button)

        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=message_text,
                                    reply_markup=keyboard)


alive.keep_alive()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
