"""
blend_swahili.py
Downloads and blends multiple Swahili datasets into one unified instruction-tuning JSONL.
Output: data/swahili_blended/train.jsonl + validation.jsonl
"""

import json
import random
import os
import requests
import tempfile
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
SOURCES_FILE = OUTPUT_DIR / "sources.json"
SEED = 42
random.seed(SEED)

HF_TOKEN = os.environ.get("HF_TOKEN", None)
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def download_hf_file(url, output_path):
    """Download a file from Hugging Face with optional auth."""
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(r.content)

def try_load_via_datasets(hf_path, split="train"):
    """Try loading via the datasets library. Returns None on failure."""
    try:
        from datasets import load_dataset
        ds = load_dataset(hf_path, split=split, trust_remote_code=True)
        return ds
    except Exception as e:
        print(f"    datasets library failed: {e}")
        return None

def load_finetome():
    """Load ngusadeep/Swahili-FineTome-20k - ~18K instruction pairs (instruction/output columns)."""
    rows = []
    try:
        from datasets import load_dataset
        print("  Loading ngusadeep/Swahili-FineTome-20k...")
        ds = load_dataset("ngusadeep/Swahili-FineTome-20k", split="train", trust_remote_code=True)
        for item in ds:
            inst = str(item.get("instruction", "")).strip()
            resp = str(item.get("output", "")).strip()
            if inst and resp:
                rows.append({"instruction": inst, "response": resp, "source": "FineTome-20k-sw"})
        print(f"  FineTome-20k-sw: {len(rows)} rows")
        return rows
    except Exception as e:
        print(f"  FineTome-20k-sw: FAILED - {e}")
        return rows

def load_kenswquad():
    """Load Kencorpus/KenSwQuAD - download parquet directly. (plain answer string)"""
    rows = []
    parquet_url = "https://huggingface.co/datasets/Kencorpus/KenSwQuAD/resolve/main/train.parquet"
    try:
        print("  Downloading KenSwQuAD parquet directly...")
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as tmp:
            tmp_path = tmp.name
        download_hf_file(parquet_url, tmp_path)
        import pandas as pd
        df = pd.read_parquet(tmp_path)
        os.unlink(tmp_path)
        for _, item in df.iterrows():
            context = str(item.get("context", "")).strip()
            question = str(item.get("question", "")).strip()
            answer = str(item.get("answer", "")).strip()
            if question and answer:
                instruction = f"Soma kifungu kifuatacho kisha ujibu swali.\n\nKifungu: {context}\n\nSwali: {question}"
                rows.append({"instruction": instruction, "response": answer, "source": "KenSwQuAD"})
        print(f"  KenSwQuAD: {len(rows)} rows")
        return rows
    except Exception as e:
        print(f"  KenSwQuAD: FAILED - {e}")
        return rows

def load_code_swahili(sample_n=15000):
    """Load michsethowusu/Code-170k-swahili."""
    rows = []
    try:
        from datasets import load_dataset
        ds = load_dataset("michsethowusu/Code-170k-swahili", split="train", trust_remote_code=True)
        indices = list(range(len(ds)))
        sampled = random.sample(indices, min(sample_n, len(indices)))
        for idx in sampled:
            item = ds[idx]
            conv = item.get("conversations", [])
            if len(conv) >= 2:
                inst = conv[0].get("value", "").strip()
                resp = conv[1].get("value", "").strip()
                if inst and resp:
                    rows.append({"instruction": inst, "response": resp, "source": "Code-170k-swahili"})
        print(f"  Code-170k-swahili: {len(rows)} rows")
        return rows
    except Exception as e:
        print(f"  Code-170k-swahili: FAILED - {e}")
        return rows

def load_swahili_corpus(sample_n=15000):
    """Load ngusadeep/Swahili-Corpus-Dataset - raw Swahili text, convert to instruction format."""
    rows = []
    try:
        from datasets import load_dataset
        print("  Loading Swahili-Corpus-Dataset as pretraining text...")
        ds = load_dataset("ngusadeep/Swahili-Corpus-Dataset", split="train", trust_remote_code=True)
        indices = list(range(len(ds)))
        sampled = random.sample(indices, min(sample_n, len(indices)))
        prompts = [
            "Eleza kuhusu mada ifuatayo kwa Kiswahili:",
            "Andika kuhusu mada hii:",
            "Toa maelezo kuhusu:",
            "Fafanua kwa kina:",
        ]
        for idx in sampled:
            item = ds[idx]
            text = item.get("text", item.get("content", "")).strip()
            if not text:
                continue
            if len(text) < 50:
                continue
            instruction = random.choice(prompts)
            text_truncated = text[:1500] if len(text) > 1500 else text
            rows.append({"instruction": instruction, "response": text_truncated, "source": "Swahili-Corpus"})
        print(f"  Swahili-Corpus: {len(rows)} rows")
        return rows
    except Exception as e:
        print(f"  Swahili-Corpus: FAILED - {e}")
        return rows

def load_nile_exposure(sample_n=10000):
    """Load nileagi/swahili-language-exposure-v2 as backup raw text."""
    rows = []
    try:
        from datasets import load_dataset
        print("  Loading nileagi/swahili-language-exposure-v2...")
        ds = load_dataset("nileagi/swahili-language-exposure-v2", split="train", trust_remote_code=True)
        indices = list(range(len(ds)))
        sampled = random.sample(indices, min(sample_n, len(indices)))
        prompts = [
            "Eleza kuhusu mada ifuatayo kwa Kiswahili:",
            "Andika kuhusu mada hii:",
            "Toa maelezo kuhusu:",
            "Fafanua kwa kina:",
        ]
        for idx in sampled:
            item = ds[idx]
            text = item.get("text", item.get("content", "")).strip()
            if not text:
                continue
            if len(text) < 50:
                continue
            instruction = random.choice(prompts)
            text_truncated = text[:1500] if len(text) > 1500 else text
            rows.append({"instruction": instruction, "response": text_truncated, "source": "Swahili-Exposure"})
        print(f"  Swahili-Exposure: {len(rows)} rows")
        return rows
    except Exception as e:
        print(f"  Swahili-Exposure: FAILED - {e}")
        return rows

def main():
    print("=== Blending Swahili Datasets ===\n")

    all_rows = []
    source_counts = {}

    print("1/5 Loading FineTome-20k-sw...")
    rows = load_finetome()
    all_rows.extend(rows)
    source_counts["FineTome-20k-sw"] = len(rows)

    print("\n2/5 Loading KenSwQuAD...")
    rows = load_kenswquad()
    all_rows.extend(rows)
    source_counts["KenSwQuAD"] = len(rows)

    print("\n3/5 Loading Code-170k-swahili...")
    rows = load_code_swahili(sample_n=15000)
    all_rows.extend(rows)
    source_counts["Code-170k-swahili"] = len(rows)

    print("\n4/5 Loading Swahili-Corpus-Dataset...")
    rows = load_swahili_corpus(sample_n=15000)
    all_rows.extend(rows)
    source_counts["Swahili-Corpus"] = len(rows)

    # Skipping Swahili-Exposure-V2 (1GB+ download, raw text overlap with Swahili-Corpus)

    print(f"\nTotal before dedup: {len(all_rows)} rows")
    random.shuffle(all_rows)

    seen = set()
    deduped = []
    for row in all_rows:
        key = (row["instruction"][:80], row["response"][:80])
        if key not in seen:
            seen.add(key)
            deduped.append(row)

    print(f"Total after dedup: {len(deduped)} rows")
    random.shuffle(deduped)

    split_idx = int(len(deduped) * 0.95)
    train = deduped[:split_idx]
    validation = deduped[split_idx:]

    base = OUTPUT_DIR / "swahili_blended"
    train_file = base / "train.jsonl"
    val_file = base / "validation.jsonl"
    os.makedirs(base, exist_ok=True)

    with open(train_file, "w", encoding="utf-8") as f:
        for row in train:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    with open(val_file, "w", encoding="utf-8") as f:
        for row in validation:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"\nSaved:")
    print(f"  {train_file} ({len(train)} rows)")
    print(f"  {val_file} ({len(validation)} rows)")

    source_info = {
        "seed": SEED,
        "sources": {k: {"rows": v} for k, v in source_counts.items()},
        "total_before_dedup": len(all_rows),
        "total_after_dedup": len(deduped),
        "train_rows": len(train),
        "validation_rows": len(validation)
    }
    with open(SOURCES_FILE, "w", encoding="utf-8") as f:
        json.dump(source_info, f, indent=2, ensure_ascii=False)

    print(f"\nSources saved to {SOURCES_FILE}")
    print("=== Done ===")

if __name__ == "__main__":
    main()
