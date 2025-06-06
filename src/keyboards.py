
import json
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
config_path = BASE_DIR / 'resources' / 'menus' / 'main.json'

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")],  # Persistent start button
            [KeyboardButton(text="🎲 Випадковий факт")],
            [KeyboardButton(text="💬 ChatGPT")],
            [KeyboardButton(text="🗣 Розмова з історичною особистістю")],
            [KeyboardButton(text="📚 Вікторина")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False  # Keep keyboard visible
    )

def get_random_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Хочу ще факт", callback_data="new_random_fact"),
                InlineKeyboardButton(text="Закінчити", callback_data="end")
            ]
        ]
    )

def get_talk_personalities_keyboard() -> InlineKeyboardMarkup:
    personalities = config["personalities"]
    buttons = [[InlineKeyboardButton(text=person, callback_data=f"talk_{person}")] for person in personalities]
    buttons.append([InlineKeyboardButton(text="Закінчити", callback_data="end")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_talk_end_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Закінчити", callback_data="end")]
        ]
    )

def get_quiz_themes_keyboard() -> InlineKeyboardMarkup:
    themes = config["quiz_themes"]
    buttons = [[InlineKeyboardButton(text=theme, callback_data=f"quiz_{theme}")] for theme in themes]
    buttons.append([InlineKeyboardButton(text="Закінчити", callback_data="end")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_quiz_options_keyboard(theme: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ще питання", callback_data=f"quiz_{theme}"),
                InlineKeyboardButton(text="Змінити тему", callback_data="quiz_change_theme"),
                InlineKeyboardButton(text="Закінчити", callback_data="end")
            ]
        ]
    )

def get_quiz_answer_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="A", callback_data="answer_A"),
                InlineKeyboardButton(text="B", callback_data="answer_B"),
                InlineKeyboardButton(text="C", callback_data="answer_C"),
                InlineKeyboardButton(text="D", callback_data="answer_D")
            ]
        ]
    )