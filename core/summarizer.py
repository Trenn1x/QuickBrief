from pathlib import Path
from llama_cpp import Llama

MODEL = Path(__file__).parents[1] / "models" / "phi2-q4.gguf"
SYS = """
You are a senior strategist.
Return a concise creative brief **in plain Markdown**.
Do NOT use code blocks or ``` fences.

Sections (all required):
## Brand Tone
## Audience Insights
## Campaign Objectives
## Creative Brief   <!-- bullet user stories, channel mix, KPIs -->
"""

def synthesize(text: str) -> str:
    llm = Llama(model_path=str(MODEL), n_gpu_layers=32)
    out = llm(f"{SYS}\n\nRAW NOTES:\n{text}\n\nBRIEF:", max_tokens=600)
    return out["choices"][0]["text"].strip()

