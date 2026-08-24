import traceback
from jnius import autoclass

PythonActivity = autoclass("org.kivy.android.PythonActivity")
ContentValues = autoclass("android.content.ContentValues")
MediaStore = autoclass("android.provider.MediaStore")


def write_crash(text):
    try:
        activity = PythonActivity.mActivity
        resolver = activity.getContentResolver()

        values = ContentValues()

        values.put(
            MediaStore.MediaColumns.DISPLAY_NAME,
            "StoryFund_crash.txt"
        )

        values.put(
            MediaStore.MediaColumns.MIME_TYPE,
            "text/plain"
        )

        values.put(
            MediaStore.MediaColumns.RELATIVE_PATH,
            "Documents/StoryFund"
        )

        collection = MediaStore.Files.getContentUri("external")

        uri = resolver.insert(
            collection,
            values
        )

        if uri is not None:
            stream = resolver.openOutputStream(uri)

            stream.write(
                text.encode("utf-8")
            )

            stream.close()

    except Exception:
        pass


try:

    write_crash(
        "StoryFund Python STARTED\n"
    )

    from app import StoryFundApp

    write_crash(
        "app import OK\n"
    )

    if __name__ == "__main__":

        write_crash(
            "starting StoryFundApp...\n"
        )

        StoryFundApp().run()


except BaseException:

    write_crash(
        "\n===== CRASH =====\n" +
        traceback.format_exc()
    )

    raise
