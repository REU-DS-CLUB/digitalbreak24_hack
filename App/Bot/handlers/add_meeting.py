import os

import requests
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message

from App.Bot.utils.statesform import AddNewMeeting

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

        headers = {
            'accept': 'application/json'
        }

        params = {
            'chat_id': str(message.chat.id),
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
        if "error" not in answer and "file_id" in answer:
            await message.answer(f"Файл скачен. \nИдентификационный номер файла - {answer['file_id']}")
        else:
            await message.answer("Файл не загружен.")

        open_file.close()
        os.remove(path)
    else:
        await message.answer("Допустимые форматы: ogg, wav, m4a, mp3, mpeg4, mpeg")