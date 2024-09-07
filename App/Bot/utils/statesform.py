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
