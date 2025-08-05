"""Thin wrapper around llama-cpp so the rest of the code can just call `chat()`."""

from pathlib import Path
from functools import lru_cache
from llama_cpp import Llama

# ---------- model path & loading --------------------------------------------
MODEL_PATH = Path(__file__).parents[1] / "models" / "phi2-q4.gguf"

@lru_cache(maxsize=1)          # load once, reuse for every call
def _get_model() -> Llama:
    return Llama(model_path=str(MODEL_PATH), n_gpu_layers=32)

# ---------- public helper ----------------------------------------------------
def chat(
    messages: list[dict],
    max_tokens: int = 600,
    temperature: float = 0.7,
    top_p: float = 0.9,
):
    """
    Minimal chat wrapper that turns `[{"role":"system",...}, …]` into a prompt
    llama-cpp understands, then returns the generated text.
    """

    prompt_parts = []
    for m in messages:
        role = m["role"]
        content = m["content"].strip()

        if role == "system":
            prompt_parts.append(f"<<SYS>>\n{content}\n<</SYS>>")
        elif role == "user":
            prompt_parts.append(f"[INST] {content} [/INST]")
        else:                       # assistant / other
            prompt_parts.append(content)

    prompt = "\n".join(prompt_parts) + "\n"

    llm = _get_model()
    out = llm(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
    )
    return out["choices"][0]["text"].strip()

