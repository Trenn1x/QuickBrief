"""Generate a one-page creative brief from raw discovery notes."""

from core.llm import chat   # wrapper around llama-cpp
import textwrap

# --- 1. System role ----------------------------------------------------------
SYSTEM = textwrap.dedent("""
    You are **BriefSynth**, a senior brand strategist.
    Your job: turn messy discovery-call notes into a tight *one-page* creative
    brief.  Use the following outline and **Markdown** formatting:

    1. **Objective** – 1 sentence
    2. **Audience insight** – 2 – 3 bullet points
    3. **Single-minded proposition**
    4. **Channel mix** – table: Channel | Rationale
    5. **KPIs / success metrics**
    6. **Next-step action items** – checklist

    • Keep total length ≈350 – 450 words  
    • Do **NOT** invent facts—summarize what’s in the notes.  
    • Use clear agency language, no jargon fluff.
""").strip()

# --- 2. Main helper ----------------------------------------------------------
def synthesize(notes: str) -> str:
    if not notes.strip():
        raise ValueError("No notes provided")

    prompt = [
        {"role": "system", "content": SYSTEM},
        {"role": "user",   "content": notes.strip()},
    ]

    # You can adjust temperature / top_p here if desired
    return chat(
        prompt,
        max_tokens=600,        # hard stop so we stay <512 total ctx
        temperature=0.7,
        top_p=0.9,
    )

