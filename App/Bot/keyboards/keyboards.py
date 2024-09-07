from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def keyboard_start():
    kb = [
        [KeyboardButton(text="Найти совещание")],
        [KeyboardButton(text="Добавить совещание")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def keyboard_back_start() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="В начало")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def keyboard_action():
    kb = [
        [KeyboardButton(text="Посмотреть файлы")],
        [KeyboardButton(text="Спикеры")],
        [KeyboardButton(text="Получить статус обработки файла")],
        [KeyboardButton(text="Выбрать другую встречу")],
        [KeyboardButton(text="В начало")]
        # [KeyboardButton(text="Добавить задачи в EvaProject")],
        # [KeyboardButton(text="Внести изменения в текст")],
        # [KeyboardButton(text="Прослушать с заданной секунды")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, persistent=True, resize_keyboard=True)


def file_type():
    kb = [
        [KeyboardButton(text="Отчеты и транскрипт текста, PDF с паролем")],
        [KeyboardButton(text="Отчеты и транскрипт текста, PDF")],
        [KeyboardButton(text="Отчеты и транскрипт текста, Word")],
        [KeyboardButton(text="Audio")],
        [KeyboardButton(text="В начало")],
        [KeyboardButton(text="Назад")]
        # [KeyboardButton(text="Саммари эмоционального окраса разговора")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, persistent=True, resize_keyboard=True)


def keyboard_speakers():
    kb = [
        [KeyboardButton(text="Посмотреть спикеров")],
        [KeyboardButton(text="Редактировать спикера")],
        [KeyboardButton(text="Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, persistent=True, resize_keyboard=True)