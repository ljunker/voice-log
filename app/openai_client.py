from openai import OpenAI
from .settings import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_TONE_PROMPT = (
    "Du bist ein Assistent, der kurze Tagebuch-Notizen in einen "
    "klaren, formalen und gut lesbaren Stil umschreibt. "
    "Erhalte alle Fakten, Namen, Zeiten und Aufgaben. "
    "Schreibe in der **ersten Person Vergangenheit** "
    "und fasse die Inhalte präzise zusammen."
)


def transcribe_audio(path: str) -> tuple[str, int | None]:
    """Transcribe an audio file with OpenAI Audio API.
    Returns (text, duration_sec or None).
    """
    with open(path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model=settings.OPENAI_TRANSCRIBE_MODEL,
            language="de", # uncomment if your notes are primarily German
            # response_format="json"
        )
    # Depending on SDK, `text` field is standard for transcription result
    text = getattr(transcription, "text", None) or transcription.__dict__.get("text", "")
    # Duration is not always returned; keep None if absent
    duration = getattr(transcription, "duration", None) or transcription.__dict__.get("duration")
    return text, int(duration) if duration else None


def formalize_text(raw: str) -> str:
    resp = client.chat.completions.create(
        model=settings.OPENAI_TEXT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_TONE_PROMPT},
            {"role": "user", "content": raw},
        ],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
