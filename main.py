import traceback

try:
    from app import StoryFundApp

    if __name__ == "__main__":
        StoryFundApp().run()

except Exception:
    try:
        with open("/sdcard/StoryFund_crash.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
    except Exception:
        pass
    raise
