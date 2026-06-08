# NeomPro

Türkçe sesli yapay zeka asistanı. Bilgisayar açılınca arka planda gizli çalışır, "**Neom uyan**" demenle uyanır, samimi bir arkadaş gibi muhabbet eder, sistem işlerini yapar, "**Neom uyu**" deyince tekrar uyku moduna geçer.

- **STT**: Google Speech Recognition (online, ücretsiz)
- **LLM**: Ollama + llama3.2:3b (tamamen lokal, hızlı yanıt)
- **TTS**: Microsoft Edge TTS, `tr-TR-EmelNeural` (online, ücretsiz, doğal nöral ses)
- **Lokal yedek TTS**: Piper modeli ve binary'leri `bin/` + `models/tts/` altında duruyor (gerekirse `tts.py` Piper'a geri çevrilebilir)

## Klasör Yapısı

```
NeomPro/
├── src/                          # Python kaynak kodu
│   ├── main.py                   # Giriş noktası ve dinleme döngüsü
│   ├── config.py                 # Yollar, sabitler, sistem promptu
│   ├── tts.py                    # Piper ile seslendirme
│   ├── llm.py                    # Ollama ile sohbet
│   ├── skills.py                 # Sistem komutları (uygulama aç, hava, ses vb.)
│   └── tools/
│       └── list_voices.py        # Yardımcı: pyttsx3 ses listesi
├── bin/                          # Piper EXE + DLL + espeak-ng-data
├── models/tts/                   # Piper Türkçe ses modeli
├── scripts/
│   ├── install_autostart.ps1     # Boot'ta otomatik başlatma kur
│   ├── install_autostart.bat     #   (kolay tıklama için)
│   ├── uninstall_autostart.ps1   # Kaldır
│   └── uninstall_autostart.bat
├── requirements.txt
├── run.bat                       # Konsol açık şekilde başlat (debug)
├── run-silent.bat                # Konsolsuz başlat (pythonw)
└── README.md
```

## Kurulum

### 1. Python paketleri
```powershell
pip install -r requirements.txt
```

### 2. Ollama
[ollama.com](https://ollama.com/) sitesinden Ollama'yı kurun, sonra:
```powershell
ollama pull llama3
```
Ollama Windows'ta açılışta arka planda otomatik çalışır.

### 3. Otomatik başlatma (boot'ta gizli çalışsın)
[scripts/install_autostart.bat](scripts/install_autostart.bat) dosyasına çift tıklayın.

Bu, **NeomAsistan** adında bir Görev Zamanlayıcı görevi oluşturur:
- Oturum açıldığında otomatik başlar
- `pythonw.exe` ile konsolsuz çalışır
- Çökerse 3 kez yeniden başlatır
- Süre limiti yoktur

Kaldırmak için [scripts/uninstall_autostart.bat](scripts/uninstall_autostart.bat).

## Kullanım

Asistan açılışta **uyku modunda** başlar. Mikrofon hep dinlemededir ama yalnızca uyandırma kelimesine tepki verir.

| Komut | Sonuç |
|---|---|
| **Neom uyan** | Uyandırır, dinleme moduna alır |
| **Neom uyu** / **kapan** / **sus** | Uyku moduna döner |

### Sohbet
Uyandıktan sonra normal konuş — sistem komutu değilse llama3'e gider, samimi arkadaş tarzında cevaplar.

### Sistem komutları (dispatcher)

**Bilgi**
- "saat kaç"
- "bugün ne, tarih ne"
- "hava nasıl" (varsayılan şehir [config.py](src/config.py)'de — `WEATHER_CITY`)

**Uygulama açma** (chrome, edge, firefox, spotify, notepad, calc, vs code, explorer, ayarlar, discord, steam, telegram, whatsapp)
- "chrome aç"
- "spotify aç"
- "hesap makinesi aç"

**Web**
- "google aç" / "youtube aç"
- "google'da kedi videoları ara"
- "youtube'da lofi ara"

**Ses kontrolü**
- "sesi aç" / "sesi kıs" / "sesi kapat" / "sustur"

**Sistem**
- "bilgisayarı kilitle"
- "bilgisayarı kapat" (1 dk gecikme, iptal edilebilir)
- "bilgisayarı yeniden başlat"
- "kapanmayı iptal et"
- "ekran görüntüsü al"

**Diğer**
- "klasör aç" → proje klasörünü açar

## Manuel çalıştırma

Debug (konsol görünür):
```powershell
.\run.bat
```

Sessiz (pythonw, arka planda):
```powershell
.\run-silent.bat
```

## Loglar

Çalışma kayıtları: `%LOCALAPPDATA%\NeomPro\neom.log`

Sorun yaşarsanız bu dosyaya bakın.

## Sistem promptu / kişilik

Asistanın karakteri [src/config.py](src/config.py) içindeki `SYSTEM_PROMPT` değişkeninde. Daha resmi veya daha samimi yapmak için orayı düzenleyin.

## Yeni komut eklemek

[src/skills.py](src/skills.py) içindeki `dispatch()` fonksiyonuna yeni bir koşul ekleyin. Eğer dispatcher `None` döndürürse komut otomatik olarak LLM'e gider.
