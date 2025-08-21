import streamlit as st
import numpy as np
import soundfile as sf
from datetime import datetime
from pathlib import Path

# Bark imports
from bark import SAMPLE_RATE, generate_audio, preload_models
# from bark.generation import set_seed

# -----------------------------
# Utilities
# -----------------------------
def prepare_lyrics_for_singing(text: str, add_notes: bool = True) -> str:
    """
    Bark tends to 'sing' if we add musical markers and keep lines short.
    This helper lightly formats the lyrics.
    """
    text = text.strip()
    if not text:
        return text
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        lines = [text]
    # Add simple stanza tags and musical notes to encourage melody-like prosody
    joined = []
    for i, ln in enumerate(lines, 1):
        if add_notes:
            ln = f"♪ {ln} ♪"
        joined.append(ln)
    return "[verse]\n" + "\n".join(joined)

@st.cache_resource(show_spinner=False)
def _preload_bark_models():
    # Downloads and caches Bark models on first run
    preload_models()

def concat_clips(clips):
    if not clips:
        return np.zeros((0,), dtype=np.float32)
    return np.concatenate(clips, axis=0)

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Text → Singer (Bark)", page_icon="🎙", layout="centered")

st.title("🎙 Text → Singer (Bark)")
st.caption("Type lyrics, pick a voice, and generate sung audio locally with Suno's Bark.")

with st.expander("Tips for better singing"):
    st.markdown(
        "- Keep lines short (1 phrase per line).\n"
        "- Add punctuation and onomatopoeia (la, na, ooh) for melody.\n"
        "- Try different voices and temperature.\n"
        "- Example:\n\n"
        "\n"
        "Twinkle, twinkle, little star\n"
        "How I wonder what you are\n"
        "Up above the world so high\n"
        "Like a diamond in the sky\n"
        "\n"
    )

lyrics = st.text_area(
    "Lyrics",
    value="Twinkle, twinkle, little star\nHow I wonder what you are\nUp above the world so high\nLike a diamond in the sky",
    height=200,
    placeholder="Paste or type your lyrics here...",
)

col1, col2 = st.columns(2)
with col1:
    add_sing_helpers = st.checkbox("Auto-add singing cues (♪ ... ♪)", True)
with col2:
    temperature = st.slider("Temperature", 0.1, 1.5, 0.8, 0.05)

# Bark voice presets (common English voices). You can try others like: 'v2/en_speaker_6'
voice_presets = [
    "v2/en_speaker_1", "v2/en_speaker_2", "v2/en_speaker_3", "v2/en_speaker_4",
    "v2/en_speaker_5", "v2/en_speaker_6", "v2/en_speaker_7", "v2/en_speaker_8",
    "v2/en_speaker_9", "v2/en_speaker_10",
    "en_speaker_1", "en_speaker_2", "en_speaker_3", "en_speaker_4", "en_speaker_5",
    "en_speaker_6", "en_speaker_7", "en_speaker_8", "en_speaker_9", "en_speaker_10",
]

c1, c2, c3 = st.columns([1,1,1])
with c1:
    voice = st.selectbox("Voice preset", voice_presets, index=0)
with c2:
    seed = st.number_input("Seed (reproducibility)", value=42, min_value=0, step=1)
with c3:
    top_k = st.slider("Top-k", 1, 100, 50, 1)

st.divider()

gen_btn = st.button("Generate Singing", type="primary")

if gen_btn:
    if not lyrics.strip():
        st.error("Please enter some lyrics.")
        st.stop()

    # Prepare text to encourage singing
    formatted = prepare_lyrics_for_singing(lyrics, add_notes=add_sing_helpers)

    with st.spinner("Loading models (first run may take a while)..."):
        _preload_bark_models()

    np.random.seed(int(seed))

    # Bark can be called on the whole text; for more control, you can split by lines and concatenate.
    # Here we try whole text first, which works well for short/medium lyrics.
    try:
        audio_array = generate_audio(
            formatted,
            history_prompt=voice,
        )
    except Exception as e:
        st.warning(f"Direct generation failed ({e}). Trying line-by-line fallback...")
        clips = []
        for line in formatted.splitlines():
            if not line.strip():
                continue
            try:
                clip = generate_audio(
                    line,
                    history_prompt=voice,
                )
                clips.append(clip)
            except Exception as ie:
                st.error(f"Failed on line: {line}\n{ie}")
        audio_array = concat_clips(clips)

    if audio_array is None or len(audio_array) == 0:
        st.error("No audio generated. Try shorter lyrics or a different voice/temperature.")
        st.stop()

    # Save and present
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    wav_path = out_dir / f"bark_song_{ts}.wav"
    sf.write(wav_path, audio_array, SAMPLE_RATE)

    st.success("Done!")
    st.audio(str(wav_path), format="audio/wav")

    with open(wav_path, "rb") as f:
        st.download_button("Download .wav", data=f, file_name=wav_path.name, mime="audio/wav")

    st.caption(f"Saved to: {wav_path.resolve()}")