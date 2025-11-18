# Инструкция: Как получить и прописать Bot Token

## Шаг 1: Получение Bot Token

1. Откройте Telegram и найдите бота [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot` (если бот еще не создан) или `/token` (если бот уже создан)
3. Следуйте инструкциям BotFather:
   - Если создаете нового бота: введите имя и username
   - Если бот уже создан: выберите нужного бота из списка
4. BotFather выдаст вам токен, который выглядит примерно так:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
   ```
5. **Скопируйте этот токен** - он понадобится в следующем шаге

## Шаг 2: Прописать Token в .env файл

### Вариант 1: Через текстовый редактор

1. Откройте файл `.env` в корне проекта (если его нет, создайте на основе `.env.example`)
2. Найдите строку:
   ```env
   BOT_TOKEN=your_bot_token_here
   ```
3. Замените `your_bot_token_here` на ваш реальный токен:
   ```env
   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
   ```
4. Сохраните файл

### Вариант 2: Через терминал (macOS/Linux)

```bash
# Перейдите в папку проекта
cd /Users/mitya/CursorAI/TGbotKasheeva_v3

# Создайте .env файл если его нет
cp .env.example .env

# Откройте файл в редакторе
nano .env
# или
vim .env
# или
code .env  # если используете VS Code
```

Затем замените `your_bot_token_here` на ваш токен.

### Вариант 3: Через команду echo (быстрый способ)

```bash
# Замените YOUR_TOKEN_HERE на ваш реальный токен
echo "BOT_TOKEN=YOUR_TOKEN_HERE" > .env
echo "MODERATOR_ID=your_telegram_id" >> .env
echo "CHANNEL_USERNAME=doctor_kashcheeva" >> .env
```

## Пример заполненного .env файла:

```env
# Telegram Bot Token (получить у @BotFather)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890

# ID модератора в Telegram (для отправки ответов)
MODERATOR_ID=123456789

# Email для отправки Excel файлов с ответами (опционально)
EMAIL_TO=your_email@example.com

# SMTP настройки для отправки email (опционально)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Канал для проверки подписки (без символа @)
CHANNEL_USERNAME=doctor_kashcheeva
```

## Важные моменты:

⚠️ **Безопасность:**
- Никогда не публикуйте `.env` файл в Git (он уже в `.gitignore`)
- Не делитесь токеном с другими людьми
- Если токен скомпрометирован, создайте новый через `/revoke` в BotFather

⚠️ **Формат токена:**
- Токен должен быть в формате: `числа:буквы_и_цифры`
- Не добавляйте пробелы или кавычки вокруг токена
- Не добавляйте символ `@` перед токеном

## Проверка правильности настройки:

После заполнения `.env` файла, запустите бота:

```bash
python bot.py
```

Если токен правильный, вы увидите:
```
Бот запущен!
```

Если токен неправильный, вы увидите ошибку:
```
aiogram.exceptions.TelegramUnauthorizedError: Unauthorized
```

В этом случае проверьте:
1. Правильность токена в `.env`
2. Что токен скопирован полностью (без пробелов в начале/конце)
3. Что файл `.env` находится в корне проекта

## Дополнительные настройки:

После настройки `BOT_TOKEN`, также нужно заполнить:

1. **MODERATOR_ID** - ваш Telegram ID (узнайте у [@userinfobot](https://t.me/userinfobot))
2. **CHANNEL_USERNAME** - уже указан как `doctor_kashcheeva`
3. **EMAIL_TO** и **SMTP_*** - опционально, для отправки Excel файлов на email

## Готово!

После заполнения `BOT_TOKEN` в `.env` файле, бот готов к запуску! 🚀

