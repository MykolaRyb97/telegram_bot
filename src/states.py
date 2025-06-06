
from aiogram.fsm.state import State, StatesGroup

class GPTStates(StatesGroup):
    waiting_for_prompt = State()

class TalkStates(StatesGroup):
    waiting_for_personality = State()
    chatting = State()

class QuizStates(StatesGroup):
    choosing_theme = State()
    answering = State()

class TranslateStates(StatesGroup):
    choosing_language = State()
    translating = State()

class RecommendStates(StatesGroup):
    choosing_category = State()
    choosing_genre = State()
    viewing_recommendation = State()