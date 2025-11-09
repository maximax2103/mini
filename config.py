import os
from dotenv import load_dotenv

# Загрузить переменные из .env файла (также пробуем 23.env как резерв)
load_dotenv()  # Пробуем .env
load_dotenv('23.env')  # Если .env нет, пробуем 23.env

# Токен бота Telegram
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "8480030670:AAGET1e5lFJQpAd6WXk0T9OjLPCVmOh1tUg")

# Настройки реферальной системы
REFERRAL_BONUS: int = 50  # Бонус за приглашение друга (звёзды)
REFERRAL_ACTIVITY_BONUS: int = 20  # Бонус за активность реферала

# Настройки заданий
MIN_TASK_REWARD: int = 10  # Минимальная награда за задание
MAX_TASK_REWARD: int = 10000  # Максимальная награда за задание

# Настройки модерации
AUTO_APPROVE_THRESHOLD: int = 5  # Количество успешных выполнений для автоподтверждения
CAPTCHA_REQUIRED: bool = True  # Требовать капчу для новых пользователей

# Настройки вывода
MIN_WITHDRAWAL: int = 100  # Минимальная сумма для вывода (звёзды)
