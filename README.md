# Kiswahili AI — Swahili Instruction Model

> AutoScientist Challenge 2026 — Language Category

## Overview

Kiswahili AI is a Swahili instruction-tuned language model fine-tuned from **Llama-4-Scout-17B-16E-Instruct (109B MoE)** using **AutoScientist** by Adaption Labs. It combines **4 public Swahili datasets** into a unified instruction dataset (~52K rows), processes them through **Adaptive Data** for quality enhancement, and trains via AutoScientist's closed-loop co-optimization.

**Result**: **73% win rate** (adapted) vs **27%** (baseline) — **+170% relative improvement** on Adaption's held-out test set.

**Why Swahili?** Over 100 million speakers across East Africa. Swahili is a low-resource language where current LLMs show a 28-45% performance gap compared to English.

## Dataset

| Source | Rows | Type |
|--------|:----:|------|
| FineTome-20k-sw | 17,982 | General instruction |
| KenSwQuAD | 7,506 | Extractive QA |
| Code-170k-swahili | 14,969 | Code conversations |
| Swahili-Corpus-Dataset | 12,267 | Raw text (converted to instruction) |
| **Total** | **52,118** (after dedup) | |

### Data Adaptation

The raw dataset scored **Grade D (6.9th percentile)**. After Adaptive Data processing (deduplication + reasoning traces + hallucination mitigation), quality improved **+62% to Grade B (25.6th percentile)**.

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

### Results

| Metric | Baseline | Adapted | Improvement |
|--------|:--------:|:-------:|:-----------:|
| Win Rate | 27% | 73% | **+170%** |
| General Category Win Rate | 31% | 69% | **+123%** |

## Pipeline

```
Public HF Datasets → Blend Script → JSONL → Adaptive Data → 
Adaptation (D→B) → AutoScientist → Trained Model → HF + Kaggle
```

1. **Blend**: `data/blend_swahili.py` downloads and merges 4 datasets
2. **Validate**: `data/validate_format.py` checks JSONL quality
3. **Adapt**: Adaptive Data — deduplication, reasoning traces, hallucination mitigation
4. **Train**: AutoScientist co-optimizes data + training recipe
5. **Release**: Weights + dataset on Hugging Face + Kaggle

## How to Use

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("NabajyotiPathak/kiswahili-ai")
tokenizer = AutoTokenizer.from_pretrained("NabajyotiPathak/kiswahili-ai")

prompt = "Elezea umuhimu wa teknolojia katika elimu."
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512)
print(tokenizer.decode(outputs[0]))
```

## Project Structure

```
swahili-ai/
├── data/
│   ├── blend_swahili.py       # Download + blend 4 datasets
│   ├── validate_format.py     # Validate output format
│   ├── sources.json           # Dataset provenance
│   └── swahili_blended/       # Output directory (generated)
├── docs/
│   ├── MODEL_CARD.md          # Hugging Face model card
│   └── DATASET_CARD.md        # Hugging Face dataset card
├── adaptive_data_config.md    # Adaptive Data settings
├── autoscientist_config.md    # AutoScientist experiment config
└── README.md
```

## Reproducibility

1. Run `data/blend_swahili.py` to recreate the blended dataset from public sources
2. Upload to Adaptive Data with: deduplication + reasoning traces + hallucination mitigation
3. Train via AutoScientist with LoRA on Llama-4-Scout-17B

## Links

- **Model**: https://huggingface.co/NabajyotiPathak/kiswahali-ai
- **Dataset**: https://huggingface.co/datasets/NabajyotiPathak/kiswahili-ai-blended
- **Kaggle Dataset**: https://www.kaggle.com/datasets/nabajyotipathak/kiswahili-ai-blended
- **Kaggle Model**: https://www.kaggle.com/models/nabajyotipathak/kiswahili-ai-blended
- **GitHub**: https://github.com/ThatDawg/kiswahili-ai

## Judging Criteria Alignment

| Criterion | How We Address It |
|-----------|-------------------|
| Performance improvement | 27% → 73% win rate (+170%) on held-out test set |
| Dataset originality | Multi-source blend (4 datasets) + Adaptive Data enhancement |
| Real-world impact | 100M+ Swahili speakers underserved by current AI |
| AutoScientist depth | Full co-optimization loop: data adaptation → training → convergence |
| Release quality | Model card, dataset card, reproducible pipeline, open weights |

## License

Apache 2.0

## Acknowledgments

- Adaption Labs — AutoScientist + Adaptive Data + free compute
- Samwel Ngusa — FineTome-20k-sw
- Kencorpus Project — KenSwQuAD
- Mich Seth Owusu — Code-170k-swahili
- Noel Masasi & Bernard Masua — Swahili-Corpus-Dataset