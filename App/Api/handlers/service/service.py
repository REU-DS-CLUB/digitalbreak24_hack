import json

from Postgres.connections import get_connection


class Service:
    """
    Service to handle requests with params
    """

    @staticmethod
    def read_from_db(file_id: int, field_name: str) -> str:

        with get_connection() as conn:
            with conn.cursor() as cur:

                cur.execute(f"""
                    SELECT {field_name}
                    FROM public.file_library
                    WHERE id = {file_id};""")

                answer = cur.fetchone()

        return answer

    @staticmethod
    def update_field_db(file_id: int, field_name: str, new_value):
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""
                        UPDATE public.file_library
                        SET {field_name} = {new_value}
                        WHERE id = {file_id};""")
                return 'Success'

        except Exception as e:
            return f'Error updating field: {e}'

    @staticmethod
    def insert_into_db(file_name, path, create_time, duration):

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:

                    cur.execute(f"""
                        INSERT INTO public.file_library (raw_file_name, create_time, duration, raw_audio_path, status)
                        VALUES ('{file_name}', '{create_time}', '{duration}', '{path}', 'получен и загружен');""")
                    cur.execute("SELECT currval('file_library_id_seq') as file_id;")
                    file_id = cur.fetchone()

                    conn.commit()

                return file_id

        except Exception as e:
            return e

    @staticmethod
    def update_speaker_mapping_db(file_id, speaker_id, new_name, new_role):

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:

                    cur.execute(f"""
                        SELECT speaker_mapping
                        FROM public.file_library 
                        WHERE id = '{file_id}';""")

                    new_speaker_mapping = cur.fetchone()['speaker_mapping']
                    old_values = new_speaker_mapping[speaker_id]
                    if new_name == '-':
                        new_name = old_values[0]
                    if new_role == '-':
                        new_role = old_values[1]
                    new_speaker_mapping[speaker_id] = [new_name, new_role]

                    cur.execute(f"""
                        UPDATE public.file_library 
                        SET speaker_mapping = '{json.dumps(new_speaker_mapping)}'
                        WHERE id = '{file_id}';""")

                    conn.commit()

                    return 'Success'

        except Exception as e:
            return f'Error updating field: {e}'
