# ======================================
# StoryFund v0.4
# File: story_engine.py
# ======================================

import random


def load_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]


INTROS = load_lines("story_data/intro.txt")
MIDDLES = load_lines("story_data/middle.txt")
ENDINGS = load_lines("story_data/ending.txt")


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