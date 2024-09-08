import os

import requests

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from App.Bot.utils.statesform import PasswordPDF, FindMeetingSteps, LogicalBlocks
from pypdf import PdfReader, PdfWriter

router = Router()


async def get_file_type(text: str) -> tuple[str, str]:
    to_api = ""
    type_file = ""
    if text == "Отчет в PDF с паролем" or "Отчет в PDF":
        to_api = "sum_pdf"
        type_file = "pdf"

    if text == "Отчет в Word":
        to_api = "sum_word"
        type_file = "docx"

    if text == "Аудио":
        to_api = "raw_audio"
        type_file = "mp3"

    return to_api, type_file


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Отчет в PDF с паролем")
async def set_pdf(message: Message, state: FSMContext):
    await message.answer("Задайте пароль")
    await state.set_state(PasswordPDF.GET_PASSWORD)


@router.message(PasswordPDF.GET_PASSWORD)
async def set_pdf_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    file_path = await get_file(message, state)

    try:
        reader = PdfReader(file_path)

        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
        writer.encrypt(message.text)

        with open(file_path, "wb") as out_file:
            writer.write(out_file)

        file = FSInputFile(file_path)
        await message.reply_document(file)

    except Exception:
        await message.answer("Нет pdf")
    finally:
        os.remove(file_path)


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Отчет в PDF")
async def get_pdf(message: Message, state: FSMContext):
    file_path = await get_file(message, state)

    try:
        file = FSInputFile(file_path)
        await message.reply_document(file)

    except Exception:
        await message.answer("Нет файла")

    finally:
        os.remove(file_path)


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Отчет в Word")
async def get_word(message: Message, state: FSMContext):
    file_path = await get_file(message, state)

    try:
        file = FSInputFile(file_path)
        await message.reply_document(file)

    except Exception:
        await message.answer("Нет файла")

    finally:
        os.remove(file_path)


async def get_file(message: Message, state: FSMContext):
    data = await state.get_data()
    file_info = await get_file_type(message.text)

    headers = {
        'accept': 'application/json'
    }

    params = {
        'content_type': file_info[0]
    }

    response = requests.get(f"http://84.201.145.135:8000/v1/handlers/send_file/{data['file_id']}",
                            params=params,
                            headers=headers)

    file_path = f"{os.path.dirname(os.path.abspath(__file__))}\\voices\\{data['file_id']}.{file_info[1]}"
    f = open(file_path, 'wb')
    f.write(response.content)
    f.close()
    return file_path


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Аудио")
async def get_audio(message: Message, state: FSMContext):
    file_path = await get_file(message, state)

    try:
        file = FSInputFile(file_path)
        await message.reply_audio(file)

    except Exception:
        await message.answer("Нет аудиофайла")

    finally:
        os.remove(file_path)