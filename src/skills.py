import datetime
import logging
import os
import re
import subprocess
import urllib.parse
import urllib.request
import webbrowser

from config import PROJECT_ROOT, WEATHER_CITY

APPS = {
    "chrome": "chrome",
    "edge": "msedge",
    "firefox": "firefox",
    "spotify": "spotify",
    "not defteri": "notepad",
    "notepad": "notepad",
    "hesap makinesi": "calc",
    "hesap makinası": "calc",
    "kalkülatör": "calc",
    "vs code": "code",
    "visual studio code": "code",
    "explorer": "explorer",
    "dosya gezgini": "explorer",
    "ayarlar": "ms-settings:",
    "discord": "discord",
    "steam": "steam",
    "telegram": "telegram",
    "whatsapp": "whatsapp",
}

_TR_DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
_TR_MONTHS = [
    "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
]


def _open_app(query):
    for name, cmd in APPS.items():
        if name in query:
            try:
                if cmd.startswith("ms-settings:"):
                    os.startfile(cmd)
                else:
                    subprocess.Popen(cmd, shell=True)
                return f"{name.capitalize()} açılıyor."
            except Exception as e:
                logging.warning(f"{name} acilamadi: {e}")
                return f"{name} açamadım."
    return None


def _strip_search_query(text, *keywords):
    q = text
    for k in keywords:
        q = q.replace(k, " ")
    q = re.sub(r"\s+", " ", q).strip(" '")
    return q


def _search_web(text):
    if "youtube" in text:
        q = _strip_search_query(text, "youtube", "'da", "'de", "da", "de", "ara", "aç")
        if q:
            webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}")
            return f"YouTube'da {q} aranıyor."
    q = _strip_search_query(text, "google", "'da", "'de", "ara", "internette")
    if q:
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote(q)}")
        return f"{q} aranıyor."
    return None


def _get_time():
    return f"Saat {datetime.datetime.now().strftime('%H:%M')}."


def _get_date():
    now = datetime.datetime.now()
    return f"Bugün {now.day} {_TR_MONTHS[now.month - 1]} {now.year}, {_TR_DAYS[now.weekday()]}."


def _get_weather():
    try:
        url = f"https://wttr.in/{urllib.parse.quote(WEATHER_CITY)}?format=%l:+%C+%t&lang=tr"
        req = urllib.request.Request(url, headers={"User-Agent": "curl"})
        with urllib.request.urlopen(req, timeout=5) as r:
            text = r.read().decode("utf-8", errors="ignore").strip()
        return f"Hava durumu — {text}"
    except Exception as e:
        logging.warning(f"Hava durumu alinamadi: {e}")
        return "Hava durumunu şu an alamıyorum."


def _send_media_key(key_code):
    cmd = (
        "powershell -NoProfile -WindowStyle Hidden -Command "
        f"\"(New-Object -ComObject WScript.Shell).SendKeys([char]{key_code})\""
    )
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _volume_up():
    for _ in range(4):
        _send_media_key(175)
    return "Sesi açtım."


def _volume_down():
    for _ in range(4):
        _send_media_key(174)
    return "Sesi kıstım."


def _volume_mute():
    _send_media_key(173)
    return "Sesi kapattım."


def _lock_computer():
    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
    return "Bilgisayarı kilitliyorum."


def _shutdown_computer():
    subprocess.run(["shutdown", "/s", "/t", "60"], shell=True)
    return "Bilgisayar bir dakika sonra kapanacak. İptal etmek için 'kapanmayı iptal et' de."


def _cancel_shutdown():
    subprocess.run(["shutdown", "/a"], shell=True)
    return "Kapanmayı iptal ettim."


def _restart_computer():
    subprocess.run(["shutdown", "/r", "/t", "60"], shell=True)
    return "Bilgisayar bir dakika sonra yeniden başlayacak. İptal için 'kapanmayı iptal et' de."


def _screenshot():
    try:
        from PIL import ImageGrab
    except ImportError:
        return "Ekran görüntüsü için Pillow kurulu değil."
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        os.makedirs(desktop, exist_ok=True)
        path = os.path.join(desktop, f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        ImageGrab.grab().save(path)
        return "Ekran görüntüsünü masaüstüne kaydettim."
    except Exception as e:
        logging.exception(f"Screenshot hatasi: {e}")
        return "Ekran görüntüsü alamadım."


def _open_project_folder():
    os.startfile(PROJECT_ROOT)
    return "Klasörü açtım."


def dispatch(text):
    """Routes a recognized command. Returns response string or None if unhandled."""
    t = text.lower().strip()

    if "iptal" in t and ("kapan" in t or "kapat" in t or "yeniden başlat" in t):
        return _cancel_shutdown()
    if "yeniden başlat" in t and "bilgisayar" in t:
        return _restart_computer()
    if ("bilgisayarı kapat" in t or "sistemi kapat" in t) and "iptal" not in t:
        return _shutdown_computer()
    if any(w in t for w in ("bilgisayarı kilitle", "ekranı kilitle", "kilitle bilgisayar")):
        return _lock_computer()
    if "ekran görüntüsü" in t or "screenshot" in t:
        return _screenshot()

    if "sesi kapat" in t or "sustur" in t:
        return _volume_mute()
    if any(w in t for w in ("sesi aç", "ses aç", "sesi yükselt", "sesi arttır", "sesi artır")):
        return _volume_up()
    if any(w in t for w in ("sesi kıs", "ses kıs", "sesi azalt", "sesi düşür")):
        return _volume_down()

    if re.search(r"\bsaat\b", t) and re.search(r"\bka[çc]\b", t):
        return _get_time()
    date_phrases = (
        "tarih ne", "tarihi söyle", "tarihi öğren",
        "bugün ayın kaçı", "ayın kaçı", "ayin kaci",
        "hangi gün", "ne günü", "ne günündeyiz",
        "günlerden ne", "bugün ne tarihi",
    )
    if any(p in t for p in date_phrases):
        return _get_date()
    if "hava durumu" in t or (re.search(r"\bhava\b", t) and ("nasıl" in t or "kaç derece" in t)):
        return _get_weather()

    if "klasör aç" in t or "dosyaları aç" in t or "proje aç" in t:
        return _open_project_folder()
    if "google aç" in t or "google'ı aç" in t:
        webbrowser.open("https://www.google.com")
        return "Google açıldı."
    if "youtube aç" in t or "youtube'u aç" in t:
        webbrowser.open("https://www.youtube.com")
        return "YouTube açıldı."

    if "ara" in t and ("google" in t or "youtube" in t or "internette" in t):
        res = _search_web(t)
        if res:
            return res

    if " aç" in t or t.endswith(" aç") or t.startswith("aç"):
        res = _open_app(t)
        if res:
            return res

    if "ara" in t:
        res = _search_web(t)
        if res:
            return res

    return None
