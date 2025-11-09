import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Проверка токена перед инициализацией
if not config.BOT_TOKEN or len(config.BOT_TOKEN) < 10:
    logger.error("❌ ОШИБКА: Токен бота не установлен или слишком короткий!")
    logger.error("Проверьте токен в config.py или в файле .env")
    raise ValueError("Токен бота не установлен. Проверьте файл .env или config.py")

# Инициализация бота
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🎮 Играть", web_app=types.WebAppInfo(url="https://yourusername.github.io/telegram-mini-app/mini_app.html")))
    
    await message.answer("Привет! Нажми кнопку, чтобы запустить мини-приложение.", reply_markup=keyboard)


async def main():
    logger.info("Запуск мини-апп бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise
