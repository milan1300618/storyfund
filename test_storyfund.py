from backend import (
    create_user,
    login_user,
    load_feed
)

from words import generate_words

from story_engine import generate_story


print("BACKEND OK")

u = create_user()

print("NOVY UCET:")
print(u)


print("LOGIN:")
print(
    login_user(
        u["nik"],
        u["pin"]
    )
)


words = generate_words()

print("SLOVA:")
print(words)


print("TEST PRIBEHU:")
print(
    generate_story(
        words[:4]
    )
)


print("FEED:")
print(
    load_feed()
)