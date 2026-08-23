# ======================================
# StoryFund v0.4
# File: story_engine.py
# ======================================

import random
import os


def load_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]


INTROS = load_lines(os.path.join(os.path.dirname(__file__), "intro.txt"))
MIDDLES = load_lines(os.path.join(os.path.dirname(__file__), "middle.txt"))
ENDINGS = load_lines(os.path.join(os.path.dirname(__file__), "ending.txt"))


def generate_story(words):

    if len(words) != 4:
        return "Vyber presne 4 slová."

    intro = random.choice(INTROS)
    middle = random.choice(MIDDLES)
    ending = random.choice(ENDINGS)

    story = f"""{intro}

{middle}

{ending}
"""

    return story.strip()