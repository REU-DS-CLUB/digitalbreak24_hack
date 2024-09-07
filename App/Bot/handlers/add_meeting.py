import os
# from pydub import AudioSegment

import requests
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.filters import Command

from App.Bot.utils.statesform import AddNewMeeting, FindMeetingSteps, EditSpeakers

from App.Bot.keyboards.keyboards import keyboard_start, keyboard_back_start, keyboard_action, file_type, keyboard_speakers

router = Router()


@router.message(AddNewMeeting.GET_AUDIO_FILE and F.content_type == "voice")
async def get_voice(message: Message, bot: Bot):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    audio_type = message.voice.mime_type.split("/")[1]
    if audio_type in ('ogg', 'wav', 'm4a', 'mp3', 'mpeg4', 'mpeg'):
        file_holder = f"{os.path.dirname(os.path.abspath(__file__))}\\voices\\"
        path = f"{file_holder}{str(file_id)}.{audio_type}"
        await bot.download_file(file_path, path)

        # AudioSegment.from_file(path).export(path.replace(file.filename.split('.')[-1], 'mp3'), format='mp3')

        headers = {
            'accept': 'application/json'
        }

        params = {
            'create_time': datetime.now(),
            'duration': message.voice.duration
        }

        open_file = open(path, 'rb')
        files = {
            'file': (f"{str(file_id)}.{audio_type}", open_file, message.voice.mime_type),
        }

        response = requests.post('http://84.201.145.135:8000/v1/handlers/file', params=params, headers=headers,
                                 files=files)
        answer = response.json()
        print(answer)
        if "error" not in answer and "file_id" in answer:
            await message.answer(f"Файл скачен. \nИдентификационный номер файла - {answer['file_id']}")
        else:
            await message.answer("Файл не загружен.")

        open_file.close()
        os.remove(path)
    else:
        await message.answer("Допустимые форматы: ogg, wav, m4a, mp3, mpeg4, mpeg")