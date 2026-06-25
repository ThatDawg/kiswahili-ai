# AutoScientist Experiment Configuration

## Experiment Setup
| Field | Value |
|-------|-------|
| Name | `kiswahili-ai-v1` |
| Category | **Language** |
| Language | **Swahili (sw)** |
| Method | Instruction Tuning |

## Model
- **Base Model**: meta-llama/Llama-4-Scout-17B-16E-Instruct (109B MoE)
- **Training Method**: SFT with LoRA (r=64, alpha=128, all-linear)
- **Epochs**: 1
- **Batch Size**: max
- **Learning Rate**: 0.0001 (cosine scheduler)
- **Warmup Ratio**: 0.03
- **Max Grad Norm**: 1
- **Weight Decay**: 0.02

## Dataset
- **Source**: 20,000 rows from Kiswahili AI Blended Dataset
- **Adaptation**: Deduplication + Reasoning Traces + Hallucination Mitigation
- **Quality Improvement**: D → B grade (+62%)

## Results
- **Baseline Win Rate**: 27%
- **Adapted Win Rate**: 73%
- **Relative Improvement**: +170%
- **Converged**: Yes

## Training Time
48-72 hours (free compute provided by Adaption)
