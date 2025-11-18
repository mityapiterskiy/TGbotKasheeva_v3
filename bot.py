"""
Telegram бот для психотерапевтической программы
"""
import asyncio
import json
from pathlib import Path
from typing import Dict, Optional

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.chat_member import ChatMemberStatus

from config import BOT_TOKEN, CHANNEL_USERNAME, BOT_STRUCTURE_FILE, EMAIL_TO
from utils import (
    load_bot_structure,
    determine_group,
    save_user_responses,
    send_email_with_excel,
    send_to_moderator_telegram
)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Состояния FSM
class SurveyStates(StatesGroup):
    waiting_for_subscription = State()
    waiting_for_question_1 = State()
    waiting_for_question_2 = State()
    waiting_for_question_3 = State()
    watching_lessons = State()
    lesson_1 = State()
    lesson_2 = State()
    lesson_3 = State()


# Глобальная переменная для структуры бота
bot_structure: Dict = {}


async def check_channel_subscription(user_id: int) -> bool:
    """
    Проверяет подписку пользователя на канал @doctor_kashcheeva
    
    ВАЖНО: Для работы этой функции бот должен быть администратором канала
    или канал должен быть публичным.
    
    Возвращает True если пользователь подписан, False если нет.
    """
    if not CHANNEL_USERNAME:
        return True  # Если канал не указан, пропускаем проверку
    
    # Убираем @ если он есть в начале
    channel = CHANNEL_USERNAME.lstrip('@')
    
    try:
        # Проверяем статус пользователя в канале
        member = await bot.get_chat_member(f"@{channel}", user_id)
        
        # Пользователь считается подписанным если его статус:
        # - MEMBER - обычный подписчик
        # - ADMINISTRATOR - администратор канала
        # - CREATOR - создатель канала
        is_subscribed = member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]
        
        return is_subscribed
    except Exception as e:
        print(f"Ошибка проверки подписки на канал @{channel}: {e}")
        # В случае ошибки возвращаем False для безопасности
        return False


def create_subscription_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой подписки на канал @doctor_kashcheeva"""
    # Убираем @ если он есть в начале
    channel = CHANNEL_USERNAME.lstrip('@') if CHANNEL_USERNAME else 'doctor_kashcheeva'
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=bot_structure.get('channel_check', {}).get('button_text', 'Подписаться'),
            url=f"https://t.me/{channel}"
        )],
        [InlineKeyboardButton(
            text="✅ Я подписался",
            callback_data="check_subscription"
        )]
    ])
    return keyboard


def create_question_keyboard(question: Dict) -> InlineKeyboardMarkup:
    """Создает клавиатуру с вариантами ответа на вопрос"""
    buttons = []
    for i, variant in enumerate(question.get('variants', []), 1):
        buttons.append([InlineKeyboardButton(
            text=variant,
            callback_data=f"answer_{question['id']}_{i}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_lesson_keyboard(lesson: Dict) -> InlineKeyboardMarkup:
    """Создает клавиатуру для урока"""
    buttons = []
    if lesson.get('next_lesson'):
        buttons.append([InlineKeyboardButton(
            text="Следующий урок",
            callback_data=f"lesson_{lesson['next_lesson']}"
        )])
    else:
        buttons.append([InlineKeyboardButton(
            text="Завершить",
            callback_data="finish_lessons"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Проверяем подписку на канал
    if not await check_channel_subscription(user_id):
        await message.answer(
            bot_structure.get('channel_check', {}).get('message', 
                'Подпишитесь на канал для продолжения'),
            reply_markup=create_subscription_keyboard()
        )
        await state.set_state(SurveyStates.waiting_for_subscription)
        return
    
    # Если подписан, показываем приветствие
    await message.answer(bot_structure.get('greeting', 'Добро пожаловать!'))
    
    # Начинаем опрос
    await start_survey(message, state)


@dp.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, state: FSMContext):
    """Проверка подписки после нажатия кнопки"""
    user_id = callback.from_user.id
    
    if await check_channel_subscription(user_id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Начать диалогику",
                callback_data="start_survey"
            )]
        ])
        await callback.message.edit_text(
            bot_structure.get('subscription_check', {}).get('message', 
                'Спасибо за подписку!'),
            reply_markup=keyboard
        )
        await callback.answer("Отлично!")
    else:
        await callback.answer(
            "Пожалуйста, подпишитесь на канал, чтобы продолжить",
            show_alert=True
        )


@dp.callback_query(F.data == "start_survey")
async def start_survey_callback(callback: CallbackQuery, state: FSMContext):
    """Начинает опрос после нажатия кнопки"""
    await callback.answer()
    await start_survey(callback.message, state)


async def start_survey(message: Message, state: FSMContext):
    """Начинает опрос"""
    questions = bot_structure.get('questions', [])
    if not questions:
        await message.answer("Ошибка: вопросы не найдены в структуре бота")
        return
    
    first_question = questions[0]
    await message.answer(
        first_question['text'],
        reply_markup=create_question_keyboard(first_question)
    )
    await state.set_state(SurveyStates.waiting_for_question_1)
    await state.update_data(answers={})


@dp.callback_query(F.data.startswith("answer_"))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    """Обработчик ответов на вопросы"""
    data = callback.data.split('_')
    question_id = int(data[1])
    variant_id = int(data[2])
    
    # Получаем данные состояния
    state_data = await state.get_data()
    answers = state_data.get('answers', {})
    
    # Получаем вопрос
    questions = bot_structure.get('questions', [])
    question = next((q for q in questions if q['id'] == question_id), None)
    
    if not question:
        await callback.answer("Ошибка: вопрос не найден")
        return
    
    # Сохраняем ответ
    variant_text = question['variants'][variant_id - 1]
    answers[f'question_{question_id}'] = variant_text
    
    await state.update_data(answers=answers)
    await callback.answer()
    
    # Переходим к следующему вопросу или уроку
    if question.get('next_question'):
        next_question = next((q for q in questions if q['id'] == question['next_question']), None)
        if next_question:
            await callback.message.edit_text(
                next_question['text'],
                reply_markup=create_question_keyboard(next_question)
            )
            await state.set_state(SurveyStates.waiting_for_question_2 if question_id == 1 
                                else SurveyStates.waiting_for_question_3)
        else:
            await start_lessons(callback.message, state)
    elif question.get('next_step') == 'lessons':
        await start_lessons(callback.message, state)
    else:
        await finish_survey(callback.message, state)


async def start_lessons(message: Message, state: FSMContext):
    """Начинает показ уроков"""
    lessons = bot_structure.get('lessons', [])
    if not lessons:
        await message.answer("Ошибка: уроки не найдены")
        await finish_survey(message, state)
        return
    
    first_lesson = lessons[0]
    await show_lesson(message, state, first_lesson)


async def show_lesson(message: Message, state: FSMContext, lesson: Dict):
    """
    Показывает урок с видео
    
    Как работает хранение видео в Telegram:
    1. Видео хранится на серверах Telegram после загрузки
    2. Telegram выдает file_id - уникальный идентификатор файла для бота
    3. file_id можно использовать для повторной отправки без повторной загрузки
    4. file_id сохраняется в bot_structure.json в поле video_file_id
    
    Для получения file_id:
    - Отправьте видео боту в личные сообщения
    - Запустите get_video_id.py скрипт
    - Скопируйте полученный file_id в bot_structure.json
    """
    video_file_id = lesson.get('video_file_id')
    tags = lesson.get('tags', [])  # Получаем теги из структуры урока
    
    # Формируем подпись с тегами
    caption_parts = [
        f"📹 {lesson.get('title', 'Урок')}",
        "",
        lesson.get('description', '')
    ]
    
    # Добавляем теги в конец подписи
    if tags:
        hashtags = ' '.join([f"#{tag.replace(' ', '_')}" for tag in tags])
        caption_parts.append("")
        caption_parts.append(hashtags)
    
    caption = "\n".join(caption_parts)
    
    # Проверяем, является ли это placeholder
    if video_file_id and video_file_id.startswith('VIDEO_'):
        # Если это placeholder, сообщаем что нужно загрузить видео
        await message.answer(
            f"📹 {lesson.get('title', 'Урок')}\n\n"
            f"{lesson.get('description', '')}\n\n"
            f"⚠️ Видео еще не загружено. Пожалуйста, загрузите видео и обновите video_file_id в bot_structure.json",
            reply_markup=create_lesson_keyboard(lesson)
        )
    elif not video_file_id:
        # Если file_id отсутствует
        await message.answer(
            f"📹 {lesson.get('title', 'Урок')}\n\n"
            f"{lesson.get('description', '')}\n\n"
            f"⚠️ Видео не настроено. Добавьте video_file_id в bot_structure.json",
            reply_markup=create_lesson_keyboard(lesson)
        )
    else:
        # Отправляем видео с подписью и тегами
        try:
            await message.answer_video(
                video_file_id,
                caption=caption,
                reply_markup=create_lesson_keyboard(lesson)
            )
        except Exception as e:
            await message.answer(
                f"📹 {lesson.get('title', 'Урок')}\n\n"
                f"{lesson.get('description', '')}\n\n"
                f"⚠️ Ошибка отправки видео: {e}\n\n"
                f"Проверьте, что file_id корректный и видео доступно.",
                reply_markup=create_lesson_keyboard(lesson)
            )
    
    # Устанавливаем состояние в зависимости от номера урока
    if lesson['id'] == 1:
        await state.set_state(SurveyStates.lesson_1)
    elif lesson['id'] == 2:
        await state.set_state(SurveyStates.lesson_2)
    elif lesson['id'] == 3:
        await state.set_state(SurveyStates.lesson_3)


@dp.callback_query(F.data.startswith("lesson_"))
async def handle_lesson_callback(callback: CallbackQuery, state: FSMContext):
    """Обработчик перехода к следующему уроку"""
    lesson_id = int(callback.data.split('_')[1])
    lessons = bot_structure.get('lessons', [])
    
    lesson = next((l for l in lessons if l['id'] == lesson_id), None)
    if lesson:
        await callback.answer()
        await show_lesson(callback.message, state, lesson)
    else:
        await callback.answer("Урок не найден")


@dp.callback_query(F.data == "finish_lessons")
async def finish_lessons_callback(callback: CallbackQuery, state: FSMContext):
    """Завершение просмотра уроков"""
    await callback.answer()
    await finish_survey(callback.message, state)


async def finish_survey(message: Message, state: FSMContext):
    """Завершает опрос и определяет группу"""
    state_data = await state.get_data()
    answers = state_data.get('answers', {})
    
    # Определяем группу
    group_id = determine_group(answers)
    
    # Сохраняем ответы
    user_id = message.from_user.id
    username = message.from_user.username
    
    excel_file = await save_user_responses(user_id, username, answers, group_id)
    
    # Отправляем на email
    if EMAIL_TO:
        await send_email_with_excel(excel_file)
    
    # Отправляем модератору в Telegram
    await send_to_moderator_telegram(bot, user_id, username, answers, group_id)
    
    # Определяем финальное сообщение
    if group_id:
        group = next((g for g in bot_structure.get('groups', []) if g['id'] == group_id), None)
        group_name = group.get('name', 'группа') if group else 'группа'
        
        final_message = (
            f"🎉 Поздравляю! Вы прошли опрос.\n\n"
            f"📊 На основе ваших ответов вам подходит: **{group_name}**\n\n"
            f"Скоро с вами свяжется модератор для уточнения деталей.\n\n"
            f"Контакты: {bot_structure.get('moderator_contact', '@doctorkashcheeva')}"
        )
    else:
        final_message = (
            f"Спасибо за прохождение опроса!\n\n"
            f"Скоро с вами свяжется модератор.\n\n"
            f"Контакты: {bot_structure.get('moderator_contact', '@doctorkashcheeva')}"
        )
    
    await message.answer(final_message)
    await state.clear()


async def main():
    """Главная функция запуска бота"""
    global bot_structure
    
    # Загружаем структуру бота
    bot_structure = await load_bot_structure(BOT_STRUCTURE_FILE)
    
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

