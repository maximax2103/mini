import logging
import json # Добавлено для обработки JSON данных
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import config
import storage # Добавлено для работы с хранилищем пользователей

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
    keyboard.add(types.KeyboardButton("🎮 Играть", web_app=types.WebAppInfo(url="https://maximax2103.github.io/mini/")))
    
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

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    logger.info(f"Получены данные от Web App от пользователя {message.from_user.id}: {message.web_app_data.data}")
    
    # Здесь вы можете обработать данные, например, обновить количество попыток пользователя
    data = json.loads(message.web_app_data.data)
    if data['event'] == 'game_won':
        attempts_used = data['attemptsUsed']
        user = storage.get_user(message.from_user.id)
        if user:
            # Предполагаем, что у пользователя есть поле 'attempts'
            # Если его нет, вам нужно будет добавить его в storage.py и при создании пользователя
            current_attempts = user.get('attempts', 0) # Получаем текущие попытки, по умолчанию 0
            user['attempts'] = current_attempts - attempts_used
            storage.update_user(user['telegram_id'], attempts=user['attempts'])
            await message.answer(f"🎉 Вы выиграли в игре и использовали {attempts_used} попыток! У вас осталось {user['attempts']} попыток.")
        else:
            await message.answer("❌ Ошибка: Пользователь не найден.")

    await message.answer("✅ Данные от игры получены и обработаны!")

