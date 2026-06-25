---
language: sw
tags:
- swahili
- instruction-tuning
- low-resource-language
- autoscientist
- adaptive-data
license: apache-2.0
datasets:
- ngusadeep/FineTome-20k-sw
- Kencorpus/KenSwQuAD
- michsethowusu/Code-170k-swahili
- ngusadeep/Swahili-Corpus-Dataset
---

# Kiswahili AI - Swahili Instruction Model

## Model Description

This model is a Swahili instruction-tuned language model fine-tuned using **AutoScientist** by Adaption Labs. It is optimized for understanding and generating Swahili text across multiple domains including general knowledge, question answering, code, and raw text understanding.

Built for the **AutoScientist Challenge** (Language category) to improve Swahili language model performance over the baseline.

## Training Data

The model was fine-tuned on **Kiswahili AI Blended Dataset**, a multi-source instruction dataset combining:

| Source | Rows | Type |
|--------|------|------|
| FineTome-20k-sw | 17,982 | General instruction |
| KenSwQuAD | 7,506 | Extractive QA reformatted to instruction |
| Code-170k-swahili | 14,969 | Code conversations |
| Swahili-Corpus-Dataset | 12,267 | Raw text converted to instruction |
| **Total** | **52,118** | |

All data was processed and adapted through **Adaptive Data** platform (deduplication, reasoning traces, hallucination mitigation).

## Training Procedure

- **Platform**: AutoScientist by Adaption Labs
- **Base Model**: Llama-4-Scout-17B-16E-Instruct (109B MoE)
- **Method**: Closed-loop co-optimization of data and training recipes
- **Compute**: Provided by Adaption / Together AI
- **Iterations**: AutoScientist co-optimization loop until convergence
- **Win Rate**: 73% (adapted) vs 27% (baseline) — +170% relative improvement

## Intended Use

- Swahili language understanding and generation
- Question answering in Swahili
- Code generation with Swahili instructions
- Educational and informational tasks for Swahili speakers

## Limitations

- Primarily trained on Kenyan Swahili variants
- Performance on other dialects (Congo, Tanzania coastal) may vary
- Not aligned for safety-critical applications without additional fine-tuning

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

## Citation

```
@model{kiswahili_ai_2026,
  author = {Nabajyoti Pathak},
  title = {Kiswahili AI: Swahili Instruction Model},
  year = {2026},
  publisher = {Hugging Face},
  url = {https://huggingface.co/NabajyotiPathak/kiswahili-ai}
}
```

## Submitted to

AutoScientist Challenge 2026 - Language Category - Adaption Labs
