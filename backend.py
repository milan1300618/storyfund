# ======================================
# StoryFund v0.3
# File: backend.py
# Používatelia + limit príbehov
# ======================================

from settings_manager import get
from firebase_auth import create_user_auth
import time
import random
import string


from database import (
    get_users,
    save_users,
    get_stories,
    save_stories
)


from cycle import get_current_state



# ======================================
# GENEROVANIE ÚČTOV
# ======================================

def generate_nik():

    users = get_users()


    while True:

        nik = (
            "SF"
            +
            "".join(
                random.choices(
                    string.digits,
                    k=5
                )
            )
        )


        if not any(
            u["nik"] == nik
            for u in users
        ):

            return nik





def generate_pin():

    return "".join(
        random.choices(
            string.digits,
            k=6
        )
    )




# ======================================
# VYTVORENIE POUŽÍVATEĽA
# ======================================

def create_user(nik=None, pin=None):


    users = get_users()


    if nik is None:
        nik = generate_nik()

    if pin is None:
        pin = generate_pin()


    # ======================================
    # FIREBASE AUTH ÚČET ÚČASTNÍKA
    # ======================================
    # Účet sa vytvorí automaticky.
    # Účastník stále používa iba svoj NIK + PIN.
    auth_result = create_user_auth(nik, pin)

    if not auth_result.get("ok"):
        # Ak sa Firebase Auth účet nepodarí vytvoriť,
        # používateľa zatiaľ nezapisujeme do users.
        return None


    users.append({
    "nik": nik,
    "pin": pin,
    "registered": time.strftime("%Y-%m-%d %H:%M:%S"),
    "active": True,
    "cycle_id": "",
    "stories_count": 0
})


    save_users(users)



    return {

        "nik": nik,

        "pin": pin

    }





# ======================================
# LOGIN
# ======================================

def login_user(nik, pin):


    users = get_users()


    for u in users:


        if (

            u["nik"] == nik

            and

            u["pin"] == pin

        ):


            if not u.get(
                "active",
                True
            ):

                return False



            return True



    return False





# ======================================
# KONTROLA LIMITU
# ======================================

def can_add_story(nik):


    users = get_users()


    state = get_current_state()


    cycle_id = state["cycle_id"]



    for u in users:


        if u["nik"] == nik:



            # nové kolo

            if u.get(
                "cycle_id"
            ) != cycle_id:


                u["cycle_id"] = cycle_id

                u["stories_count"] = 0



                save_users(users)




            return (
    u["stories_count"] < get("MAX_STORIES_PER_CYCLE")
)



    return False





# ======================================
# ULOŽENIE PRÍBEHU
# ======================================

def save_story(
        nik,
        words,
        story,
        score
):


    if not can_add_story(nik):

        return False



    stories = get_stories()



    stories.append({

        "nik": nik,

        "words": words,

        "story": story,

        "score": score,

        "time": time.time()

    })



    save_stories(stories)



    users = get_users()



    state = get_current_state()



    for u in users:


        if u["nik"] == nik:


            u["cycle_id"] = state["cycle_id"]

            u["stories_count"] += 1



    save_users(users)



    return True





# ======================================
# FEED
# ======================================

def load_feed():


    stories = get_stories()


    stories.sort(

        key=lambda x:x["time"],

        reverse=True

    )


    return stories





# ======================================
# ADMIN FUNKCIE
# ======================================

def block_user(nik):


    users = get_users()


    for u in users:


        if u["nik"] == nik:


            u["active"] = False


            save_users(users)


            return True



    return False





def unblock_user(nik):


    users = get_users()


    for u in users:


        if u["nik"] == nik:


            u["active"] = True


            save_users(users)


            return True



    return False





def list_users():

    return get_users()