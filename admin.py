# ======================================
# StoryFund v0.2
# File: admin.py
# Admin panel
# ======================================


from database import get_admin
from cycle import force_new_cycle

from backend import (
    create_user,
    list_users,
    block_user,
    unblock_user
)

from cycle import (
    set_fund,
    preview_distribution,
    distribute,
    close_cycle
)



# ======================================
# ADMIN LOGIN
# ======================================

def admin_login():

    admin = get_admin()


    print("\n================")
    print(" ADMIN LOGIN ")
    print("================")


    nik = input("NIK: ")
    pin = input("PIN: ")


    if (
        nik == admin["nik"]
        and
        pin == admin["pin"]
    ):

        print("\n✔ Admin prihlásený")

        return True


    print("\n❌ Nesprávne údaje")

    return False




# ======================================
# HLAVNÉ MENU
# ======================================

def admin_menu():


    while True:


        print("\n============================")
        print("        ADMIN PANEL")
        print("============================")


        print("""
1. Vytvoriť používateľa
2. Zobraziť používateľov
3. Blokovať používateľa
4. Odblokovať používateľa

5. Nastaviť fond
6. Náhľad rozdelenia
7. Rozdeliť pomoc
8. Uzavrieť kolo

0. Koniec
""")


        choice = input("Vyber: ")



        if choice == "1":

            create_user_menu()



        elif choice == "2":

            show_users()



        elif choice == "3":

            block_menu()



        elif choice == "4":

            unblock_menu()



        elif choice == "5":

            set_fund_menu()



        elif choice == "6":

            preview_menu()



        elif choice == "7":

            distribute_menu()



        elif choice == "8":

            close_menu()



        elif choice == "0":

            break





# ======================================
# VYTVORIŤ ÚČET
# ======================================

def create_user_menu():


    user = create_user()


    print("\n================")
    print(" NOVÝ ÚČET ")
    print("================")


    print(
        "NIK:",
        user["nik"]
    )


    print(
        "PIN:",
        user["pin"]
    )



# ======================================
# ZOZNAM POUŽÍVATEĽOV
# ======================================

def show_users():


    users = list_users()


    print("\n================")
    print(" POUŽÍVATELIA ")
    print("================")


    for u in users:


        status = (
            "AKTÍVNY"
            if u.get("active", True)
            else
            "BLOKOVANÝ"
        )


        print(
            u["nik"],
            "-",
            status
        )





# ======================================
# BLOKOVANIE
# ======================================

def block_menu():


    nik = input(
        "NIK na blokovanie: "
    )


    if block_user(nik):

        print("✔ Používateľ zablokovaný")

    else:

        print("❌ NIK nenájdený")





# ======================================
# ODBLOKOVANIE
# ======================================

def unblock_menu():


    nik = input(
        "NIK na odblokovanie: "
    )


    if unblock_user(nik):

        print("✔ Používateľ odblokovaný")

    else:

        print("❌ NIK nenájdený")





# ======================================
# FOND
# ======================================

def set_fund_menu():


    try:

        amount = float(
            input(
                "Suma fondu: "
            )
        )


        set_fund(amount)


        print(
            "✔ Fond nastavený"
        )


    except:

        print(
            "❌ Chyba"
        )





# ======================================
# NÁHĽAD
# ======================================

def preview_menu():


    try:

        count = int(
            input(
                "Počet príjemcov: "
            )
        )


        amount = preview_distribution(
            count
        )


        print(
            "Každý dostane:",
            amount,
            "€"
        )


    except:

        print(
            "❌ Chyba"
        )





# ======================================
# ROZDELENIE
# ======================================

def distribute_menu():


    try:

        count = int(
            input(
                "Počet príjemcov: "
            )
        )


        result = distribute(
            count
        )


        print(
            "\n✔ Rozdelené"
        )


        for r in result:

            print(
                r["nik"],
                "->",
                r["amount"],
                "€"
            )


    except:

        print(
            "❌ Chyba"
        )





# ======================================
# UZAVRETIE KOLA
# ======================================

def close_menu():


    close_cycle()


    print(
        "✔ Kolo uzavreté"
    )

def close_cycle(self):
    force_new_cycle()



# ======================================
# ŠTART
# ======================================

if __name__ == "__main__":


    if admin_login():

        admin_menu()