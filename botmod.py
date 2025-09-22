from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import re

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Регулярное выражение для обнаружения ссылок
URL_REGEX = re.compile(r'(https?://\S+)')

# Список запретных слов
FORBIDDEN_WORDS = ['пидр', 'хуй']  # Замените на свои слова

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def filter_messages(message: types.Message):
    # Проверка на наличие ссылки
    if URL_REGEX.search(message.text):
        await delete_and_notify(message)
        return

    # Проверка на наличие запретных слов
    for word in FORBIDDEN_WORDS:
        if word in message.text.lower():  # Приводим текст к нижнему регистру для нечувствительности к регистру
            await delete_and_notify(message)
            return

async def delete_and_notify(message: types.Message):
    try:
        await message.delete()
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


