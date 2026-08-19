# ======================================
# StoryFund v0.6
# File: config.py
# Centrálna konfigurácia aplikácie
# ======================================

# ======================================
# APLIKÁCIA
# ======================================

APP_NAME = "StoryFund"
APP_VERSION = "0.6"
APP_BUILD = "2026.07.16"

TEST_MODE = True


# ======================================
# PRÍBEHY
# ======================================

WORDS_TO_SHOW = 8
WORDS_TO_SELECT = 4

MAX_GENERATIONS = 3
MAX_STORIES_PER_CYCLE = 3


# ======================================
# AI
# ======================================

MIN_AI_SCORE = 70
MAX_AI_SCORE = 100

SHOW_AI_SCORE = True


# ======================================
# ZOBRAZENIE
# ======================================

SHOW_SELECTED_WORDS = False


# ======================================
# BUDÚCE FUNKCIE
# ======================================

ENABLE_COMMENTS = False


# ======================================
# TRANSPARENTNÝ ÚČET
# ======================================

TRANSPARENT_ACCOUNT = (
    "https://www.unicreditbank.sk/sk/ostatne/"
    "transparentny-ucet.html?"
    "IBAN=SK5611110000001491048088"
)