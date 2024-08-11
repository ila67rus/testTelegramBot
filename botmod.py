from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import re

API_TOKEN = '7331998507:AAGPULwRv13Qx8PSQNxh9o8CJfX-ImfFHk4'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Регулярное выражение для обнаружения ссылок
URL_REGEX = re.compile(r'(https?://\S+)')

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def filter_links(message: types.Message):
    # Если сообщение содержит ссылку, удаляем его
    if URL_REGEX.search(message.text):
        try:
            await message.delete()
            # Отправляем уведомление в тот же чат
            
        except Exception as e:
            # Логируем ошибку, если произошла проблема
            print(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

