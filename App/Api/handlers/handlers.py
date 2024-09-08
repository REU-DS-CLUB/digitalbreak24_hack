import json
import os
from pathlib import Path
from typing import Dict
from pydub import AudioSegment

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from fastapi import UploadFile
from starlette.status import HTTP_405_METHOD_NOT_ALLOWED

from . import service

handlers = APIRouter(
    prefix="/v1/handlers",
    tags=['handlers']
)

tmp_file_dir = "/files/raw_audio/"
Path(tmp_file_dir).mkdir(parents=True, exist_ok=True)


@handlers.post(path="/file",
               summary='Endpoint for saving audio file from user',
               description="receives audio file in one of the accepted formats and saves it locally"
               )
async def receive_file(file: UploadFile, create_time='2024-01-01 10:00:00', duration=0):
    """
    Args:
        file: бинарный вид аудио-файла в одном из допустимых форматов (ogg, wav, m4a, mp3, mpeg4, mpeg)
        create_time: дата создания файла
        duration: продолжительность аудио
    """

    try:
        # получаем файл и пишем на диск
        path = os.path.join(tmp_file_dir, file.filename)
        with open(path, 'wb') as disk_file:

            file_bytes = await file.read()
            disk_file.write(file_bytes)
            print(f"Received file named {file.filename} containing {len(file_bytes)} bytes with path {path}. ")

        # если файл уже не в формате mp3, то переводим
        if file.filename.split('.')[-1] != 'mp3':
            try:
                sound = AudioSegment.from_file(path)
                sound.export(path.replace(file.filename.split('.')[-1], 'mp3'), format='mp3')
            except Exception as e:
                raise e

        # создаем новую строку в бд
        file_id = service.insert_into_db(file.filename.replace(file.filename.split('.')[-1], 'mp3'),
                                         path.replace(file.filename.split('.')[-1], 'mp3'),
                                         create_time,
                                         duration)

        # возвращаем клиенту идентификатор записи, по которой к ней можно будет обращаться
        return file_id

    except Exception as e:
        raise e


@handlers.get(path="/process_file/{file_id}",
              summary='Endpoint for activating ML-processing on the chosen audio file',
              description="retrieves correct path to the audio file from db table and starts ML-pipeline with it"
              )
async def process_file(file_id: int) -> str:
    """
    Args:
        file_id: идентификатор файла, который необходим для процессинга
    """

    file_path = service.read_from_db(file_id, field_name='raw_audio_path')

    # TODO: call processing pipeline on file_path
    #

    #

    # TODO: call tg bot alert
    #

    status = service.update_field_db(file_id, 'status', 'обработка завершена')

    return status


@handlers.get(path="/status/{file_id}",
              summary='Endpoint for getting processing status',
              description="takes file id and sends back actual processing status for that file from db table"
              )
async def get_status(file_id: int):
    """
    Args:
        file_id: идентификатор файла, который необходим для процессинга
    """

    try:
        # селектим из бд статус файла и возвращаем
        file_status = service.read_from_db(file_id, 'status')
        return file_status

    except Exception as e:
        return {"error": e}


@handlers.get(path="/send_file/{file_id}/{type}",
              summary="Endpoint for getting processing results",
              description="receives recording id and sends it's chosen files back to the client"
              )
async def send_file(file_id: int, content_type: str, unofficial_blocks=""):
    """
    Args:
        file_id: идентификатор файла, который необходим для процессинга
        content_type: тип желаемого результата [raw_audio/sum_word/sum_pdf]
        unofficial_blocks: желаемые логические блоки в неофициальном саммари записи (необязательный параметр)
    """

    if content_type == "raw_audio":
        audio_path = service.read_from_db(file_id, 'raw_audio_path')['raw_audio_path']

        return FileResponse(path=audio_path,
                            filename=audio_path.split('/')[-1],
                            media_type='audio/mpeg')

    # TODO: написать логику
    elif content_type == "sum_word":
        file_path_1 = service.read_from_db(file_id, 'official_summary_path')
        file_name_1 = ""
        file_path_2 = service.read_from_db(file_id, 'unofficial_summary_path')
        file_name_2 = ""
        return FileResponse(path=file_path_1, filename=file_name_1, media_type='')

    # TODO: написать логику
    elif content_type == "sum_pdf":
        file_path_1 = service.read_from_db(file_id, 'official_summary_path')
        file_name_1 = ""
        file_path_2 = service.read_from_db(file_id, 'unofficial_summary_path')
        file_name_2 = ""
        return FileResponse(path=file_path_1, filename=file_name_1, media_type='')

    else:
        return "error"


@handlers.get(path="/add_tasks/{file_id}",
              summary="Endpoint for adding tasks to the task tracker",
              description="creates tasks in task tracker from parsed audio recordings"
              )
async def add_tasks(file_id: int) -> str:
    """
    Args:
        file_id: идентификатор файла, который необходим для процессинга
    """

    # TODO: process tasks
    #

    status = ""

    return status


@handlers.get(path="/update_speakers_1/{file_id}",
              summary="Endpoint for getting speakers list",
              description="sends all speakers,  from the selected file"
              )
async def update_speakers_1(file_id: int) -> Dict:
    """
    Args:
        file_id: идентификатор файла, который необходим для процессинга
    """

    replicas = service.read_from_db(file_id, 'speaker_mapping')

    return replicas


@handlers.get(path="/update_speakers_2/{file_id}",
              summary="Endpoint for sending audio sample for chosen speaker",
              description="receives speaker's id and sends their voice sample"
              )
async def update_speakers_2(file_id: int, speaker_id: str):
    """
    Args:
        file_id: идентификатор файла, который необходим для процессинга
        speaker_id: выбранный ключ в словаре спикеров
    """

    def find_longest(speaker):

        d = service.read_from_db(file_id, 'diarization')['diarization']

        max_len = -1
        time_brackets = ''

        for sec, dicts in d.items():
            if dicts['speaker'] == speaker:
                if len(dicts['text']) > max_len:
                    max_len = len(dicts['text'])
                    time_brackets = sec

        return time_brackets

    try:
        audio_path = service.read_from_db(file_id, 'raw_audio_path')['raw_audio_path']
        print(f'audio_path_1: {audio_path}')

        song = AudioSegment.from_mp3(audio_path)
        print(f'find_longest: {find_longest(speaker_id)}')

        start = int(find_longest(speaker_id).split('->')[0])
        extract = song[start*1000: start*1000+20*1000]

        print(f'path: {audio_path.replace('.mp3', '-extract.mp3')}')
        extract.export(audio_path.replace('.mp3', '-extract.mp3'), format="mp3")

        return FileResponse(path=audio_path.replace('.mp3', '-extract.mp3'),
                            filename=audio_path.split('/')[-1],
                            media_type='audio/mpeg')

    except Exception as e:
        return {"error": e}


@handlers.post(path="/update_speakers_3/{file_id}",
               summary="Endpoint for updating speaker data in db table",
               description="receiving new values for speaker's name and role and updating mapping field in the db"
               )
async def update_speakers_3(file_id: int, speaker_id: str, new_name: str = '-', new_role: str = '-') -> str:
    """
    Args:
        file_id: идентификатор файла, который необходим для процессинга
        speaker_id: выбранный ключ в словаре спикеров
        new_name: новое имя для установки в бд (необязательный параметр)
        new_role: новая роль для установки в бд (необязательный параметр)
    """

    status_code = service.update_speaker_mapping_db(file_id, speaker_id, new_name, new_role)

    return status_code
