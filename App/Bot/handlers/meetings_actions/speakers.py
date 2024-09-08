import os

import requests

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from App.Bot.utils.statesform import AudioSpeaker, EditSpeakers

from App.Bot.keyboards.keyboards import keyboard_speakers

router = Router()


async def check_speaker_id(state: FSMContext, id_speaker: int):
    data = await state.get_data()
    headers = {
        'accept': 'application/json',
    }

    response = requests.get(f"http://84.201.145.135:8000/v1/handlers/update_speakers_1/{data['file_id']}", headers=headers)
    ans = response.json()
    if ans is not None and ans["speaker_mapping"] is not None:
        amount_speakers = len(ans["speaker_mapping"])
        if id_speaker <= amount_speakers:
            return True
    return False


@router.message(EditSpeakers.GET_SPEAKER_ID)
async def edit_speakers(message: Message, state: FSMContext):
    if message.text.isdigit() and await check_speaker_id(state, int(message.text)):
        await state.update_data(speaker_id=int(message.text))
        await message.answer("Отправьте ФИО спикера либо прочерк (-), чтобы оставить текущий")
        await state.set_state(EditSpeakers.GET_SPEAKER_NAME)
    else:
        await message.answer("Неверный номер спикера", reply_markup=keyboard_speakers())


@router.message(EditSpeakers.GET_SPEAKER_NAME)
async def edit_speakers_fio(message: Message, state: FSMContext):
    await state.update_data(speaker_name=message.text)
    await message.answer("Отправьте должность спикера либо прочерк (-), чтобы оставить текущую")
    await state.set_state(EditSpeakers.GET_SPEAKER_TITLE)


@router.message(EditSpeakers.GET_SPEAKER_TITLE)
async def edit_speakers_title(message: Message, state: FSMContext):
    await state.update_data(speaker_title=message.text)
    data = await state.get_data()

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'speaker_id': f"speaker_{data['speaker_id']}",
        'new_name': data['speaker_name'],
        'new_role': data['speaker_title']
    }

    response = requests.post(f"http://84.201.145.135:8000/v1/handlers/update_speakers_3/{data['file_id']}",
                             params=params,
                             headers=headers)
    await message.answer("Изменения загружены")


@router.message(AudioSpeaker.GET_SPEAKER_ID_AUDIO)
async def check_speakers(message: Message, state: FSMContext):
    if message.text.isdigit() and await check_speaker_id(state, int(message.text)):
        data = await state.get_data()

        headers = {
            'accept': 'application/json'
        }

        params = {
            'speaker_id': f"speaker_{message.text}"
        }

        response = requests.get(f"http://84.201.145.135:8000/v1/handlers/update_speakers_2/{data['file_id']}", params=params,
                                headers=headers, allow_redirects=True)

        file_path = f"{os.path.dirname(os.path.abspath(__file__))}\\voices\\{data['file_id']}_{message.text}.mp3"
        f = open(file_path, 'wb')
        f.write(response.content)

        try:
            file = FSInputFile(file_path)
            await message.reply_audio(file)
        except Exception:
            await message.answer("Нет аудиофайла")
        finally:
            f.close()
            os.remove(file_path)
    else:
        await message.answer("Неверный номер спикера", reply_markup=keyboard_speakers())
