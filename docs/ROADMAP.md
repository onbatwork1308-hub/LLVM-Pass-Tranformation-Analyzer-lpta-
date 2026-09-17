# LPTA Roadmap

## MVP
- Capture pass-by-pass IR snapshots using `opt -print-changed=quiet`
- Compute basic metrics (instruction/load/store/branch counts) with llvmlite
- Text diff between before/after IR per pass
- Static HTML timeline + diff viewer

## Near-term upgrades
- User-selectable passes to analyze (instead of the full default pipeline)
- Descriptions for all LLVM passes, not just the common ones
- Pass timing data (from `opt -time-passes`)

## Long-term / grad-school-level goals
- Native LLVM instrumentation (real PassInstrumentationCallbacks in C++)
  instead of shelling out to `opt`
- Codegen correlation: map IR changes to final assembly
- Cross-run comparison (e.g. -O2 vs -O3, or two LLVM versions)
- Optional AI-assisted explanation for passes with no manual description yet
