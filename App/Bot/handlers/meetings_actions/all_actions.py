import requests

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from App.Bot.utils.statesform import AudioSpeaker, FindMeetingSteps, EditSpeakers
from App.Bot.handlers.meetings_actions import speakers, send_file
from App.Bot.keyboards.keyboards import keyboard_start, keyboard_action, file_type, keyboard_speakers

router = Router()

router.include_routers(
    speakers.router,
    send_file.router
)


@router.message(FindMeetingSteps.GET_MEETING_ID)
async def get_id_meeting(message: Message, state: FSMContext):
    error = "Неверный Идентификационный номер файла"
    if message.text.isdigit():

        headers = {
            'accept': 'application/json',
        }

        response = requests.get(f"http://84.201.145.135:8000/v1/handlers/status/{int(message.text)}", headers=headers)
        answer = response.json()
        if answer is not None and "status" in answer:
            await state.set_state(FindMeetingSteps.GET_ACTION)
            await message.answer("Выбери действие", reply_markup=keyboard_action())
            await state.update_data(file_id=int(message.text))
        else:
            await message.answer(error, reply_markup=keyboard_start())
    else:
        await message.answer(error, reply_markup=keyboard_start())


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Посмотреть файлы")
async def action_show_file(message: Message, state: FSMContext):
    await message.answer("Выбери тип файла", reply_markup=file_type())


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Спикеры")
async def speakers(message: Message, state: FSMContext):
    await get_speakers(message, state)
    await message.answer("Выбери действие", reply_markup=keyboard_speakers())


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Редактировать спикера")
async def edit_speakers(message: Message, state: FSMContext):
    await state.set_state(EditSpeakers.GET_SPEAKER_ID)
    await message.answer("Пришлите номер изменяемого спикера")


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Посмотреть спикеров")
async def show_speakers(message: Message, state: FSMContext):
    await get_speakers(message, state)


async def get_speakers(message: Message, state: FSMContext):
    data = await state.get_data()
    headers = {
        'accept': 'application/json',
    }

    response = requests.get(f"http://84.201.145.135:8000/v1/handlers/update_speakers_1/{data['file_id']}", headers=headers)
    ans = response.json()
    answer = ""
    if ans is not None and ans["speaker_mapping"] is not None:
        for speaker in ans["speaker_mapping"]:
            if ans['speaker_mapping'][speaker][0] == "":
                ans['speaker_mapping'][speaker][0] = "не задано"

            if ans['speaker_mapping'][speaker][1] == "":
                ans['speaker_mapping'][speaker][1] = "не задана"

            answer += f"{speaker}: имя {ans['speaker_mapping'][speaker][0]} (должность {ans['speaker_mapping'][speaker][1]})\n"
        await message.answer(answer)
    else:
        await message.answer("Нет спикеров.")


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Получить статус обработки файла")
async def get_file_status(message: Message, state: FSMContext):
    data = await state.get_data()
    headers = {
        'accept': 'application/json',
    }

    response = requests.get(f"http://84.201.145.135:8000/v1/handlers/status/{data['file_id']}", headers=headers)
    answer = response.json()
    if "error" not in data and 'file_id' in data and 'status' in answer:
        await message.answer(f"Статус файла {data['file_id']} - {answer['status']}")
    else:
        await message.answer("У файла нет статуса")


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Прослушать спикера по номеру")
async def audio_speaker(message: Message, state: FSMContext):
    await message.answer("Пришли номер спикера")
    await state.set_state(AudioSpeaker.GET_SPEAKER_ID_AUDIO)
