import logging
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import speech_recognition as sr

from config import (
    AMBIENT_CALIBRATION_DURATION,
    ASSISTANT_NAMES,
    LISTEN_PHRASE_TIME_LIMIT,
    LOG_DIR,
    LOG_FILE,
    SLEEP_WORDS,
    WAKE_WORDS,
)
from llm import cevapla, warmup
from skills import dispatch
from tts import konus

os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)

asistan_uykuda = True


def _has_whole_word(text, words):
    for w in words:
        if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", text):
            return True
    return False


def _strip_name(text):
    out = text
    for name in ASSISTANT_NAMES:
        out = re.sub(rf"(?<!\w){re.escape(name)}(?!\w)", " ", out)
    return " ".join(out.split()).strip()


def _contains_name(text):
    return any(re.search(rf"(?<!\w){re.escape(name)}(?!\w)", text) for name in ASSISTANT_NAMES)


def komut_isle(text):
    global asistan_uykuda

    if _has_whole_word(text, SLEEP_WORDS):
        konus("Tamam, uyuyorum. Beni çağırırsan buradayım.")
        asistan_uykuda = True
        return

    komut = _strip_name(text)
    if not komut:
        konus("Efendim?")
        return

    skill_response = dispatch(komut)
    if skill_response:
        konus(skill_response)
        return

    konus(cevapla(komut))


def _create_recognizer():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.9
    recognizer.non_speaking_duration = 0.5
    return recognizer


def _listen_for_command(recognizer):
    """Open mic, capture one phrase, close mic. Returns recognized lowercase text or None."""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=AMBIENT_CALIBRATION_DURATION)
            logging.info(f"Dinleniyor (energy_threshold={recognizer.energy_threshold:.0f})")
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=LISTEN_PHRASE_TIME_LIMIT)
            logging.info("Ses yakalandi, STT'ye gonderiliyor")
    except sr.WaitTimeoutError:
        logging.info("15sn ses yok, yeniden dinleniyor")
        return None
    except OSError as e:
        logging.warning(f"Mikrofon hatasi: {e}")
        time.sleep(2)
        return None

    try:
        return recognizer.recognize_google(audio, language="tr-TR").lower()
    except sr.UnknownValueError:
        logging.info("STT sesi anlayamadi (UnknownValueError)")
        return None
    except sr.RequestError as e:
        logging.warning(f"STT baglanti hatasi: {e}")
        time.sleep(1)
        return None


def main():
    global asistan_uykuda

    recognizer = _create_recognizer()
    logging.info("Neom basliyor, uyku modunda")
    warmup()

    while True:
        try:
            text = _listen_for_command(recognizer)
            if not text:
                continue

            logging.info(f"Duyuldu: {text}")

            if asistan_uykuda:
                if any(w in text for w in WAKE_WORDS):
                    asistan_uykuda = False
                    konus("Buradayım, dinliyorum.")
                continue

            if not _contains_name(text):
                logging.info("Ad gecmedi, gormezden geliniyor")
                continue

            komut_isle(text)

        except KeyboardInterrupt:
            logging.info("KeyboardInterrupt ile kapaniyor")
            break
        except Exception as e:
            logging.exception(f"Ana dongu hatasi: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
