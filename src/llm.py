import logging

import ollama

from config import OLLAMA_KEEP_ALIVE, OLLAMA_MODEL, OLLAMA_NUM_PREDICT, SYSTEM_PROMPT


def warmup():
    """Model'i ve sistem promptunu KV cache'e onceden yukler."""
    try:
        ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "merhaba"},
            ],
            options={"num_predict": 1},
            keep_alive=OLLAMA_KEEP_ALIVE,
        )
        logging.info(f"Ollama model {OLLAMA_MODEL} on yuklendi (system prompt KV cache hazir)")
    except Exception as e:
        logging.warning(f"Warmup basarisiz: {e}")


def cevapla(soru):
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": soru},
            ],
            options={"num_predict": OLLAMA_NUM_PREDICT},
            keep_alive=OLLAMA_KEEP_ALIVE,
        )
        return response["message"]["content"].strip()
    except Exception as e:
        logging.exception(f"Ollama hatasi: {e}")
        return "Şu an düşünemiyorum, Ollama'ya ulaşamadım."
