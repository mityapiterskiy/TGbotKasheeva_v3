# Деплой Telegram бота

## ⚠️ Важно: Vercel не подходит для Telegram ботов

Vercel предназначен для:
- Статических сайтов
- Serverless функций (короткие запросы)
- API endpoints

Telegram бот требует:
- **Постоянно работающий процесс** (long-running)
- Polling или Webhook для получения обновлений

## ✅ Рекомендуемые платформы для деплоя:

### 1. Railway (РЕКОМЕНДУЕТСЯ) - самый простой

**Плюсы:**
- Бесплатный тариф (500 часов/месяц)
- Простая настройка
- Автоматический деплой из GitHub
- Поддержка Python

**Как задеплоить:**
1. Зайдите на [railway.app](https://railway.app)
2. Войдите через GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Выберите ваш репозиторий
5. Railway автоматически определит Python
6. Добавьте переменные окружения (BOT_TOKEN, MODERATOR_ID и т.д.)
7. Готово!

### 2. Render

**Плюсы:**
- Бесплатный тариф
- Простая настройка
- Автоматический деплой

**Как задеплоить:**
1. Зайдите на [render.com](https://render.com)
2. "New" → "Web Service"
3. Подключите GitHub репозиторий
4. Настройки:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
5. Добавьте переменные окружения
6. Deploy

### 3. Heroku

**Плюсы:**
- Стабильная платформа
- Много документации

**Минусы:**
- Нет бесплатного тарифа (только платный)

### 4. DigitalOcean App Platform

**Плюсы:**
- Надежная платформа
- Хорошая производительность

**Минусы:**
- Платный (от $5/месяц)

## 📋 Что нужно для деплоя:

### 1. Создайте файл для деплоя

**Для Railway/Render/Heroku:**

Создайте `Procfile`:
```
worker: python bot.py
```

Или `runtime.txt` (для Heroku):
```
python-3.12.0
```

### 2. Переменные окружения

На платформе добавьте:
- `BOT_TOKEN` - токен бота
- `MODERATOR_ID` - ваш Telegram ID
- `CHANNEL_USERNAME` - doctor_kashcheeva
- `EMAIL_TO`, `SMTP_*` - опционально

### 3. requirements.txt

Уже создан ✅

## 🚀 Быстрый деплой на Railway:

1. Зайдите на [railway.app](https://railway.app)
2. Войдите через GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Выберите `TGbotKasheeva_v3`
5. Railway автоматически определит Python
6. В настройках проекта → "Variables" добавьте:
   ```
   BOT_TOKEN=ваш_токен
   MODERATOR_ID=ваш_id
   CHANNEL_USERNAME=doctor_kashcheeva
   ```
7. Готово! Бот запустится автоматически

## ⚙️ Альтернатива: Vercel с Webhook (сложно)

Если очень нужно использовать Vercel, можно переделать на webhook:

1. Создать serverless функцию для обработки webhook
2. Настроить webhook в Telegram
3. Но это требует переработки кода

**Не рекомендуется** - лучше использовать Railway или Render.

## 📝 Рекомендация:

**Используйте Railway** - это самый простой и бесплатный вариант для Telegram ботов.

