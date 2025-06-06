
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram import Router
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext

from settings.utils import get_logger
from settings.config import config
from resources.prompts import (
    random_txt, gpt_txt, quiz_txt, talk_cobain_txt, talk_hawking_txt,
    talk_maksV_txt, talk_nietzsche_txt, talk_queen_txt, talk_tolkien_txt
)
from src.keyboards import (
    get_main_menu_keyboard, get_random_keyboard, get_talk_personalities_keyboard,
    get_talk_end_keyboard, get_quiz_themes_keyboard, get_quiz_options_keyboard,
    get_quiz_answer_keyboard
)
from src.openai_api import get_chatgpt_response
from src.states import GPTStates, TalkStates, QuizStates

logger = get_logger(__name__)
router = Router()

quiz_scores = {}
disliked_items = {}

PERSONALITY_IMAGE_MAP = {
    "Курт Кобейн": "talk_cobain.jpg",
    "Стівен Гокінг": "talk_hawking.jpg",
    "Максим Вовкодав": "talk_maksV.jpg",
    "Фрідріх Ніцше": "talk_nietzsche.jpg",
    "Королева Єлизавета": "talk_queen.jpg",
    "Джон Роналд Руел Толкін": "talk_tolkien.jpg"
}

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext) -> None:
    logger.info(f"Команда /start викликана користувачем {message.from_user.id}")
    with open(config.path_to_messages / "main.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()
    photo_path = config.path_to_images / "avatar_main.jpg"
    if not photo_path.exists():
        logger.error(f"Файл не знайдено: {photo_path}")
        await message.answer("⚠️ Зображення не знайдено.")
        return
    photo = FSInputFile(photo_path)
    await message.answer_photo(photo=photo, caption=text, reply_markup=get_main_menu_keyboard())
    await state.clear()

@router.message(Command("random"))
async def random_command(message: Message) -> None:
    try:
        logger.info(f"Команда /random викликана користувачем {message.from_user.id}")
        photo_path = config.path_to_images / "random.jpg"
        if not photo_path.exists():
            photo_path = config.path_to_images / "avatar_main.jpg"
        logger.info(f"Шлях до зображення: {photo_path}")

        photo = FSInputFile(photo_path)
        with open(config.path_to_messages / "random.txt", "r", encoding="utf-8") as f:
            caption = f.read().strip()
        await message.answer_photo(photo=photo, caption=caption)

        fact = await get_chatgpt_response(random_txt)
        logger.info(f"Отримана відповідь від ChatGPT: {fact}")
        await message.answer(fact, reply_markup=get_random_keyboard())

    except TelegramAPIError as e:
        logger.error(f"Telegram API помилка при /random: {e}")
        await message.answer("⚠️ Помилка Telegram API.")
    except Exception as e:
        logger.error(f"Невідома помилка при /random: {e}")
        await message.answer("⚠️ Щось пішло не так.")

@router.callback_query(lambda c: c.data == "new_random_fact")
async def handle_new_random_fact(callback: CallbackQuery):
    try:
        logger.info(f"Отримано callback_data: {callback.data} від користувача {callback.from_user.id}")
        fact = await get_chatgpt_response(random_txt)
        logger.info(f"Новий факт: {fact}")
        await callback.message.answer(fact, reply_markup=get_random_keyboard())
        await callback.answer()

    except TelegramAPIError as e:
        logger.error(f"Telegram API помилка при натисканні кнопки: {e}")
        await callback.answer("⚠️ Виникла помилка Telegram API.", show_alert=True)
    except Exception as e:
        logger.error(f"Невідома помилка при обробці callback: {e}")
        await callback.answer("⚠️ Щось пішло не так.", show_alert=True)

@router.message(TalkStates.chatting)
async def handle_talk_chatting(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        personality = data.get("personality")
        system_prompt = data.get("system_prompt")

        logger.info(f"Обробка повідомлення для особистості: {personality}")
        if not personality or not system_prompt:
            logger.error("Дані про особистість або промпт відсутні в стані.")
            await message.answer("⚠️ Помилка: інформація про особистість втрачена. Спробуй обрати особистість знову через /talk.")
            await state.clear()
            return

        user_input = message.text.strip()
        if not user_input:
            logger.warning("Отримано порожнє повідомлення.")
            await message.answer("⚠️ Будь ласка, напиши повідомлення.")
            return

        logger.info(f"Вхідне повідомлення: {user_input}")
        logger.info(f"Системний промпт: {system_prompt}")

        full_prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        logger.info(f"Повний промпт для OpenAI: {full_prompt}")


        response = await get_chatgpt_response(full_prompt)
        if not response:
            logger.error("Відсутня відповідь від OpenAI API.")
            await message.answer("⚠️ Не вдалося отримати відповідь від сервісу. Спробуй ще раз.")
            return


        logger.info(f"Відповідь від OpenAI: {response}")


        await message.answer(response, reply_markup=get_talk_end_keyboard())

    except TelegramAPIError as e:
        logger.error(f"Помилка Telegram API при обробці чату: {e}")
        await message.answer("⚠️ Помилка Telegram API. Спробуй ще раз.")
    except Exception as e:
        logger.error(f"Помилка при обробці чату: {e}", exc_info=True)
        await message.answer("⚠️ Щось пішло не так. Спробуй обрати особистість знову через /talk.")
        await state.clear()

@router.message()
async def handle_text_buttons(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()


    if current_state == TalkStates.chatting:
        return

    text = message.text.strip() if message.text else ""

    if text == "/start":
        await start_command(message, state)
        return

    if text == "🎲 Випадковий факт" or text == "/random":
        await random_command(message)
        return

    if text == "💬 ChatGPT" or text == "/gpt":
        await message.answer("🧠 Напиши своє запитання до ChatGPT.")
        await state.set_state(GPTStates.waiting_for_prompt)
        return

    if text == "🗣 Розмова з історичною особистістю" or text == "/talk":
        await talk_command(message, state)
        return

    if text == "📚 Вікторина" or text == "/quiz":
        await quiz_command(message, state)
        return


    if current_state == GPTStates.waiting_for_prompt:
        await gpt_command(message, state)
        return


    await message.answer("🤖 Я не впізнав цю команду. Спробуй ще раз або натисни /start.")

@router.message(Command("gpt"))
async def gpt_command(message: Message, state: FSMContext) -> None:
    try:
        user_input = message.text.strip()[4:].strip() if message.text.startswith("/gpt") else message.text
        if not user_input:
            await message.answer("⚠️ Напиши своє запитання після команди /gpt.")
            return

        logger.info(f"Користувач {message.from_user.id} запитав: {user_input}")
        photo_path = config.path_to_images / "gpt.jpg"
        if not photo_path.exists():
            photo_path = config.path_to_images / "avatar_main.jpg"
        logger.info(f"Шлях до зображення: {photo_path}")

        photo = FSInputFile(photo_path)
        with open(config.path_to_messages / "gpt.txt", "r", encoding="utf-8") as f:
            caption = f.read().strip()
        await message.answer_photo(photo=photo, caption=caption)

        response = await get_chatgpt_response(f"{gpt_txt}\n{user_input}")
        logger.info(f"Відповідь ChatGPT: {response}")
        await message.answer(response)
        await state.clear()  # Reset state after response

    except TelegramAPIError as e:
        logger.error(f"Telegram API помилка при обробці /gpt: {e}")
        await message.answer("⚠️ Помилка Telegram API.")
    except Exception as e:
        logger.error(f"Невідома помилка при /gpt: {e}")
        await message.answer("⚠️ Щось пішло не так.")

@router.message(Command("talk"))
async def talk_command(message: Message, state: FSMContext) -> None:
    try:
        logger.info(f"Команда /talk викликана користувачем {message.from_user.id}")
        photo_path = config.path_to_images / "talk.jpg"
        if not photo_path.exists():
            photo_path = config.path_to_images / "avatar_main.jpg"
        if not photo_path.exists():
            logger.error(f"Файл не знайдено: {photo_path}")
            await message.answer("⚠️ Зображення не знайдено.")
            return

        photo = FSInputFile(photo_path)
        with open(config.path_to_messages / "talk.txt", "r", encoding="utf-8") as f:
            caption = f.read().strip()
        await message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=get_talk_personalities_keyboard()
        )
        await state.set_state(TalkStates.waiting_for_personality)

    except TelegramAPIError as e:
        logger.error(f"Помилка при обробці /talk: {e}")
        await message.answer("⚠️ Помилка Telegram API.")

@router.callback_query(lambda c: c.data.startswith("talk_"))
async def handle_talk_personality(callback: CallbackQuery, state: FSMContext):
    personality = callback.data.replace("talk_", "")
    prompt_map = {
        "Курт Кобейн": talk_cobain_txt,
        "Стівен Гокінг": talk_hawking_txt,
        "Максим Вовкодав": talk_maksV_txt,
        "Фрідріх Ніцше": talk_nietzsche_txt,
        "Королева Єлизавета": talk_queen_txt,
        "Джон Роналд Руел Толкін": talk_tolkien_txt
    }
    system_prompt = prompt_map.get(personality)
    if not system_prompt:
        await callback.answer("⚠️ Промпт для цієї особистості не знайдено.", show_alert=True)
        return

    image_file = PERSONALITY_IMAGE_MAP.get(personality, "avatar_main.jpg")
    photo_path = config.path_to_images / image_file
    if not photo_path.exists():
        photo_path = config.path_to_images / "avatar_main.jpg"
    photo = FSInputFile(photo_path)
    await callback.message.answer_photo(
        photo=photo,
        caption=f"Ти розмовляєш із {personality}. Напиши своє повідомлення!"
    )

    await state.update_data(personality=personality, system_prompt=system_prompt)
    await state.set_state(TalkStates.chatting)
    await callback.answer()

@router.message(Command("quiz"))
async def quiz_command(message: Message, state: FSMContext) -> None:
    try:
        logger.info(f"Команда /quiz викликана користувачем {message.from_user.id}")
        user_id = message.from_user.id
        quiz_scores[user_id] = quiz_scores.get(user_id, 0)

        photo_path = config.path_to_images / "quiz.jpg"
        if not photo_path.exists():
            photo_path = config.path_to_images / "avatar_main.jpg"
        if not photo_path.exists():
            logger.error(f"Файл не знайдено: {photo_path}")
            await message.answer("⚠️ Зображення не знайдено.")
            return

        photo = FSInputFile(photo_path)
        with open(config.path_to_messages / "quiz.txt", "r", encoding="utf-8") as f:
            caption = f.read().strip()
        await message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=get_quiz_themes_keyboard()
        )
        await state.set_state(QuizStates.choosing_theme)

    except TelegramAPIError as e:
        logger.error(f"Помилка при обробці /quiz: {e}")
        await message.answer("⚠️ Помилка Telegram API.")

@router.callback_query(lambda c: c.data.startswith("quiz_"))
async def handle_quiz_theme(callback: CallbackQuery, state: FSMContext):
    theme = callback.data.replace("quiz_", "")
    prompt = (
        f"{quiz_txt}\n"
        f"Створи одне запитання на тему '{theme}' з 4 варіантами відповідей (A, B, C, D), "
        f"і напиши правильну відповідь наприкінці у форматі: 'Правильна відповідь: X'"
    )
    full_response = await get_chatgpt_response(prompt)

    # Парсинг відповіді GPT
    lines = full_response.strip().splitlines()
    question_text = "\n".join([line for line in lines if not line.startswith("Правильна відповідь:")])
    correct_answer_line = next((line for line in lines if "Правильна відповідь:" in line), "")
    correct_answer = correct_answer_line.split(":")[-1].strip().upper()

    await callback.message.answer(question_text, reply_markup=get_quiz_answer_keyboard())


    await state.update_data(
        theme=theme,
        question_text=question_text,
        correct_answer=correct_answer
    )
    await state.set_state(QuizStates.answering)
    await callback.answer()

@router.callback_query(lambda c: c.data == "quiz_change_theme")
async def handle_quiz_change_theme(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📚 Обери нову тему:", reply_markup=get_quiz_themes_keyboard())
    await state.set_state(QuizStates.choosing_theme)
    await callback.answer()

@router.message(QuizStates.answering)
async def handle_quiz_answer(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        data = await state.get_data()
        user_answer = message.text.strip().upper()
        correct = data.get("correct_answer")
        theme = data.get("theme")
        question = data.get("question_text")

        prompt = (
            f"Питання: {question}\n"
            f"Правильна відповідь: {correct}\n"
            f"Користувач відповів: {user_answer}\n"
            f"Відповідай коротко 'Правильно!' або 'Неправильно!', і додай пояснення."
        )

        result = await get_chatgpt_response(prompt)


        if "Правильно!" in result:
            quiz_scores[user_id] = quiz_scores.get(user_id, 0) + 1

        score = quiz_scores[user_id]
        await message.answer(f"{result}\n\n🎯 Твій рахунок: {score}", reply_markup=get_quiz_options_keyboard(theme))
    except Exception as e:
        logger.error(f"Помилка при обробці відповіді: {e}", exc_info=True)
        await message.answer("⚠️ Щось пішло не так.")

@router.callback_query(lambda c: c.data == "end")
async def handle_end(callback: CallbackQuery, state: FSMContext):
    logger.info(f"Користувач {callback.from_user.id} завершив розмову")
    with open(config.path_to_messages / "main.txt", "r", encoding="utf-8") as f:
        text = f.read().strip()
    photo_path = config.path_to_images / "avatar_main.jpg"
    if not photo_path.exists():
        logger.error(f"Файл не знайдено: {photo_path}")
        await callback.message.answer("⚠️ Зображення не знайдено.")
        return
    photo = FSInputFile(photo_path)
    await callback.message.answer_photo(photo=photo, caption=text, reply_markup=get_main_menu_keyboard())
    await state.clear()
    await callback.answer()

@router.callback_query(lambda c: c.data.startswith("answer_"))
async def handle_quiz_answer_button(callback: CallbackQuery, state: FSMContext):
    try:
        user_id = callback.from_user.id
        user_answer = callback.data.replace("answer_", "")
        data = await state.get_data()
        correct = data.get("correct_answer")
        question = data.get("question_text")
        theme = data.get("theme")

        prompt = (
            f"Питання: {question}\n"
            f"Правильна відповідь: {correct}\n"
            f"Користувач відповів: {user_answer}\n"
            f"Відповідай 'Правильно!' або 'Неправильно!', і коротко поясни чому."
        )

        result = await get_chatgpt_response(prompt)

        if "Правильно!" in result:
            quiz_scores[user_id] = quiz_scores.get(user_id, 0) + 1

        score = quiz_scores[user_id]
        await callback.message.answer(
            f"{result}\n\n🎯 Твій рахунок: {score}",
            reply_markup=get_quiz_options_keyboard(theme)
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Помилка при обробці відповіді кнопкою: {e}", exc_info=True)
        await callback.message.answer("⚠️ Щось пішло не так.")