# Kiswahili AI — Swahili Instruction Model

> Team Omni — Adaption AutoScientist Challenge 2026 (Language Category)
> HackIndia AI Agents Hackathon 2026 — Adaption Adaptive Data Track

## Overview

Kiswahili AI is a Swahili instruction-tuned language model fine-tuned from **Llama-4-Scout-17B-16E-Instruct (109B MoE)** using **AutoScientist** by Adaption Labs. It combines **4 public Swahili datasets** into a unified instruction dataset (~52K rows), processes them through **Adaptive Data** for quality enhancement, and trains via AutoScientist's closed-loop co-optimization.

**Result**: **73% win rate** (adapted) vs **27%** (baseline) — **+170% relative improvement** on Adaption's held-out test set.

**Why Swahili?** Over 100 million speakers across East Africa. Swahili is a low-resource language where current LLMs show a 28-45% performance gap compared to English.

## Results

| Metric | Baseline | Adapted | Improvement |
|--------|:--------:|:-------:|:-----------:|
| Win Rate | 27% | 73% | **+170%** |
| General Category Win Rate | 31% | 69% | **+123%** |
| Dataset Grade | D (6.9th percentile) | B (25.6th percentile) | **+62%** |

## Dataset

Blended from 4 public Swahili datasets:

| Source | Rows | Type |
|--------|:----:|------|
| FineTome-20k-sw | 17,982 | General instruction |
| KenSwQuAD | 7,506 | Extractive QA |
| Code-170k-swahili | 14,969 | Code conversations |
| Swahili-Corpus-Dataset | 12,267 | Raw text (converted to instruction) |
| **Total** | **52,118** (after dedup) | |

### Adaptive Data Processing

Applied 3 recipes:
- **Prompt Deduplication** — removed near-duplicate prompts
- **Reasoning Traces** — added chain-of-thought steps
- **Hallucination Mitigation** — grounded responses in context

Quality improved from **Grade D (6.9th percentile)** to **Grade B (25.6th percentile)**, a **+62% relative improvement**.

## Training

| Setting | Value |
|---------|-------|
| **Base Model** | meta-llama/Llama-4-Scout-17B-16E-Instruct (109B MoE) |
| **Method** | SFT with LoRA (r=64, alpha=128, all-linear) |
| **Epochs** | 1 |
| **Batch Size** | max |
| **Learning Rate** | 0.0001 (cosine scheduler) |
| **Warmup Ratio** | 0.03 |
| **Weight Decay** | 0.02 |
| **Platform** | AutoScientist by Adaption Labs |

## Pipeline

```
Public HF Datasets → Blend Script → JSONL → Adaptive Data →
Adaptation (D→B) → AutoScientist → Trained Model → HF + Kaggle
```

## Links

- **Model (HF)**: https://huggingface.co/NabajyotiPathak/kiswahali-ai
- **Dataset (HF)**: https://huggingface.co/datasets/NabajyotiPathak/kiswahili-ai-blended
- **Dataset (Kaggle)**: https://www.kaggle.com/datasets/nabajyotipathak/kiswahili-ai-blended
- **Model (Kaggle)**: https://www.kaggle.com/models/nabajyotipathak/kiswahili-ai-blended
- **GitHub**: https://github.com/ThatDawg/kiswahili-ai

## How to Use

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("NabajyotiPathak/kiswahali-ai")
tokenizer = AutoTokenizer.from_pretrained("NabajyotiPathak/kiswahali-ai")

prompt = "Elezea umuhimu wa teknolojia katika elimu."
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512)
print(tokenizer.decode(outputs[0]))
```

## Reproducibility

1. Run `data/blend_swahili.py` to recreate the blended dataset from public sources
2. Upload to Adaptive Data with: deduplication + reasoning traces + hallucination mitigation
3. Train via AutoScientist with LoRA on Llama-4-Scout-17B

## License

Apache 2.0

## Acknowledgments

- Adaption Labs — AutoScientist + Adaptive Data + free compute
- HackIndia — AI Agents Hackathon platform
- Samwel Ngusa — FineTome-20k-sw
- Kencorpus Project — KenSwQuAD
- Mich Seth Owusu — Code-170k-swahili
- Noel Masasi & Bernard Masua — Swahili-Corpus-Dataset
