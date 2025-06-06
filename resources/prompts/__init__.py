
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "random.txt", "r", encoding="utf-8") as f:
    random_txt = f.read().strip()

with open(BASE_DIR / "gpt.txt", "r", encoding="utf-8") as f:
    gpt_txt = f.read().strip()

with open(BASE_DIR / "quiz.txt", "r", encoding="utf-8") as f:
    quiz_txt = f.read().strip()

with open(BASE_DIR / "talk_cobain.txt", "r", encoding="utf-8") as f:
    talk_cobain_txt = f.read().strip()

with open(BASE_DIR / "talk_hawking.txt", "r", encoding="utf-8") as f:
    talk_hawking_txt = f.read().strip()

with open(BASE_DIR / "talk_maksV.txt", "r", encoding="utf-8") as f:
    talk_maksV_txt = f.read().strip()

with open(BASE_DIR / "talk_nietzsche.txt", "r", encoding="utf-8") as f:
    talk_nietzsche_txt = f.read().strip()

with open(BASE_DIR / "talk_queen.txt", "r", encoding="utf-8") as f:
    talk_queen_txt = f.read().strip()

with open(BASE_DIR / "talk_tolkien.txt", "r", encoding="utf-8") as f:
    talk_tolkien_txt = f.read().strip()