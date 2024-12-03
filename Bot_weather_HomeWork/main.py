import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand, Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import requests
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Определяем состояние для ожидания ввода города
class WeatherState(StatesGroup):
    waiting_for_city = State()

# Функция для получения погоды
def get_weather(city):
    api_key = "b7d03c1c5c46a905a488af89efc4343f"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = round(data['main']['temp'])
        description = data['weather'][0]['description'].capitalize()
        return f"Погода в {city}: {temp}°C, {description}."
    else:
        return "Не удалось получить погоду. Проверьте название города."

# Команда /start
@dp.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет! Я бот, который знает погоду в любом городе мира!. Напишите /weather или выберите в меню, чтобы узнать погоду.")

# Команда /help
@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer("Я могу:\n/start - приветствие\n/help - помощь\n/weather - узнать погоду.")

# Команда /weather
@dp.message(Command('weather'))
async def weather_command(message: Message, state: FSMContext):
    await message.answer("Напишите название города, чтобы узнать погоду.")
    await state.set_state(WeatherState.waiting_for_city)

# Обработка ввода города
@dp.message(StateFilter(WeatherState.waiting_for_city))
async def process_city(message: Message, state: FSMContext):
    city = message.text
    weather_info = get_weather(city)
    await message.answer(weather_info)
    await state.clear()

# Устанавливаем команды для меню
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="weather", description="Узнать погоду")
    ]
    await bot.set_my_commands(commands)

# Запуск бота
async def main():
    await set_commands(bot)  # Устанавливаем команды в меню
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
