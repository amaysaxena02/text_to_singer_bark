# 🎙️ Text → Singer (Bark) — Streamlit App

Generate singing audio from lyrics using [Suno's Bark](https://github.com/suno-ai/bark). This app lets you paste lyrics, pick a voice preset, and produce a sung vocal clip.

> **Note**: Bark creates **text-to-audio** and can sing when prompted with musical cues (e.g., `♪ ... ♪`). It is not a full DAW; it outputs a single mono WAV with a vocal-like rendering (sometimes with slight accompaniment-like textures).

---

## 🔧 Quick Start

### 1) Create & activate a virtual environment (recommended)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
> ⚠️ Install the correct **PyTorch** wheel for your machine **before** installing the rest, especially on Windows.

- **CPU-only (Windows/macOS/Linux):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

- **NVIDIA GPU (CUDA 12.1):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

Then install the app deps:
```bash
pip install -r requirements.txt
```

If `bark` or `transformers` pull a different `tokenizers` version, reinstall:
```bash
pip install --upgrade tokenizers>=0.15.2
```

### 3) Run the app
```bash
streamlit run app.py
```

On first run Bark will download its models; this can take a few minutes depending on your connection. Subsequent runs are fast due to caching.

---

## 🎛️ Usage Tips

- Keep lines short and add punctuation for phrasing.
- Leaving **“Auto-add singing cues (♪ … ♪)”** ON helps Bark switch into a melodic style.
- Try different **voice presets** (e.g., `v2/en_speaker_6`) and tweak **temperature** (0.6–1.0 is a good range).
- If generation fails for a long paragraph, the app automatically falls back to **line-by-line** synthesis and stitches the clips.
- Output is saved to `outputs/bark_song_YYYYmmdd_HHMMSS.wav`.

---

## ❓ Troubleshooting

- **Long or complex lyrics timeout** → Try shorter input or use simpler wording; the app will also try per-line fallback.
- **Tokenizers version errors** → `pip install --upgrade tokenizers>=0.15.2`.
- **Torch installation issues (Windows)** → Ensure you used the *correct* index URL for CPU vs CUDA builds.
- **No singing quality** → Add more musical cues (`♪`, `la la la`, `ooh`, `[verse]`, `[chorus]`) and keep lines concise.

---

## 🧱 What this app is (and isn’t)

- ✅ Local, simple **text → sung audio** generator using Bark.
- ✅ Easy UI (Streamlit), with voice, temperature, seed, and top-k controls.
- ❌ It doesn’t accept MIDI or output multitrack stems.
- ❌ It’s not a full song arranger—use a DAW for mixing/instrumentals.

---

## 📄 License

This template is provided "as is". Please check the Bark license and model card for usage terms and attribution where applicable.
