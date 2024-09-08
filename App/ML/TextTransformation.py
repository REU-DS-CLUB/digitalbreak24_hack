from secrets.api import API_GIGACHAT, YANDEXGPT_KEY
from LLM import GigaChatTask, YandexGPT
from Prompts import make_speaker_mapping_prompt, verificatiom_correctness_prompt, \
                    getting_question_prompt, questions_details_prompt, make_theme_prompt, \
                    tasks_details_prompt
import json
from datetime import datetime
import re
from langdetect import detect, DetectorFactory
import pickle as pkl
DetectorFactory.seed = 0


def diarisation_to_text(diarisation_result: dict) -> str:
    """
    Преобразует результаты диаризации (разбиения речи по спикерам) в текстовый формат.

    Аргументы:
        diarisation_result (dict): Словарь, где ключи представляют собой временные промежутки в формате
        "start,end", а значения — это информация о спикере и тексте реплики.
    
    Возвращает:
        str: Строка, содержащая временные промежутки, имена спикеров и реплики в виде:
        "Время: start - end Спикер: speaker Реплика Спикера: text", разделенные новой строкой.
    """
    result = []
    speaker_unique = []
    for key in diarisation_result.keys():
        second_start, second_end = [float(val.strip()) for val in key.split(',')]
        details = diarisation_result[key]
        speaker = details['speaker'].lower()[:-3] + f'_{len(speaker_unique) + 1}'
        speaker_unique.append(speaker)
        text = details['text']
        result.append(f"{second_start} - {second_end} {speaker}: {text} \n")
        participants = list(set(speaker_unique))
    return participants, '\n'.join(result)

# def make_mapping(model, system_prompt, text):
#     """
#     Преобразует текст с использованием модели, применяет системный промпт и возвращает результат в виде словаря.

#     Аргументы:
#         model: Модель, которая обрабатывает текст и промпт.
#         system_prompt: Промпт, используемый для настройки модели.
#         text: Текст, который нужно обработать моделью.
    
#     Возвращает:
#         dict: Результат работы модели, преобразованный в словарь из JSON-строки.
#     """

#     output = model.output(text, system_prompt)
#     output_corrected = output.replace("'", '"')
#     json_data = json.loads(output_corrected)
#     return json_data


def make_tasks(model, system_prompt, text):
    output = model.output(system_prompt, text)
    return json.loads(output.replace("'", '"'))


def make_rename_speaker_mapping(text, speaker_mapping):
    """
    Заменяет идентификаторы спикеров (например, SPEAKER_00) на их имена в тексте, используя заданное соответствие.

    Аргументы:
        text (str): Текст, содержащий идентификаторы спикеров.
        speaker_mapping (dict): Словарь с отображением идентификаторов спикеров на их имена. 
        Пример: {"SPEAKER_00": {"name": "Андрей"}}
    
    Возвращает:
        str: Текст с заменёнными идентификаторами спикеров на их имена.
    """

    for speaker in speaker_mapping.keys():
        text = text.replace(speaker, speaker_mapping[speaker]["name"])
    return text

    
def make_questions(model, system_prompt, text):
    output = model.output(text, system_prompt)
    questions = re.findall(r"'([^']*)'", output)
    questions = [i for i in questions if detect(i) == 'ru']
    return questions


def make_detail_questions(model, system_prompt, text, questions):
    # Генерация запроса для модели
    question_and_text = f"""### Вопросы: {questions} \n
                            ### Исходный текст: {text}"""

    # Получаем данные из модели (скорее всего, это строка)
    output = model.output(question_and_text, system_prompt)

    # Разбираем строку и ищем соответствующие блоки для каждого вопроса
    details = []

    for question in questions:
        question_detail = {
            'question_name': question,
            'decision': '',
            'people': [],
            'deadline': '',
            'context': ''
        }

        # Пытаемся найти соответствующую информацию для каждого вопроса в output
        # Используем регулярные выражения или текстовый парсинг
        decision_pattern = re.compile(rf'{re.escape(question)}.*?(?=\n|$)', re.IGNORECASE)
        people_pattern = r'speaker[_\s]\d+:?'
        deadline_pattern = r'(к \d{4} году|до \d{4} года|в \d{4} году|к \d{4})'
        context_pattern = r'(?<=:)(.*?)(?=\.)'

        # Ищем решение (decision)
        decision_match = re.search(decision_pattern, output)
        if decision_match:
            question_detail['decision'] = decision_match.group(0)

        # Ищем людей (people)

        people_matches = re.findall(people_pattern, output)
        if people_matches:
            question_detail['people'] = list(set(people_matches))

        # Ищем дедлайн (deadline)
        deadline_match = re.search(deadline_pattern, output)
        if deadline_match:
            question_detail['deadline'] = deadline_match.group(0)

        # Ищем контекст (context)
        context_match = re.search(context_pattern, output)
        if context_match:
            question_detail['context'] = context_match.group(0).strip()

        details.append(question_detail)

    return transform_data(details)


def make_theme(model, system_prompt, text):
    output = model.output(text, system_prompt)
    return output


def make_correction(model, system_prompt, json_file):
    """
    Исправляет текст в JSON-файле, используя модель, и обновляет содержимое текста на исправленный вариант.

    Аргументы:
        model: Модель для выполнения коррекции текста.
        system_prompt: Промпт для настройки модели.
        json_file (dict): JSON-файл, содержащий текст для коррекции.
    
    Возвращает:
        dict: Обновлённый JSON-словарь с исправленным текстом.
    """

    json_string = dict(json_file)
    for key in json_string.keys():
        text = json_string[key]['text']
        output = model.output(text, system_prompt)
        json_string[key]['text'] = output
        
        return json_string

def transform_data(data):
    transformed = []
    for entry in data:
        question_obj = {
            entry["question_name"]:
             [{
                "decision": entry["decision"],
                "people": entry["people"],
                "deadline": entry["deadline"],
                "context": entry["context"]
            }]
        }
        transformed.append(question_obj)
    return transformed


def make_final_dict(theme, participants, detail_questions, tasks):
    final_json = {
        "theme": theme,
        "participants": participants,
        "questions": detail_questions,
        "tasks":tasks}
    return final_json
