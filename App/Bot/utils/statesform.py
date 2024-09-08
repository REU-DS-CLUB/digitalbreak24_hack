from aiogram.fsm.state import StatesGroup, State


class FindMeetingSteps(StatesGroup):
    GET_MEETING_ID = State()
    GET_ACTION = State()
    GET_TYPE = State()


class AddNewMeeting(StatesGroup):
    GET_AUDIO_FILE = State()


class EditSpeakers(StatesGroup):
    GET_SPEAKER_ID = State()
    GET_SPEAKER_NAME = State()
    GET_SPEAKER_TITLE = State()


class AudioSpeaker(StatesGroup):
    GET_SPEAKER_ID_AUDIO = State()


class PasswordPDF(StatesGroup):
    GET_PASSWORD = State()
    DOWNLOAD_PDF_PASSWORD = State()


class LogicalBlocks(StatesGroup):
    LOGICAL_BLOCKS = State()
    SEND_FILE = State()