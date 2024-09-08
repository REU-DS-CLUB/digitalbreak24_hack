import os

import requests

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from App.Bot.utils.statesform import PasswordPDF, FindMeetingSteps, LogicalBlocks
from pypdf import PdfReader, PdfWriter

router = Router()


async def get_file_type(text: str) -> tuple[str, str, str]:
    oficial = ""
    inform = ""
    type_file = ""
    if text == "Отчет в PDF с паролем" or "Отчет в PDF":
        oficial = "official_summary_pdf"
        inform = "unofficial_summary_pdf"
        type_file = "pdf"

    if text == "Отчет в Word":
        oficial = "official_summary_word"
        inform = "unofficial_summary_word"
        type_file = "docx"

    if text == "Аудио":
        oficial = "audio"
        inform = "audio"
        type_file = "mp3"

    return oficial, inform, type_file


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Отчет в PDF с паролем")
async def set_pdf(message: Message, state: FSMContext):
    await message.answer("Задайте пароль")
    await state.set_state(PasswordPDF.GET_PASSWORD)


@router.message(PasswordPDF.GET_PASSWORD)
async def set_pdf_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    file_path = await get_file(message, state)

    try:
        reader = PdfReader(file_path[0])

        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
        writer.encrypt(message.text)

        with open(file_path[0], "wb") as out_file:
            writer.write(out_file)

        file = FSInputFile(file_path[1])
        await message.answer("Официальный файл")
        await message.reply_document(file)

        reader = PdfReader(file_path[1])

        writer = PdfWriter()
        writer.append_pages_from_reader(reader)
        writer.encrypt(message.text)

        with open(file_path[1], "wb") as out_file:
            writer.write(out_file)

        file = FSInputFile(file_path[1])
        await message.answer("Неофициальный файл")
        await message.reply_document(file)

    except Exception:
        await message.answer("Нет pdf")
    finally:
        os.remove(file_path[0])
        os.remove(file_path[1])


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Отчет в PDF")
async def get_pdf(message: Message, state: FSMContext):
    file_path = await get_file(message, state)

    try:
        file_ofic = FSInputFile(file_path[0])
        await message.answer("Официальный файл")
        await message.reply_document(file_ofic)

        file_informal = FSInputFile(file_path[1])
        await message.answer("Неофициальный файл")
        await message.reply_document(file_informal)

    except Exception:
        await message.answer("Нет файла")

    finally:
        os.remove(file_path[0])
        os.remove(file_path[1])


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Отчет в Word")
async def get_word(message: Message, state: FSMContext):
    file_path = await get_file(message, state)

    try:
        file_ofic = FSInputFile(file_path[0])
        await message.answer("Официальный файл")
        await message.reply_document(file_ofic)

        file_informal = FSInputFile(file_path[1])
        await message.answer("Неофициальный файл")
        await message.reply_document(file_informal)

    except Exception:
        await message.answer("Нет файла")

    finally:
        os.remove(file_path[0])
        os.remove(file_path[1])


async def get_file(message: Message, state: FSMContext):
    data = await state.get_data()
    file_info = await get_file_type(message.text)

    headers = {
        'accept': 'application/json'
    }

    params_oficial = {
        'content_type': file_info[0]
    }

    response_oficial = requests.get(f"http://84.201.145.135:8000/v1/handlers/send_file/{data['file_id']}",
                            params=params_oficial,
                            headers=headers)

    params_informal = {
        'content_type': file_info[1]
    }

    response_informal = requests.get(f"http://84.201.145.135:8000/v1/handlers/send_file/{data['file_id']}",
                            params=params_informal,
                            headers=headers)

    file_path_ofic = f"{os.path.dirname(os.path.abspath(__file__))}\\voices\\{data['file_id']}_ofic.{file_info[2]}"
    file_path_info = f"{os.path.dirname(os.path.abspath(__file__))}\\voices\\{data['file_id']}_informal.{file_info[2]}"
    f = open(file_path_ofic, 'wb')
    f.write(response_oficial.content)
    f.close()

    f = open(file_path_info, 'wb')
    f.write(response_informal.content)
    f.close()
    return file_path_ofic, file_path_info


@router.message(FindMeetingSteps.GET_ACTION and F.text == "Аудио")
async def get_audio(message: Message, state: FSMContext):
    file_path = await get_file(message, state)

    try:
        file = FSInputFile(file_path[0])
        await message.reply_audio(file)

    except Exception:
        await message.answer("Нет аудиофайла")

    finally:
        os.remove(file_path[0])
        os.remove(file_path[1])
