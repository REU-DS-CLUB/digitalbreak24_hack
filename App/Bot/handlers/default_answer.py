from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from App.Bot.keyboards.keyboards import keyboard_start
router = Router()


@router.message(F.text == "В начало")
async def get_back(message: Message, state: FSMContext):
    await state.clear()
    await get_start(message)


@router.message()
async def get_start(message: Message):
    await message.answer("Что вы хотите сделать?", reply_markup=keyboard_start())