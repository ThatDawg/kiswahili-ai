# Adaptive Data Configuration

## Dataset Ingestion
- **Source**: Local JSONL file (`swahili_blended/train_20k.jsonl`)
- **Format**: JSONL with `instruction` and `response` columns
- **Upload method**: Web UI → Adapt my Data → Instruction Dataset
- **Free tier limit**: 20,000 rows max per launch

## Wizard Flow
1. Click **"Adapt my Data"** in left sidebar
2. Select **"Instruction Dataset"**
3. When asked to expand → **Skip** (our data is already in Swahili)
4. When asked about brand guidelines → **No**
5. Map columns:
   - Prompt → `instruction`
   - Completion → `response`

## Column Mapping
```
prompt    → instruction    (required - the Swahili task/question)
completion → response      (required - the Swahili answer)
source    → (unmapped)     (provenance metadata)
```

## Recipes Enabled
| Recipe | Purpose |
|--------|---------|
| Prompt Deduplication | Remove duplicate instruction-response pairs |
| Reasoning Traces | Add step-by-step reasoning to responses |
| Hallucination Mitigation | Reduce factual errors |

## Recipes Skipped
| Recipe | Reason |
|--------|--------|
| Prompt Rephrase | Not needed — prompts are clean from blend script |
| Prompt Metadata Injection | Not needed — no extra metadata to inject |
| House Special | Too expensive for free tier |

## Credit Info
- **Cost**: 200 credits for 20,000 rows
- Adaptation took ~12 hours
