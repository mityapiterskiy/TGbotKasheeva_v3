# Решение проблемы установки зависимостей

## 🔍 Что происходит:

У вас **Python 3.13** - это очень новая версия (вышла недавно). Пакет `aiogram` зависит от `pydantic-core`, который пытается собраться из исходников, но для этого нужен **Rust компилятор**.

## ❌ Проблема:

```
ERROR: Failed building wheel for pydantic-core
Rust not found, installing into a temporary directory
```

Python 3.13 слишком новый - многие пакеты еще не имеют готовых бинарных сборок для него.

## ✅ Решения (выберите одно):

### Решение 1: Использовать Python 3.11 или 3.12 (РЕКОМЕНДУЕТСЯ)

Эти версии более стабильны и имеют готовые бинарные сборки:

```bash
# Проверьте какие версии Python установлены
ls /usr/local/bin/python3.*
# или
which python3.12 python3.11

# Если есть python3.12 или python3.11, используйте его:
python3.12 -m pip install -r requirements.txt
# или
python3.11 -m pip install -r requirements.txt

# Затем запускайте бота через эту версию:
python3.12 bot.py
```

### Решение 2: Установить Rust (если нужно использовать Python 3.13)

```bash
# Установите Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Перезапустите терминал или выполните:
source $HOME/.cargo/env

# Затем попробуйте снова:
pip3 install -r requirements.txt
```

### Решение 3: Использовать виртуальное окружение с Python 3.12

```bash
# Установите pyenv (если нет)
brew install pyenv

# Установите Python 3.12
pyenv install 3.12.7

# Создайте виртуальное окружение
pyenv local 3.12.7
python -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Запустите бота
python bot.py
```

### Решение 4: Обновить версии пакетов (может помочь)

Попробуйте установить более новые версии без фиксации:

```bash
pip3 install aiogram aiofiles python-dotenv openpyxl aiohttp --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

## 🎯 Быстрое решение (если есть Python 3.12):

```bash
# 1. Проверьте есть ли Python 3.12
python3.12 --version

# 2. Если есть, установите зависимости через него
python3.12 -m pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

# 3. Запускайте бота через Python 3.12
python3.12 bot.py
```

## 📝 Рекомендация:

**Лучше всего использовать Python 3.11 или 3.12** - они стабильны и все пакеты имеют готовые сборки для них.

Python 3.13 слишком новый и многие пакеты еще не адаптированы.

