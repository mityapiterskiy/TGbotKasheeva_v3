#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Парсер RTF файла для извлечения структуры чат-бота
"""
import re
import json
from pathlib import Path


def decode_rtf_unicode(text):
    """Декодирует Unicode escape-последовательности из RTF"""
    def replace_unicode(match):
        code = match.group(1)
        try:
            return chr(int(code))
        except ValueError:
            return ''
    
    # Заменяем \u1089\'3f на символы
    text = re.sub(r'\\u(\d+)\\\'3f', replace_unicode, text)
    # Заменяем обычные \u последовательности
    text = re.sub(r'\\u(\d+)', replace_unicode, text)
    return text


def parse_rtf_structure(rtf_file_path):
    """Парсит RTF файл и извлекает структуру бота"""
    
    with open(rtf_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Декодируем Unicode
    content = decode_rtf_unicode(content)
    
    # Убираем RTF разметку, оставляем только текст
    # Удаляем RTF команды
    content = re.sub(r'\\[a-z]+\d*\s?', '', content)
    content = re.sub(r'\{[^}]*\}', '', content)
    content = re.sub(r'\\par', '\n', content)
    content = re.sub(r'\\pard', '\n', content)
    
    # Очищаем от лишних пробелов
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    structure = {
        'greeting': '',
        'questions': [],
        'lessons': [],
        'groups': []
    }
    
    current_question = None
    current_lesson = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Приветствие
        if 'кнопка Начать' in line.lower() or 'здравствуйте' in line.lower():
            if i + 1 < len(lines):
                structure['greeting'] = lines[i + 1]
                i += 1
        
        # Вопросы
        elif 'кнопка Пройти опрос' in line.lower() or 'опрос' in line.lower():
            if i + 1 < len(lines):
                question_text = lines[i + 1]
                current_question = {
                    'text': question_text,
                    'variants': []
                }
                structure['questions'].append(current_question)
                i += 1
        
        # Варианты ответов
        elif 'вариант' in line.lower() and current_question:
            if i + 1 < len(lines):
                variant_text = lines[i + 1]
                current_question['variants'].append(variant_text)
                i += 1
        
        # Уроки
        elif 'урок' in line.lower() and ('видео' in line.lower() or 'видео-урок' in line.lower()):
            if i + 1 < len(lines):
                lesson_text = lines[i + 1]
                current_lesson = {
                    'number': len(structure['lessons']) + 1,
                    'description': lesson_text,
                    'video_file_id': None  # Будет заполнено позже
                }
                structure['lessons'].append(current_lesson)
                i += 1
        
        # Группы
        elif 'группа' in line.lower() or 'групп' in line.lower():
            if i + 1 < len(lines):
                group_text = lines[i + 1]
                structure['groups'].append({
                    'name': group_text,
                    'description': group_text
                })
                i += 1
        
        i += 1
    
    return structure


if __name__ == '__main__':
    rtf_file = Path('структура чат-бота.rtf')
    
    if not rtf_file.exists():
        print(f"Файл {rtf_file} не найден!")
        exit(1)
    
    structure = parse_rtf_structure(rtf_file)
    
    # Сохраняем структуру в JSON
    output_file = Path('bot_structure.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=2)
    
    print(f"Структура сохранена в {output_file}")
    print(f"Найдено вопросов: {len(structure['questions'])}")
    print(f"Найдено уроков: {len(structure['lessons'])}")
    print(f"Найдено групп: {len(structure['groups'])}")

