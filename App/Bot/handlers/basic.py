from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from App.Bot.handlers import add_meeting, default_answer
from App.Bot.handlers.meetings_actions import all_actions

from App.Bot.utils.statesform import AddNewMeeting, FindMeetingSteps

from App.Bot.keyboards.keyboards import keyboard_back_start, keyboard_action

router = Router()

router.include_routers(
    add_meeting.router,
    all_actions.router,
    default_answer.router
)


@router.message(F.text == "Добавить совещание")
async def get_audio_meeting(message: Message, state: FSMContext):
    await message.reply("Пришлите аудио-файл", reply_markup=keyboard_back_start())
    await state.set_state(AddNewMeeting.GET_AUDIO_FILE)


@router.message(F.text == "Найти совещание")
async def ask_id_meeting(message: Message, state: FSMContext):
    await message.reply("Пришлите идентификационный номер совещания", reply_markup=keyboard_back_start())
    await state.set_state(FindMeetingSteps.GET_MEETING_ID)


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Выбрать другую встречу")
async def change_file(message: Message, state: FSMContext):
    await ask_id_meeting(message, state)


@router.message(F.text == "Назад")
async def get_back(message: Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer("Выбери действие", reply_markup=keyboard_action())
    print(current_state)

    # if current_state == "FindMeetingSteps:GET_ACTION" or current_state == "EditSpeakers:GET_SPEAKER_ID" or current_state == "FindMeetingSteps.GET_MEETING_ID" or :
    #     await message.answer("Выбери действие", reply_markup=keyboard_action())
    # else:
    #     print(current_state)
        # EditSpeakers:GET_SPEAKER_ID


if __name__ == "__main__":
    pass





