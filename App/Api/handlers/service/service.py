import json
from telegram import Bot

from Postgres.connections import get_connection
from ML.LLM import GigaChatTask, YandexGPT
from ML.TextTransformation import make_correction, diarisation_to_text, make_questions, make_detail_questions, make_theme, make_tasks, make_final_dict
from ML.secrets.api import API_GIGACHAT, YANDEXGPT_KEY
from ML.LLM import GigaChatTask, YandexGPT
from ML.Prompts import make_speaker_mapping_prompt, verificatiom_correctness_prompt, \
                    getting_question_prompt, questions_details_prompt, make_theme_prompt, \
                    tasks_details_prompt

from ML.SpeechProcessing import SpeechProcessing
from ML.diarization import diarization
from ML.EvaProjectIntegration.EvaProjectIntegration import create_task


class Service:
    """
    Service to handle requests with params
    """
    def __init__(self):
        self.gigachat = GigaChatTask(API_GIGACHAT)
        self.yandexgpt = YandexGPT(YANDEXGPT_KEY)

    @staticmethod
    def read_from_db(file_id: int, field_name: str) -> str:

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute(f"""
                    SELECT {field_name}
                    FROM public.file_library
                    WHERE id = {file_id};""")

                answer = cur.fetchone()

        return answer

    @staticmethod
    def update_field_db(file_id: int, field_name: str, new_value):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""
                        UPDATE public.file_library
                        SET {field_name} = {new_value}
                        WHERE id = {file_id};""")
                return 'Success'

        except Exception as e:
            return f'Error updating field: {e}'

    @staticmethod
    def insert_into_db(file_name, path, create_time, duration, chat_id):

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:

                    cur.execute(f"""
                        INSERT INTO public.file_library (file_name, create_time, duration, audio_path, status, chat_id)
                        VALUES ('{file_name}', '{create_time}', '{duration}', '{path}', 'получен и загружен', {chat_id});""")
                    cur.execute("SELECT currval('file_library_id_seq') as file_id;")
                    file_id = cur.fetchone()

                    conn.commit()

                return file_id

        except Exception as e:
            return e

    @staticmethod
    def update_speaker_mapping_db(file_id, speaker_id, new_name, new_role):

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:

                    cur.execute(f"""
                        SELECT speaker_mapping
                        FROM public.file_library 
                        WHERE id = '{file_id}';""")

                    new_speaker_mapping = cur.fetchone()['speaker_mapping']
                    old_values = new_speaker_mapping[speaker_id]
                    if new_name == '-':
                        new_name = old_values[0]
                    if new_role == '-':
                        new_role = old_values[1]
                    new_speaker_mapping[speaker_id] = [new_name, new_role]

                    cur.execute(f"""
                        UPDATE public.file_library 
                        SET speaker_mapping = '{json.dumps(new_speaker_mapping)}'
                        WHERE id = '{file_id}';""")

                    conn.commit()

                    return 'Success'

        except Exception as e:
            return f'Error updating field: {e}'

    @staticmethod
    def send_message_as_bot(file_id, message):

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""
                        SELECT chat_id
                        FROM public.file_library
                        WHERE id = {file_id};""")

                    chat_id = cur.fetchone()['chat_id']

            bot_token = '7443785768:AAEq0GdrZx_FwNH6INOkv4i7_AQ23BLNaps'
            bot = Bot(token=bot_token)
            bot.send_message(chat_id=chat_id, text=message)

        except Exception as e:
            return f'Error sending message through tg bot: {e}'

    def make_correction(self, json_file,):

        return make_correction(self.gigachat, verificatiom_correctness_prompt, json_file)

    @staticmethod
    def diarisation_to_text(json_file):

        return diarisation_to_text(json_file)

    def make_questions(self, text):

        return make_questions(self.gigachat, getting_question_prompt, text)

    def make_detail_questions(self, text, questions):

        return make_detail_questions(self.gigachat, questions_details_prompt, text, questions)

    def make_theme(self, text):

        return make_theme(self.gigachat, make_theme_prompt, text)

    def make_tasks(self, text):

        return make_tasks(self.gigachat, tasks_details_prompt, text)

    @staticmethod
    def make_final_dict(theme, participants, detail_questions, tasks):

        return make_final_dict(theme, participants, detail_questions, tasks)

    @staticmethod
    def speech_processing(audio_path):

        return diarization(audio_path)

    @staticmethod
    def run_task_tracker_processing(document):

        try:
           create_task(document)
           return "Success"

        except Exception as e:
            return f'Error sending message through tg bot: {e}'
