import io
import json
import os
from datetime import datetime
from typing import Dict, List
from pydub import AudioSegment

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile
from starlette.status import HTTP_405_METHOD_NOT_ALLOWED

# from utils.utils import get_user_station
from . import service

handlers = APIRouter(
    prefix="/v1/handlers",
    tags=['handlers']
)


@handlers.post(path="/file",
               description="receives and download file"
               )
async def receive_file(file: UploadFile) -> int | str:
    """
    Args:
        file:
    """

    # TODO: написать обработку формата файла на этой стороне
    if file.filename.split('.')[-1] == 'mp3':
        try:
            # получаем файл и пишем на диск
            with open(f'/files/raw_audio/{file.filename.split('.')[-1]}.mp3', 'wb') as disk_file:

                file_bytes = await file.read()
                disk_file.write(file_bytes)

                print(f"Received file named {file.filename} containing {len(file_bytes)} bytes. ")

            # создаем новую строку в бд
            file_id = service.insert_into_db(f'meeting_{''}')

            return file_id

        except Exception as e:
            return f"error: {e}, sorry :("

    else:
        try:
            sound = AudioSegment.from_mp3(file)
            sound.export(f'/files/raw_audio/{file.filename.split('.')[-1]}.mp3', format='mp3')

            # создаем новую строку в бд
            file_id = service.insert_into_db(f'meeting_{''}')

            return file_id

        except Exception as e:
            return f"error: {e}, sorry :("


@handlers.get(path="/process_file/{file_id}",
              description="runs processing on the downloaded file"
             )
async def process_file(file_id: int) -> str:
    """
    Args:
        file_id:
    """

    file_path = service.read_from_db(file_id, field_name='raw_audio_path')

    # TODO: call processing pipeline on file_path
    #

    # TODO: update status in db
    #

    return ""


@handlers.get(path="/status/{file_id}",
              description="returns file status"
              )
async def get_status(file_id: int) -> str:
    """
    Args:

    """

    # селектим из бд статус файла и возвращаем
    file_status = service.read_from_db(file_id, 'status')

    return file_status


# TODO: как ретурнить айдио-файл? архив?
@handlers.get(path="/get_status/{file_id}/{type}",
              description="sends chosen files to the client"
              )
async def send_file(file_id: int, type, unofficial_blocks="", sec_start="", sec_end="") -> List:
    """
    Args:

    """

    if type == "audio":
        file_path = service.read_from_db(file_id, type)
        file_name = ""

        return FileResponse(path=file_path, filename=file_name, media_type='audio/mp3')

    elif type == "docx":
        file_path = service.read_from_db(file_id, type)
        file_name = ""
        return FileResponse(path=file_path, filename=file_name, media_type='')

    elif type == "pdf":
        file_path = service.read_from_db(file_id, type)
        file_name = ""
        return FileResponse(path=file_path, filename=file_name, media_type='')

    elif type == "pdf_password":
        file_path = service.read_from_db(file_id, type)
        file_name = ""
        return FileResponse(path=file_path, filename=file_name, media_type='')

    else:
        return "error"


@handlers.get(path="/add_tasks/{file_id}",
              description="adds tasks to the task tracker"
              )
async def add_tasks(file_id: int) -> str:
    """
    Args:

    """

    # TODO: process tasks
    #

    status = ""

    return status


@handlers.get(path="/update_speakers_1/{file_id}",
              description="update speakers 1/3"
              )
async def update_speakers_1(file_id: int) -> Dict:
    """
    Args:

    """

    # TODO: query DB and return longest replicas fro each speaker
    #

    replicas = {}

    return replicas


# TODO: как вернуть аудио?
@handlers.get(path="/update_speakers_2/{file_id}",
              description="update speakers 2/3"
              )
async def update_speakers_2(file_id: int, line_id: int) -> str:
    """
    Args:

    """

    # TODO: query DB and get voice memo for the particular speaker
    #

    status = ""

    return status


@handlers.post(path="/update_speakers_3/{file_id}",
               description="update speakers 3/3"
               )
async def update_speakers_3(file_id: int, line_id: int, new_name: str) -> str:
    """
    Args:

    """

    status_code = ""

    return status_code
