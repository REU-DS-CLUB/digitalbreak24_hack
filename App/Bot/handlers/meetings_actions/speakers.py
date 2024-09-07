import os

import requests
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.filters import Command

from App.Bot.utils.statesform import AddNewMeeting, FindMeetingSteps, EditSpeakers

from App.Bot.keyboards.keyboards import keyboard_start, keyboard_back_start, keyboard_action, file_type, keyboard_speakers

router = Router()


@router.message(EditSpeakers.GET_SPEAKER_ID)
async def edit_speakers(message: Message, state: FSMContext):
    if message.text.isdigit(): # Проверить что есть такой спефкер
        await state.update_data(speaker_id=int(message.text))
        await message.answer("Пришли имя спикера")
        await state.set_state(EditSpeakers.GET_SPEAKER_NAME)
    else:
        await message.answer("Неверный номер спикера", reply_markup=keyboard_start())


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

