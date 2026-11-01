# Balanced Batch Planner

Splits weighted items into a requested number of non-empty batches and minimizes the greatest batch load.

## Tools

| Tool or task | Purpose |
|---|---|
| `evaluate_partition` | Validate and score a proposed partition |
| `solve_partition` | Compute the hidden canonical optimum |
| `balance-batches` | Agent task that produces an optimal partition |

The verifier independently checks item coverage, canonical ordering, computed loads, and optimality by exhaustive search. Inputs are deliberately limited to ten items and four batches so verification remains reproducible.

## Layout

`contract.py` declares typed values, `src/plugin/` implements MCP tools, `verifier/` contains deterministic checks, and `tests/` covers correct, incorrect, malformed-semantic, and boundary cases.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
```
