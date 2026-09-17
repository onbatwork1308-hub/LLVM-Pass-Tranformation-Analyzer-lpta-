# LPTA Architecture

LPTA is split into three layers. Each layer only talks to the one next to
it, never skips ahead. This is what makes it possible to upgrade one part
later (e.g. swap how we capture LLVM data) without rewriting everything
else.

1. capture/   -- talks to LLVM (clang, opt). Produces raw pass events.
2. analysis/  -- takes raw events, computes metrics/diffs/descriptions.
3. frontend/  -- takes the final JSON and displays it. Knows nothing about LLVM.

## Brief discription of each layer
- capture/ is the only layer allowed to shell out to LLVM tools. If we
  later replace the `opt` CLI approach with a native C++ instrumentation
  pass, only this layer changes.
- analysis/ never talks to LLVM directly — it only receives data already
  produced by capture/. This is where metrics, diffing, and pass
  descriptions live, and where future features like pass timing or
  AI-assisted explanations will be added.
- frontend/ never talks to Python or LLVM at all. It only reads the final
  JSON file. This means the visualization could be swapped out entirely
  (e.g. for a React app) without touching any backend code.
