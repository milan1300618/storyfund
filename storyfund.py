import random
import json
import time

print("=== STORYFUND SYSTEM ===")
# -------------------------
# 1. LOGIN (NIK)
# -------------------------
nik = input("Zadaj svoj NIK: ")
print("\nVitaj:", nik)

# -------------------------
# 2. SLOVNÍK SYSTÉMU
# -------------------------
slova_db = {
    "emocie": ["nádej", "strach", "bolesť", "láska", "smútok", "odvaha", "pomoc", "radosť"],
    "miesta": ["nemocnica", "domov", "mesto", "ulica", "škola", "les", "byt", "dedina"],
    "udalosti": ["nehoda", "choroba"," strata", "začiatok", "koniec", "boj", "zmena", "záchrana"],
    "predmety": ["list", "mobil", "auto", "postel", "peniaze", "fotka", "dvere", "okno"]
}

# -------------------------
# 3. GENERÁCIA 8 SLOV
# -------------------------
def generate_words():
    words = []
    for k in slova_db:
        words.append(random.choice(slova_db[k]))
    while len(words) < 8:
        all_words = sum(slova_db.values(), [])
        words.append(random.choice(all_words))
    random.shuffle(words)
    return words[:8]

words = generate_words()

print("\n--- VYBER 4 SLOV ---")
for i, w in enumerate(words):
    print(f"{i+1}. {w}")

# -------------------------
# 4. VÝBER 4 SLOV
# -------------------------
vyber = input("\nZadaj 4 čísla (napr. 1 3 5 7): ")
idx = [int(x)-1 for x in vyber.split()]
selected = [words[i] for i in idx[:4]]

print("\nVybral si:", selected)

# -------------------------
# 5. GENERÁTOR PRÍBEHU
# -------------------------
templates = [
    "V živote človeka zohrali rolu slová {a}, {b}, {c} a {d}.",
    "Príbeh sa začal v {b}, kde sa objavila {a} a všetko zmenila.",
    "Nikto nečakal, že {c} prinesie zmenu spojenú s {d}.",
    "V tichom momente prišla {a} a s ňou aj {b}."
]

def generate_story(words):
    t = random.choice(templates)
    return t.format(a=words[0], b=words[1], c=words[2], d=words[3])

story = generate_story(selected)

print("\n--- PRÍBEH ---\n")
print(story)

# -------------------------
# 6. HODNOTENIE POTREBY
# -------------------------
high_value = ["nemocnica", "choroba", "bolesť", "smútok", "nehoda", "záchrana", "strach"]
low_value = ["radosť", "škola", "hra", "láska", "smiech"]

def evaluate(words):
    score = 50
    for w in words:
        if w in high_value:
            score += 10
        if w in low_value:
            score -= 10
    score += random.randint(-10, 10)
    return max(0, min(100, score))

score = evaluate(selected)

print("\n--- HODNOTENIE ---")
print(f"Potrebná pomoc: {score}%")

# -------------------------
# 7. ULOŽENIE
# -------------------------
data = {
    "nik": nik,
    "slova": selected,
    "pribeh": story,
    "score": score,
    "time": time.time()
}

with open("stories.json", "a") as f:
    f.write(json.dumps(data) + "\n")

print("\nUložené do databázy (stories.json)")
# ======================================
# CREATE STORY SCREEN
# ČASŤ 3/5
# ======================================


class CreateStoryScreen(MDScreen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.words = []
        self.selected = []


    def on_enter(self):

        self.clear_widgets()

        self.words = generate_words()

        self.selected = []


        main = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            padding=dp(20)
        )


        title = MDLabel(
            text="Vytvor príbeh",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(50)
        )


        main.add_widget(title)



        self.info = MDLabel(
            text="Vyber 4 slová",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )


        main.add_widget(self.info)



        self.word_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None
        )


        self.word_box.bind(
            minimum_height=self.word_box.setter("height")
        )


        main.add_widget(self.word_box)


        self.show_words()



        new_btn = MDRaisedButton(
            text="🔄 Nové slová",
            pos_hint={"center_x": .5}
        )


        new_btn.bind(
            on_release=self.new_words
        )


        main.add_widget(new_btn)



        create_btn = MDRaisedButton(
            text="✍️ Vytvoriť príbeh",
            pos_hint={"center_x": .5}
        )


        create_btn.bind(
            on_release=self.create_story
        )


        main.add_widget(create_btn)



        back_btn = MDFlatButton(
            text="⬅ Späť"
        )


        back_btn.bind(
            on_release=lambda x:
            setattr(
                self.manager,
                "current",
                "feed"
            )
        )


        main.add_widget(back_btn)



        self.add_widget(main)



    def show_words(self):

        self.word_box.clear_widgets()


        for word in self.words:


            btn = MDRaisedButton(
                text=word,
                size_hint_y=None,
                height=dp(45)
            )


            btn.bind(
                on_release=lambda x,
                w=word:
                self.select_word(w)
            )


            self.word_box.add_widget(btn)



    def select_word(self, word):


        if word in self.selected:

            self.selected.remove(word)


        elif len(self.selected) < 4:

            self.selected.append(word)



        self.info.text = (
            "Vybrané: "
            +
            ", ".join(self.selected)
            +
            "\n("
            +
            str(len(self.selected))
            +
            "/4)"
        )



    def new_words(self, button):

        self.words = generate_words()

        self.selected = []

        self.show_words()



    def create_story(self, button):


        if not is_open():

            self.info.text = "❌ Kolo je zatvorené"

            return



        if len(self.selected) != 4:

            self.info.text = "Vyber presne 4 slová"

            return



        story = generate_story(
            self.selected
        )


        score = random.randint(
            1,
            99
        )


        save_story(
            current_user,
            self.selected,
            story,
            score
        )


        self.manager.get_screen(
            "result"
        ).set_result(
            story,
            score
        )


        self.manager.current = "result"
# ======================================
# FEED SCREEN
# ČASŤ 2/5
# ======================================

class FeedScreen(MDScreen):

    def on_enter(self):

        self.clear_widgets()


        main = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15)
        )


        title = MDLabel(
            text=f"StoryFund - {current_user}",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=dp(50)
        )


        main.add_widget(title)


        scroll = MDScrollView()


        feed_box = MDBoxLayout(
            orientation="vertical",
            spacing=dp(15),
            size_hint_y=None
        )

        feed_box.bind(
            minimum_height=feed_box.setter("height")
        )


        try:

            stories = load_feed()


            for story in stories[-10:][::-1]:

                card = MDCard(
                    orientation="vertical",
                    padding=dp(15),
                    size_hint_y=None,
                    height=dp(180),
                    radius=[20]
                )


                text = (
                    "👤 "
                    + story["nik"]
                    +
                    "\n\n"
                    +
                    "Slová: "
                    +
                    ", ".join(story["words"])
                    +
                    "\n\n"
                    +
                    story["story"]
                    +
                    "\n\n⭐ Index: "
                    +
                    str(story["score"])
                    +
                    "%"
                )


                card.add_widget(
                    MDLabel(
                        text=text
                    )
                )


                feed_box.add_widget(card)


        except Exception as e:

            feed_box.add_widget(
                MDLabel(
                    text="Chyba načítania feedu:\n"
                    + str(e)
                )
            )


        scroll.add_widget(feed_box)

        main.add_widget(scroll)



        create_btn = MDRaisedButton(
            text="➕ NOVÝ PRÍBEH",
            pos_hint={"center_x": .5}
        )


        create_btn.bind(
            on_release=lambda x:
            setattr(
                self.manager,
                "current",
                "create"
            )
        )


        main.add_widget(create_btn)



        logout_btn = MDFlatButton(
            text="Odhlásiť"
        )


        logout_btn.bind(
            on_release=self.logout
        )


        main.add_widget(logout_btn)


        self.add_widget(main)



    def logout(self, button):

        global current_user

        current_user = None

        self.manager.current = "login"