---
language: sw
license: apache-2.0
tags:
- swahili
- instruction-tuning
- low-resource-language
- adaptive-data
- autoscientist-challenge
---

# Kiswahili AI Blended Dataset

## Dataset Description

A multi-source Swahili instruction-following dataset created by blending four public Swahili datasets and processing them through **Adaptive Data** (Adaption Labs). Designed for fine-tuning language models to understand and generate Swahili text.

## Dataset Composition

| Source | Rows | Description |
|--------|------|-------------|
| **FineTome-20k-sw** | 17,982 | High-quality Swahili instruction pairs translated from FineTome-100k using GPT-4o-mini |
| **KenSwQuAD** | 7,506 | Human-annotated extractive QA pairs covering agriculture, education, tech, governance, daily life |
| **Code-170k-swahili** | 14,969 | Programming conversations in Swahili translated from glaive-code-assistant-v2 |
| **Swahili-Corpus-Dataset** | 12,267 | Raw Swahili text from government, news, health, education, law, agriculture (converted to instruction format) |
| **Total** | **52,118** (after dedup) | |

## Data Fields

- `instruction` (str): The task or question in Swahili
- `response` (str): The expected answer or completion in Swahili
- `source` (str): Origin dataset name

## Data Splits

- Train: ~49,512 rows (95%)
- Validation: ~2,606 rows (5%)

## Preprocessing

- Deduplication by first 80 characters of instruction + response
- Random shuffle (seed 42)
- Reformatted KenSwQuAD from extractive QA to instruction format
- Sampled to 20K for Adaptive Data free tier limit
- Adaptive Data recipes: deduplication, reasoning traces, hallucination mitigation

## Intended Use

Instruction-tuning Swahili language models for:
- General question answering
- Code generation
- Multi-task language understanding
- Educational applications for Swahili speakers (~100M+)

## License

Apache 2.0

## Citation

```
@dataset{kiswahili_ai_blended_2026,
  author = {Nabajyoti Pathak},
  title = {Kiswahili AI Blended Dataset},
  year = {2026}
  publisher = {Kaggle},
  url = {https://www.kaggle.com/datasets/nabajyotipathak/kiswahili-ai-blended}
}
```

## Acknowledgments

- Samwel Ngusa (FineTome-20k-sw)
- Kencorpus Project (KenSwQuAD)
- Mich Seth Owusu (Code-170k-swahili)
- Noel Masasi & Bernard Masua (Swahili-Corpus-Dataset)
- Adaption Labs (Adaptive Data + AutoScientist)
