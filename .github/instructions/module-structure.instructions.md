---
applyTo: "**/exercises/**"
---

# Module & Exercise Context

This workspace is a Jupyter/Python learning project. Each module follows this structure:

```
N_Module_Name/
  docs/          ← Portuguese (pt-BR) documentation (Markdown)
  exercises/     ← Jupyter notebooks and Python scripts
    libs/        ← Shared utilities for that module's exercises
  README.md
```

## Notebook conventions
- Use `.venv/` at workspace root — always activate before running Python: `source .venv/bin/activate`
- Cell outputs should be cleared before committing notebooks
- LaTeX formulas in Markdown cells: inline `$E=mc^2$`, block `$$\int f(x)\,dx$$`
- Imports go in the first code cell; constants in the second

## Exercise file naming
- `01-topic-slug.ipynb`, `02-next-topic.ipynb` — zero-padded, kebab-case
- Shared helpers go in `exercises/libs/<module>_lib.py`

## Modules
| Folder | Topic |
|---|---|
| `1_Foundation-Generative-AI/` | Foundation models, fine-tuning with LoRA, model adaptation |
| `2_LLMs-And-Text-Generation/` | Large Language Models, text generation, NLP fundamentals |
| `3_Computer-Vision-And-GenAI/` | Computer vision with GenAI, image generation models |
| `4_Building_Gen_AI_Solutions/` | End-to-end GenAI solutions, RAG, semantic search |
