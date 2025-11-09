import time
import uuid

# Простое хранилище в памяти для пользователей, заданий, отчетов и транзакций
# В реальном приложении это будет заменено на базу данных (SQLite, PostgreSQL и т.д.)
users = {}
tasks = []
reports = []
transactions = []
withdrawals = []

# --- Функции для работы с пользователями ---
def create_user(telegram_id, username, first_name, last_name, referral_code_arg=None):
    if telegram_id not in users:
        referral_code = str(uuid.uuid4())[:8] # Генерация короткого реферального кода
        new_user = {
            'telegram_id': telegram_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'balance': 0,
            'total_completed': 0,
            'total_created': 0,
            'rating': 5.0,
            'is_verified': False,
            'referral_code': referral_code,
            'referred_by_id': None,
            'attempts': 5 # Начальное количество попыток для мини-игры
        }
        
        if referral_code_arg:
            referrer = next((u for u in users.values() 
                             if u['referral_code'] == referral_code_arg), None)
            if referrer:
                new_user['referred_by_id'] = referrer['telegram_id']
                # Можно добавить бонус рефереру здесь
        
        users[telegram_id] = new_user
    return users[telegram_id]

def get_user(telegram_id):
    return users.get(telegram_id)

def update_user(telegram_id, **kwargs):
    user = users.get(telegram_id)
    if user:
        user.update(kwargs)
        return True
    return False

# --- Функции для работы с заданиями (заглушки) ---
def create_task(**kwargs):
    task = {'id': len(tasks) + 1, 'status': 'active', 'current_executors': 0, **kwargs}
    tasks.append(task)
    return task

def get_task(task_id):
    return next((t for t in tasks if t['id'] == task_id), None)

def get_active_tasks(limit=10):
    return [t for t in tasks if t['status'] == 'active'][:limit]

def take_task(task_id, executor_id):
    task = get_task(task_id)
    if task and task['current_executors'] < task['max_executors']:
        task['current_executors'] += 1
        return True
    return False

def get_user_task_executions(user_id, task_id):
    # Заглушка: в реальной БД это будет отдельная таблица
    return None # Пока нет логики для отслеживания выполнения заданий

# --- Функции для работы с отчетами (заглушки) ---
def create_report(**kwargs):
    report = {'id': len(reports) + 1, 'status': 'pending', **kwargs}
    reports.append(report)
    return report

def get_pending_reports(limit=10):
    return [r for r in reports if r['status'] == 'pending'][:limit]

def approve_report(report_id, admin_id):
    report = next((r for r in reports if r['id'] == report_id), None)
    if report and report['status'] == 'pending':
        report['status'] = 'approved'
        # Добавить логику начисления награды исполнителю и списания у заказчика
        return True
    return False

def reject_report(report_id, admin_id):
    report = next((r for r in reports if r['id'] == report_id), None)
    if report and report['status'] == 'pending':
        report['status'] = 'rejected'
        return True
    return False

# --- Функции для транзакций и вывода (заглушки) ---
def add_transaction(user_id, amount, type, description, task_id=None):
    transaction = {
        'id': len(transactions) + 1,
        'user_id': user_id,
        'amount': amount,
        'type': type,
        'description': description,
        'task_id': task_id,
        'timestamp': time.time()
    }
    transactions.append(transaction)
    return transaction

def create_withdrawal(user_id, amount, payment_details):
    withdrawal = {
        'id': len(withdrawals) + 1,
        'user_id': user_id,
        'amount': amount,
        'payment_details': payment_details,
        'status': 'pending',
        'timestamp': time.time()
    }
    withdrawals.append(withdrawal)
    return withdrawal

# --- Вспомогательные функции (заглушки) ---
def get_top_executors(limit=10):
    # Заглушка для демонстрации
    return sorted([u for u in users.values() if u.get('total_completed', 0) > 0], 
                  key=lambda x: x.get('total_completed', 0), reverse=True)[:limit]

def get_top_clients(limit=10):
    # Заглушка для демонстрации
    return sorted([u for u in users.values() if u.get('total_created', 0) > 0], 
                  key=lambda x: x.get('total_created', 0), reverse=True)[:limit]
