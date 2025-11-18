#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения file_id видео файлов
Отправьте видео боту в личные сообщения, затем запустите этот скрипт
"""
import asyncio
from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Dispatcher
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def get_file_id(message: Message):
    """Получает file_id из любого сообщения"""
    if message.video:
        video = message.video
        file_id = video.file_id
        file_unique_id = video.file_unique_id
        file_size = video.file_size
        duration = video.duration
        width = video.width
        height = video.height
        
        # Формируем информацию о видео
        info_text = (
            f"✅ Видео получено!\n\n"
            f"📹 **File ID:** `{file_id}`\n"
            f"🔑 **File Unique ID:** `{file_unique_id}`\n\n"
        )
        
        if duration:
            info_text += f"⏱️ Длительность: {duration} сек\n"
        if file_size:
            size_mb = file_size / (1024 * 1024)
            info_text += f"📦 Размер: {size_mb:.2f} МБ\n"
        if width and height:
            info_text += f"📐 Разрешение: {width}x{height}\n"
        
        info_text += (
            f"\n💡 **Инструкция:**\n"
            f"Скопируйте File ID и вставьте в bot_structure.json "
            f"в поле `video_file_id` для соответствующего урока.\n\n"
            f"File Unique ID можно использовать для отслеживания "
            f"одного и того же файла (не изменяется при переотправке)."
        )
        
        await message.answer(
            info_text,
            parse_mode="Markdown"
        )
        
        # Выводим в консоль
        print(f"\n{'='*60}")
        print(f"📹 ВИДЕО ИНФОРМАЦИЯ")
        print(f"{'='*60}")
        print(f"File ID:        {file_id}")
        print(f"File Unique ID: {file_unique_id}")
        if duration:
            print(f"Длительность:   {duration} сек")
        if file_size:
            print(f"Размер:         {file_size / (1024 * 1024):.2f} МБ")
        if width and height:
            print(f"Разрешение:     {width}x{height}")
        print(f"{'='*60}\n")
    elif message.document:
        file_id = message.document.file_id
        await message.answer(
            f"✅ Документ получен!\n\n"
            f"📄 File ID: `{file_id}`",
            parse_mode="Markdown"
        )
        print(f"\n{'='*50}")
        print(f"DOCUMENT FILE ID: {file_id}")
        print(f"{'='*50}\n")
    else:
        await message.answer(
            "Отправьте видео файл, чтобы получить его file_id"
        )


async def main():
    print("Бот запущен для получения file_id")
    print("Отправьте видео боту в личные сообщения")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

