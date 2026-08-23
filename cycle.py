# ======================================
# StoryFund v0.4
# File: cycle.py
# Finálny systém týždenných kôl
# ======================================


import time
import datetime
import random


from settings_manager import get

from database import (
    get_state,
    save_state,
    get_stories,
    clear_stories,
    get_archive,
    save_archive,
    get_users,
    save_users
)



# ======================================
# TEST MODE
# ======================================

# True  = testovanie (admin spúšťa nové kolo)
# False = automatický kalendár

TEST_MODE = False

def is_test_mode():
    return get_state().get("test_mode", False)

def set_test_mode(value):
    state = get_state()
    state["test_mode"] = bool(value)
    save_state(state)





# ======================================
# IDENTIFIKÁCIA KOLA
# ======================================

def get_cycle_id():

    today = datetime.date.today()

    year, week, _ = today.isocalendar()

    return f"{year}-{week}"





def get_cycle_times():

    today = datetime.datetime.now()

    monday = (
        today
        -
        datetime.timedelta(
            days=today.weekday()
        )
    )

    start = monday.replace(
        hour=0,
        minute=1,
        second=0,
        microsecond=0
    )


    sunday = start + datetime.timedelta(
        days=6
    )


    end = sunday.replace(
        hour=16,
        minute=0,
        second=0,
        microsecond=0
    )


    return start.timestamp(), end.timestamp()






# ======================================
# VYTVORENIE NOVÉHO KOLA
# ======================================

def start_new_cycle():


    cycle_id = get_cycle_id()



    start, end = get_cycle_times()



    state = {


        "cycle_id": cycle_id,


        "status": "open",


        "opened_at": start,


        "closes_at": end,


        "fund": 0

    }



    save_state(state)



    reset_user_limits(
        cycle_id
    )



    return state





# ======================================
# RESET LIMITOV POUŽÍVATEĽOV
# ======================================

def reset_user_limits(cycle_id):


    users = get_users()



    for u in users:


        u["cycle_id"] = cycle_id


        u["stories_count"] = 0



    save_users(users)







# ======================================
# KONTROLA OTVORENIA
# ======================================

def is_open():


    if is_test_mode():

        return True



    state = get_state()



    now = time.time()



    if now >= state.get(
        "closes_at",
        0
    ):


        return False



    return state.get(
        "status"
    ) == "open"








# ======================================
# AKTUÁLNY STAV
# ======================================

def get_current_state():

    state = get_state()
    current_cycle = get_cycle_id()

    # Automaticky otvor nové kolo pri zmene týždňa
    if state.get("cycle_id") != current_cycle:
        return start_new_cycle()

    if not state.get("cycle_id"):
        return start_new_cycle()

    return state







# ======================================
# FOND
# ======================================

def set_fund(amount):


    state = get_current_state()


    state["fund"] = float(amount)


    save_state(state)






def get_fund():


    state = get_current_state()


    return state.get(
        "fund",
        0
    )







# ======================================
# MANUÁLNY ZÁPIS MINULÉHO KOLA
# ======================================

def record_previous_cycle(amount, recipients):
    """
    Ručne uloží údaje za už ukončené kolo.
    Číslo kola sa nepoužíva - ide iba o posledné/minulé kolo.
    """
    amount = float(amount)
    recipients = int(recipients)

    if amount < 0:
        raise ValueError("Suma nemôže byť záporná.")

    if recipients <= 0:
        raise ValueError("Počet príjemcov musí byť väčší ako 0.")

    per_person = amount / recipients

    archive = get_archive()

    archive.append({
        "type": "manual_previous_cycle",
        "fund": amount,
        "participants": recipients,
        "winner_count": recipients,
        "winners": [],
        "stories": [],
        "amount_per_person": per_person,
        "closed_at": time.time()
    })

    save_archive(archive)

    return per_person


# ======================================
# ŽREBOVANIE VÍŤAZOV
# ======================================

def draw_winners():
    stories = get_stories()

    participants = sorted({s["nik"] for s in stories})

    if not participants:
        return []

    winner_count = get("WINNERS_PER_CYCLE")

    if winner_count >= len(participants):
        return participants

    return random.sample(participants, winner_count)


# ======================================
# ARCHIVÁCIA
# ======================================

def archive_cycle():


    state = get_current_state()



    stories = get_stories()



    if not stories:

        return False




    archive = get_archive()



    winners = draw_winners()
    participants = sorted({s["nik"] for s in stories})

    archive.append({

        "cycle_id": state["cycle_id"],
        "fund": state["fund"],
        "participants": len(participants),
        "winner_count": len(winners),
        "winners": winners,
        "stories": stories,
        "closed_at": time.time()

    })



    save_archive(
        archive
    )



    return True







# ======================================
# NOVÉ KOLO
# ======================================

def force_new_cycle():
    print("=== force_new_cycle START ===")

    print("Archivujem...")
    archive_cycle()

    print("Mažem stories...")
    clear_stories()

    print("Vytváram nové kolo...")
    result = start_new_cycle()

    print("=== force_new_cycle END ===")

    return result






# ======================================
# AUTOMATICKÉ UZAVRETIE
# ======================================

def check_cycle():


    if is_test_mode():

        return



    state = get_current_state()



    if time.time() >= state["closes_at"]:


        force_new_cycle()