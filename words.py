# ======================================
# StoryFund v0.6
# File: words.py
# ======================================

import random

from settings_manager import get


WORDS = [

    # EMÓCIE
    "nádej", "smútok", "radosť", "strach", "láska",
    "osamelosť", "odvaha",

    # RODINA
    "matka", "otec", "dieťa", "rodina",
    "domov", "brat", "sestra",

    # ŽIVOT
    "práca", "škola", "budúcnosť",
    "minulosť", "sen", "realita",

    # PRÍRODA
    "les", "rieka", "dážď", "slnko",
    "noc", "hviezdy", "hory",

    # PROBLÉMY
    "choroba", "hlad", "chudoba",
    "únava", "boj", "ticho",

    # HODNOTY
    "pravda", "sila", "mier",
    "priateľstvo", "dôvera"
]


def generate_words():
    """
    Vráti náhodných get("WORDS_TO_SHOW") rôznych slov.
    """
#print("WORDS_TO_SHOW =", get("WORDS_TO_SHOW"))
    return random.sample(
        WORDS,
        get("WORDS_TO_SHOW")
    )