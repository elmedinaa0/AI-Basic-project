from gtts import gTTS
from playsound3 import playsound
import os
import time
import uuid

def speak(text: str, lang: str = "en"):
    if not text.strip():
        return

    filename = f"speech_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    time.sleep(0.2)
    playsound(filename)

    try:
        os.remove(filename)
    except:
        pass
