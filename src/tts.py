import asyncio
import logging
import os

import edge_tts
import pygame

from config import EDGE_TTS_PITCH, EDGE_TTS_RATE, EDGE_TTS_VOICE, OUTPUT_AUDIO

_mixer_ready = False
_speaking = False


def _ensure_mixer():
    global _mixer_ready
    if _mixer_ready:
        return
    try:
        pygame.mixer.init()
        _mixer_ready = True
    except Exception as e:
        logging.error(f"pygame.mixer baslatilamadi: {e}")


async def _synthesize(text):
    communicate = edge_tts.Communicate(
        text,
        voice=EDGE_TTS_VOICE,
        rate=EDGE_TTS_RATE,
        pitch=EDGE_TTS_PITCH,
    )
    await communicate.save(OUTPUT_AUDIO)


def is_speaking():
    return _speaking


def konus(metin):
    global _speaking
    if not metin:
        return
    metin = metin.strip()
    logging.info(f"[Neom]: {metin}")
    print(f"[Neom]: {metin}")
    _ensure_mixer()

    try:
        asyncio.run(_synthesize(metin))
    except Exception as e:
        logging.exception(f"Edge TTS hatasi: {e}")
        return

    if not os.path.exists(OUTPUT_AUDIO):
        logging.warning("TTS ses dosyasi uretemedi")
        return

    try:
        _speaking = True
        if _mixer_ready:
            pygame.mixer.music.load(OUTPUT_AUDIO)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(20)
            pygame.mixer.music.unload()
    except Exception as e:
        logging.exception(f"Ses oynatma hatasi: {e}")
    finally:
        _speaking = False
        try:
            os.remove(OUTPUT_AUDIO)
        except OSError:
            pass
