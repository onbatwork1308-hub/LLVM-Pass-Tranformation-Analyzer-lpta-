# LPTA — LLVM Pass Transformation Analyzer

**Make LLVM optimization transformations easier to inspect, measure, and understand.**

LPTA is a Python-based tool that analyzes LLVM Intermediate Representation (IR) across optimization passes. It compares IR snapshots, highlights line-level differences, measures changes such as instruction counts, and builds a pass-by-pass transformation history that can be viewed through generated reports.

Instead of manually comparing multiple IR dumps, LPTA helps answer:

- **What changed?** Inspect the IR differences before and after a pass.
- **How much changed?** Compare instruction-level metrics.
- **Where did it change?** Associate observed changes with optimization passes.
- **How can I inspect the results?** Review the transformation history and generated HTML report.

> LPTA reports observed IR changes and metrics. A reduction in instruction count alone does not prove that generated code is faster.

## Features

- **LLVM IR capture:** Capture IR snapshots around optimization passes using the LLVM command-line tooling.
- **IR diffing:** Identify line-level changes between before-and-after IR snapshots.
- **Instruction metrics:** Measure instruction counts and other supported IR metrics.
- **Transformation history:** Build a structured history of observed changes across passes.
- **Pass knowledge:** Store pass descriptions in YAML to help explain common optimization passes.
- **HTML reporting:** Generate a report that makes the analysis easier to inspect.
- **Example programs:** Includes C examples covering Fibonacci, loops, matrix multiplication, and array summation.
- **Tests:** Includes tests for capture, history construction, and metrics.

## Architecture

LPTA is organized into three main stages:

```text
C source program
       |
       v
LLVM / opt command-line pipeline
       |
       v
Capture IR snapshots and pass information
       |
       v
Diff engine + metrics + pass knowledge
       |
       v
Transformation history
       |
       v
JSON history + HTML report / frontend
```

### Main components

| Component | Location | Responsibility |
|---|---|---|
| Capture | `lpta/capture/` | Capture IR and pass information from the LLVM command-line workflow. |
| Diff engine | `lpta/analysis/diff_engine.py` | Compare IR snapshots and identify textual differences. |
| Metrics | `lpta/analysis/metrics.py` | Calculate supported metrics for the captured IR. |
| History builder | `lpta/analysis/history_builder.py` | Assemble pass-level observations into a transformation history. |
| Pass knowledge | `lpta/analysis/pass_knowledge.py` | Work with pass descriptions and knowledge data. |
| CLI | `lpta/cli.py` | Provide the command-line entry point. |
| Reporting | `lpta/report.py` | Produce an HTML report from the analysis results. |
| Frontend | `frontend/` | Present results through the browser interface. |
| Tests | `tests/` | Test capture, history construction, and metrics. |

## Repository structure

```text
.
├── docs/                   # Architecture, pass guide, and roadmap
├── examples/               # Sample C programs
├── frontend/               # HTML, CSS, and JavaScript interface
├── lpta/
│   ├── analysis/            # Diffing, metrics, history, pass knowledge
│   ├── capture/             # LLVM IR and pass capture
│   ├── data/                # Pass descriptions
│   ├── cli.py               # Command-line entry point
│   └── report.py            # HTML report generation
├── output/                  # Generated history and HTML report
├── tests/                   # Automated tests
├── requirements.txt
├── setup.py
└── README.md
```

## Requirements

- Python 3
- LLVM/Clang command-line tools, including `opt`
- Python dependencies listed in `requirements.txt`

Make sure the LLVM tools required by your capture workflow are installed and available on your `PATH`. The LLVM tool versions should be compatible with the IR and command-line options used by your setup.

## Installation

Clone the repository:

```bash
git clone https://github.com/onbatwork1308-hub/LLVM-Pass-Tranformation-Analyzer-lpta-.git
cd LLVM-Pass-Tranformation-Analyzer-lpta-
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install LLVM/Clang separately if they are not already available. Verify the tools used by your setup:

```bash
clang --version
opt --version
```

If your system uses versioned executable names, such as `clang-22` and `opt-22`, make sure the capture configuration or commands use the names installed on your system.

## Usage

The project includes a command-line entry point at `lpta/cli.py`. Check its available options:

```bash
python -m lpta.cli --help
```

You can also inspect the project documentation for the current workflow:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/PASS_KNOWLEDGE_GUIDE.md`](docs/PASS_KNOWLEDGE_GUIDE.md)
- [`docs/ROADMAP.md`](docs/ROADMAP.md)

Run LPTA using the command and arguments supported by your current CLI implementation. The repository includes generated example artifacts in `output/`, including `history.json` and `report.html`.

## Example programs

The `examples/` directory contains:

- `fibonacci.c`
- `loops.c`
- `matrix_multiply.c`
- `sum_array.c`

These programs can be used to explore how LLVM optimization passes change IR for different control-flow, arithmetic, and memory-access patterns.

## Running tests

Run the test suite with:

```bash
python -m pytest
```

If `pytest` is not installed, install it in your virtual environment before running the tests.

## Technology stack

- **Python** for orchestration and analysis
- **LLVM / Clang / `opt`** for compiler IR and optimization workflows
- **IR diffing libraries** for identifying textual differences between snapshots
- **HTML, CSS, and JavaScript** for the frontend
- **JSON and YAML** for structured history and pass descriptions
- **pytest** for automated testing

## Current scope

The current implementation focuses on capturing and comparing IR, calculating supported metrics, building a transformation history, and generating reports.

More advanced capabilities, such as reliable semantic matching of instructions, proving that a transformation improves runtime performance, and mapping individual IR changes to final machine instructions, should be treated as future work unless implemented and documented in the repository.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Pass Knowledge Guide](docs/PASS_KNOWLEDGE_GUIDE.md)
- [Roadmap](docs/ROADMAP.md)

## Contributing

Contributions, bug reports, and suggestions are welcome. When reporting an issue, include the LLVM version, Python version, command used, and a minimal C or LLVM IR example that reproduces the problem.

## License

See [`LICENSE`](LICENSE) for the license terms.
