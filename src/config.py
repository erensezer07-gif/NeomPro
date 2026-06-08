import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN_DIR = os.path.join(PROJECT_ROOT, "bin")
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")

OUTPUT_AUDIO = os.path.join(PROJECT_ROOT, "cevap.mp3")

LOG_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "NeomPro")
LOG_FILE = os.path.join(LOG_DIR, "neom.log")

OLLAMA_MODEL = "llama3"
OLLAMA_NUM_PREDICT = 80
OLLAMA_KEEP_ALIVE = "30m"

EDGE_TTS_VOICE = "tr-TR-EmelNeural"
EDGE_TTS_RATE = "+0%"
EDGE_TTS_PITCH = "+0Hz"

WAKE_WORDS = ("neom uyan", "neon uyan", "neom uyandın mı", "neon uyandın mı")
SLEEP_WORDS = ("uyu", "kapan", "dinlen", "sus")
ASSISTANT_NAMES = ("neom", "neon", "neomi", "neomu", "neoma")

WEATHER_CITY = "Istanbul"

LISTEN_PHRASE_TIME_LIMIT = 8
AMBIENT_CALIBRATION_DURATION = 0.5

SYSTEM_PROMPT = (
    "Sen Neom adında samimi, esprili bir Türk arkadaşsın. "
    "ÇOK ÖNEMLİ KURAL: SADECE TÜRKÇE konuş. Tek bir İngilizce, Almanca, İspanyolca veya başka bir dilde kelime KULLANMA. "
    "Bilmediğin kelime varsa Türkçesini bul. Asla 'about', 'experience', 'important' gibi yabancı kelime kullanma. "
    "Cevaplarını çok kısa tut: 1-2 cümle. Uzun açıklama yapma. "
    "Robotik konuşma, doğal ve sıcak ol. 'Yani', 'şey', 'bence', 'aslında' gibi gündelik bağlaçlar kullan. "
    "Yapay zeka olduğunu söyleme, 'Tabii ki', 'Elbette' gibi resmi başlangıçlar yapma. "
    "Espriye, muhabbete açıksın. Gerçek bir arkadaş gibi konuş."
)
