from datetime import datetime
from typing import List

import pandas as pd
from Api.handlers.model.score_per_station import ScorePerStation
from utils.utils import preprocessing
from Postgres.connections import get_connection


class Service:
    """
    Service to handle requests with params
    """

    def read_from_db(self, file_id: int, field_name: str) -> str:

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute(f"""
                    SELECT {field_name}
                    FROM public.file_library
                    WHERE id = {file_id};""")

        # TODO: проверить корректность вывода
        return cur.fetch()

    # TODO: update path in db
    def update_path_db(self, file_id: int, field_name: str, new_value):

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    UPDATE public.file_library
                    SET {field_name} = {new_value}
                    WHERE id = {file_id};""")

    def insert_into_db(self, file_name) -> int:
        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT max(id) + 1
                    FROM public.file_library;""")

                file_id = cur.fetch()

                cur.execute(f"""
                    INSERT INTO public.file_library (file_name, status)
                    VALUES ({file_name}, 'received and downloaded');""")

                # TODO: проверить корректность вывода
                conn.commit()

        return file_id

    def update_speaker_mapping_db(self, speaker_id, new_name):

        # TODO: select json from DB

        # TODO: replace old value with new_value by key

        pass

    # TODO: processing task tracker
    #

    # TODO: processing ML
    #

    # TODO:
