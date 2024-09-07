import os

import requests
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.filters import Command

from App.Bot.utils.statesform import AddNewMeeting, AudioSpeaker, EditSpeakers

from App.Bot.keyboards.keyboards import keyboard_start, keyboard_back_start, keyboard_action, file_type, keyboard_speakers

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
        await message.answer("Пришли имя спикера")
        await state.set_state(EditSpeakers.GET_SPEAKER_NAME)
    else:
        await message.answer("Неверный номер спикера", reply_markup=keyboard_speakers())


@router.message(EditSpeakers.GET_SPEAKER_NAME)
async def edit_speakers(message: Message, state: FSMContext):
    await state.update_data(speaker_name=message.text)
    await message.answer("Пришли должность спикера")
    await state.set_state(EditSpeakers.GET_SPEAKER_TITLE)


@router.message(EditSpeakers.GET_SPEAKER_TITLE)
async def edit_speakers(message: Message, state: FSMContext):
    await state.update_data(speaker_title=message.text)
    data = await state.get_data()
    await message.answer(f"Спикер - {data['file_id']}, {data['speaker_id']} {data['speaker_name']} {data['speaker_title']}")


@router.message(AudioSpeaker.GET_SPEAKER_ID_AUDIO)
async def check_speakers(message: Message, state: FSMContext):
    if message.text.isdigit() and await check_speaker_id(state, int(message.text)):
        await message.answer_voice()
    else:
        await message.answer("Неверный номер спикера", reply_markup=keyboard_speakers())

