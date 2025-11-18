# Хранение и отправка видео в Telegram Bot

## Как работает хранение видео на серверах Telegram

### 1. Система идентификаторов файлов

Telegram хранит все файлы (включая видео) на своих серверах и выдает уникальные идентификаторы:

- **`file_id`** — уникальный идентификатор файла для конкретного бота
  - Может использоваться для повторной отправки без повторной загрузки
  - Может изменяться при переотправке файла другим ботом
  - Формат: строка вида `BAACAgIAAxkBAAIBY2Z...` (пример)

- **`file_unique_id`** — постоянный уникальный идентификатор файла
  - Не изменяется при переотправке
  - Используется для отслеживания одного и того же файла
  - Формат: строка вида `AgADBAAC` (пример)

- **`file_path`** — путь к файлу на серверах Telegram
  - Используется для скачивания файла через Bot API
  - Доступен только для файлов, отправленных боту

### 2. Преимущества хранения на серверах Telegram

✅ **Не нужно хранить файлы локально** — Telegram хранит все на своих серверах  
✅ **Быстрая отправка** — отправка по `file_id` мгновенная, без загрузки  
✅ **Экономия трафика** — не нужно загружать файл каждый раз  
✅ **Надежность** — Telegram обеспечивает доступность файлов  

### 3. Ограничения

⚠️ **Размер файла**: до 50 МБ для обычных ботов, до 2 ГБ для ботов с премиум-подпиской  
⚠️ **Срок хранения**: файлы хранятся неограниченно долго, но `file_id` может стать недействительным при переотправке  
⚠️ **Доступность**: файл должен быть отправлен боту хотя бы один раз  

## Процесс получения file_id

### Шаг 1: Загрузка видео боту

1. Откройте Telegram и найдите вашего бота
2. Отправьте видео файл боту в личные сообщения
3. Видео будет сохранено на серверах Telegram

### Шаг 2: Получение file_id

Используйте скрипт `get_video_id.py`:

```bash
python get_video_id.py
```

Затем отправьте видео боту. Скрипт выведет `file_id` в консоль и отправит его вам в сообщении.

### Шаг 3: Сохранение file_id в структуре бота

Скопируйте полученный `file_id` и вставьте в `bot_structure.json`:

```json
{
  "lessons": [
    {
      "id": 1,
      "title": "Урок 1",
      "description": "Описание урока",
      "video_file_id": "BAACAgIAAxkBAAIBY2Z...",  // ← Вставьте сюда file_id
      "tags": ["психология", "терапия"],
      "next_lesson": 2
    }
  ]
}
```

## Отправка видео пользователю

### Базовый пример

```python
from aiogram import Bot
from aiogram.types import Message

bot = Bot(token="YOUR_BOT_TOKEN")

# Отправка видео по file_id
await bot.send_video(
    chat_id=user_id,
    video="BAACAgIAAxkBAAIBY2Z...",  # file_id
    caption="Описание видео"
)
```

### Отправка с тегами (hashtags)

```python
tags = ["психология", "терапия", "изменения"]
hashtags = ' '.join([f"#{tag.replace(' ', '_')}" for tag in tags])

caption = f"""📹 Название видео

Описание видео

{hashtags}"""

await bot.send_video(
    chat_id=user_id,
    video=video_file_id,
    caption=caption
)
```

### Отправка с клавиатурой

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(
        text="Следующий урок",
        callback_data="lesson_2"
    )]
])

await bot.send_video(
    chat_id=user_id,
    video=video_file_id,
    caption="Описание видео",
    reply_markup=keyboard
)
```

## Альтернативные способы отправки видео

### 1. Отправка по URL (для публичных видео)

```python
await bot.send_video(
    chat_id=user_id,
    video="https://example.com/video.mp4",  # Публичный URL
    caption="Описание"
)
```

⚠️ **Ограничение**: URL должен быть публично доступным и Telegram должен иметь возможность его скачать.

### 2. Отправка из локального файла

```python
from aiogram.types import FSInputFile

video_file = FSInputFile("path/to/video.mp4")

await bot.send_video(
    chat_id=user_id,
    video=video_file,
    caption="Описание"
)
```

⚠️ **Не рекомендуется**: файл будет загружаться каждый раз, что медленно и расходует трафик.

### 3. Отправка из байтов

```python
from aiogram.types import BufferedInputFile

with open("video.mp4", "rb") as f:
    video_bytes = f.read()

video_file = BufferedInputFile(
    file=video_bytes,
    filename="video.mp4"
)

await bot.send_video(
    chat_id=user_id,
    video=video_file,
    caption="Описание"
)
```

## Структура данных урока с видео

```json
{
  "id": 1,
  "title": "Название урока",
  "description": "Подробное описание урока",
  "video_file_id": "BAACAgIAAxkBAAIBY2Z...",  // file_id от Telegram
  "tags": [                                    // Теги для подписи
    "психология",
    "терапия",
    "изменения"
  ],
  "next_lesson": 2                             // ID следующего урока
}
```

## Обработка ошибок

Всегда обрабатывайте возможные ошибки при отправке видео:

```python
try:
    await message.answer_video(
        video_file_id,
        caption=caption,
        reply_markup=keyboard
    )
except Exception as e:
    # Логируем ошибку
    print(f"Ошибка отправки видео: {e}")
    
    # Отправляем пользователю понятное сообщение
    await message.answer(
        "⚠️ Произошла ошибка при отправке видео. "
        "Пожалуйста, попробуйте позже или свяжитесь с администратором."
    )
```

## Рекомендации

1. **Используйте file_id** — это самый быстрый и эффективный способ
2. **Сохраняйте file_id в конфигурации** — не храните файлы локально
3. **Добавляйте теги** — это помогает пользователям находить контент
4. **Обрабатывайте ошибки** — всегда предусматривайте fallback
5. **Проверяйте валидность file_id** — перед использованием убедитесь, что файл доступен

## Пример полной реализации

См. функцию `show_lesson()` в файле `bot.py` для полной реализации с:
- Проверкой наличия `file_id`
- Формированием подписи с тегами
- Обработкой ошибок
- Отправкой клавиатуры для навигации

