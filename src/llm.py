"""LangChain prompt + HuggingFace LLM helper for grounded answer generation."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from langchain_core.prompts import PromptTemplate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from transformers.utils import logging as hf_logging


MODEL_NAME = "google/flan-t5-small"
ROOT = Path(__file__).resolve().parents[1]

PROMPT = PromptTemplate.from_template(
    """Use only the evidence to answer the support question.
Keep the answer short and do not add facts that are not in the evidence.

Question: {question}

Evidence:
{evidence}

Answer:"""
)


def generate_llm_answer(question: str, evidence: str) -> str:
    prompt = PROMPT.format(question=question, evidence=evidence)
    try:
        generator = _pipeline()
        result = generator(prompt, max_new_tokens=96, do_sample=False)[0]["generated_text"].strip()
        return result
    except Exception:
        return ""


@lru_cache(maxsize=1)
def _pipeline():
    hf_logging.set_verbosity_error()
    cache_dir = os.environ.get("HF_HOME", str(ROOT / ".hf_cache"))
    model_cache = Path(cache_dir) / "models--google--flan-t5-small"
    local_only = model_cache.exists() or os.environ.get("SUPPORTDESK_LLM_LOCAL_ONLY") == "1"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=cache_dir, local_files_only=local_only)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, cache_dir=cache_dir, local_files_only=local_only)
    return pipeline("text2text-generation", model=model, tokenizer=tokenizer)
