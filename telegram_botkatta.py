"""
ODDIY OB-HAVO BOTI
MUALLIF: KENJABOYEV SAMANDAR
API: OpenWeatherMap
"""

import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests
from typing import Dict, Any

load_dotenv()

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "8625938437:AAE9EZBreYUYS24iseeC_MNOSsoSj68vstc"
WEATHER_API_KEY = "8f0190e280b7ca0a214e84a4e6d50021"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
  


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_weather_data(city: str) -> Dict[str, Any]:
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'uz'
        }

        response = requests.get(WEATHER_API_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"API xatosi: {e}")
        return None


def format_weather_message(data: Dict[str, Any], city: str) -> str:
    if not data:
        return "❌ Ob-havo ma'lumotini olishda xatolik yuz berdi."

    temp = round(data['main']['temp'])
    feels_like = round(data['main']['feels_like'])
    description = data['weather'][0]['description'].capitalize()
    humidity = data['main']['humidity']
    wind_speed = round(data['wind']['speed'])

    if temp < 0:
        emoji = "❄️"
    elif temp < 10:
        emoji = "🥶"
    elif temp < 20:
        emoji = "☁️"
    elif temp < 30:
        emoji = "☀️"
    else:
        emoji = "🔥"

    message = f"""
{emoji} <b>{city.title()} shahri ob-havosi</b> {emoji}

🌡 <b>Harorat:</b> {temp}°C
🤔 <b>His qilinadi:</b> {feels_like}°C
☁️ <b>Holat:</b> {description}
💧 <b>Namlik:</b> {humidity}%
💨 <b>Shamol:</b> {wind_speed} m/s

🕐 <i>Yangilangan: hozir</i>
"""
    return message

@dp.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = """
👋 <b>Assalomu alaykum!</b>

Men ob-havo ma'lumotini beradigan botman! 🌍  

<b>📋 Buyruqlar:</b>

/weather <i>shahar_nomi</i> - Ob-havo ma'lumoti
/help - Yordam

<b>📌 Misol:</b>
<code>/weather Toshkent</code>
<code>/weather Samarqand</code>

Qaysi shahar ob-havosi kerak? 🤔
"""
    await message.answer(welcome_text, parse_mode="HTML")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
<b>Yordam bo'limi</b>

<b>Qanday foydalanish kerak?</b>

1 /weather buyrug'ini yozing
2 Bo'sh joy qoldiring
3 Shahar nomini kiriting

<b>Misol:</b>
<code>/weather Toshkent</code>

<b>Qo'llab-quvvatlanadigan shaharlar:</b>
- O'zbekiston shaharlari
- Jahon shaharlari
- Ingliz tilida yozing (Tashkent, Moscow, London)

<b>Muammo bormi?</b>
- Shahar nomini to'g'ri yozganingizni tekshiring
- Internet aloqangizni tekshiring

<b>Maslahat:</b>
Katta-kichik harflar muhim emas!
"""
    await message.answer(help_text, parse_mode="HTML")


@dp.message(Command("weather"))
async def cmd_weather(message: Message):
    try:
        command_parts = message.text.split(maxsplit=1)

        if len(command_parts) < 2:
            await message.answer(
                "❌ <b>Shahar nomini kiriting!</b>\n\n"
                "📌 <b>Misol:</b> <code>/weather Toshkent</code>",
                parse_mode="HTML"
            )
            return

        city = command_parts[1].strip()

        loading_msg = await message.answer(
            "⏳ Ma'lumot yuklanmoqda...",
            parse_mode="HTML"
        )

        weather_data = await get_weather_data(city)

        if weather_data and weather_data.get('cod') == 200:
            formatted_message = format_weather_message(weather_data, city)
            await loading_msg.edit_text(formatted_message, parse_mode="HTML")

        elif weather_data and str(weather_data.get('cod')) == '404':
            await loading_msg.edit_text(
                f"❌ <b>{city}</b> shahri topilmadi!\n\n"
                "📌 <b>Misol:</b> <code>/weather Tashkent</code>",
                parse_mode="HTML"
            )

        else:
            await loading_msg.edit_text(
                "❌ <b>Xatolik yuz berdi!</b>\n\n"
                "Iltimos, qaytadan urinib ko'ring.",
                parse_mode="HTML"
            )

    except Exception as e:
        logging.error(f"Weather command xatosi: {e}")
        await message.answer(
            "❌ <b>Kutilmagan xatolik!</b>\n\n"
            "Keyinroq urinib ko‘ring.",
            parse_mode="HTML"
        )


@dp.message()
async def echo_message(message: Message):
    await message.answer(
        "🤔 <b>Men sizni tushunmadim.</b>\n\n"
        "Ob-havo uchun:\n"
        "<code>/weather shahar_nomi</code>\n\n"
        "Yordam: /help",
        parse_mode="HTML"
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Bot ishga tushdi...")
    await dp.start_pollin(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot to'xtatildi.")













































































