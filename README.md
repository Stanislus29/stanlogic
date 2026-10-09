<div align="center">

<img src="https://img.shields.io/badge/StanLogic-Boolean%20Minimization%20%26%20Geometric%20Clustering-0B3D91?style=for-the-badge&logo=python&logoColor=white" alt="StanLogic Banner"/>

<br/>

<img src="https://img.shields.io/badge/Python-3.8%2B-0B3D91?style=flat-square&logo=python&logoColor=white" alt="Python 3.8+"/>
<img src="https://img.shields.io/pypi/v/stanlogic?style=flat-square&color=0B3D91&logo=pypi&logoColor=white" alt="PyPI version"/>
<img src="https://img.shields.io/badge/NumPy-accelerated-0B3D91?style=flat-square&logo=numpy&logoColor=white" alt="NumPy"/>
<img src="https://img.shields.io/badge/License-MIT-0B3D91?style=flat-square" alt="MIT License"/>

<br/>

*Boolean minimization through Karnaugh-map structure, geometric clustering, and scalable hierarchical decomposition.*

</div>

---

## Overview

**StanLogic** is a Python library and research workspace for simplifying Boolean systems by treating Karnaugh maps as structured geometric spaces rather than only as flat truth tables.

The project combines classical Boolean minimization with higher-dimensional clustering methods. Smaller systems are solved directly with K-map grouping, while larger systems are represented as collections of adjacent maps that can be merged across depth, span, and hyperspan dimensions.

StanLogic is intended for:

- Exploring how Boolean hypercubes collapse into larger implicants.
- Teaching and visualizing Boolean algebra and Karnaugh-map minimization.
- Comparing bitwise, geometric, vectorized, and hierarchical approaches.
- Generating minimized SOP/POS expressions and hardware-oriented output.
- Running experiments, benchmarks, and information-density analyses.

> **Research status:** StanLogic is an active research and experimentation project. The larger-variable methods are designed to investigate scalable structure and practical limits; benchmark results should be interpreted as research data rather than a guarantee of globally optimal minimization for every input.

## Core Ideas

### 1. K-map cells become bit patterns

A minterm is represented as a binary pattern. Fixed bits identify literals, while `-` represents a varying dimension. This makes adjacency, coverage, and implicant comparison suitable for bitwise operations.

### 2. Clusters are selected by coverage and dominance

The algorithms search for valid power-of-two groups, remove groups subsumed by larger groups, identify essential prime implicants, and cover remaining minterms with weighted greedy selection. Coverage is verified after selection, with fallback handling for gaps.

### 3. Higher-dimensional maps are built hierarchically

For more than four variables, the final four variables form a 4×4 K-map and the remaining variables identify additional maps. Repeated patterns can then be merged across adjacent maps:

- **2D:** cells within one 4×4 K-map.
- **3D:** clusters spanning adjacent K-maps.
- **4D:** clusters spanning adjacent 3D chunks.
- **5D:** clusters spanning adjacent hyperchunks.

The implementation uses depth-, span-, and hyperspan-dominance ideas to retain broader clusters when they cover equivalent regions.

### 4. Large systems are decomposed before they are recombined

When a complete truth table is too large to process as one in-memory problem, StanLogic partitions it into smaller subproblems. `BoolMinHcal` processes 16-variable chunks, writes intermediate implicants to CSV, and supports distributed chunk ranges and later CSV merging.

## Available Solvers

| Solver | Intended range | Main approach | Important entry points |
|:---|:---:|:---|:---|
| `BoolMin2D` | 2–4 variables | Direct K-map grouping with bitmask coverage and prime-implicant filtering | `minimize()`, `minimize_visualize()`, `generate_verilog()`, `generate_html_report()` |
| `KMapSolver3D` | Package export / compatibility solver | Three-dimensional K-map operations | Refer to the module implementation and tests for the current API |
| `BoolMinGeo` | 5+ variables | Hierarchical K-maps with 3D/4D/5D clustering and vectorized implicant merging | `minimize()`, `minimize_3d()`, `minimize_4d()`, `minimize_5d()` |
| `BoolMinHcal` | More than 16 variables | Chunked 16-variable processing with CSV-backed intermediate results | `minimize()`, `process_chunk()`, `merge_csv_files()` |
| `OnesComplement` | Binary arithmetic utility | Fixed-width one’s-complement conversion and end-around-carry addition | `set_decimals()`, `decimal_to_binary()`, `add_binaries()` |

All minimizers support the `sop` and `pos` forms where implemented. `BoolMin2D` and `BoolMinGeo` also expose reporting and hardware-output helpers, including Verilog generation and HTML reports with Graphviz/Viz.js diagrams.

## Quick Start

## Installation

Install StanLogic from PyPI:

```bash
pip install stanlogic
```

or clone the repository and install the package locally:

```bash
git clone https://github.com/Stanislus29/stanlogic.git
cd stanlogic/StanLogic
python -m pip install -e .
```

The package requires Python 3.8 or newer. Core dependencies include NumPy and Matplotlib; optional extras are available for the web interface and development tooling.

### 2–4 variable minimization

```python
from stanlogic import BoolMin2D

kmap = [
    [1, 1],
    [0, 1],
]

solver = BoolMin2D(kmap)
terms, expression = solver.minimize(form="sop")

print(terms)
print(expression)
```

`BoolMin2D` accepts K-map values of `0`, `1`, and `'d'` for don’t-care cells. It supports both SOP and POS grouping, including edge wrapping and variable-order conventions.

### Higher-dimensional minimization

```python
from stanlogic import BoolMinGeo

num_vars = 6
outputs = [0] * (2 ** num_vars)

# Example function: x1' x2'
for minterm in range(2 ** num_vars):
    bits = format(minterm, f"0{num_vars}b")
    if bits[:2] == "00":
        outputs[minterm] = 1

solver = BoolMinGeo(num_vars, outputs)
terms, expression = solver.minimize_3d(form="sop")

print(expression)
```

For automatic strategy selection, use `solver.minimize()`. The current selector uses geometric 3D minimization through 8 variables, geometric 4D minimization through 10 variables, and a hierarchical 10-variable base above that.

### Generate Verilog or an HTML report

```python
verilog = solver.generate_verilog(
    module_name="logic_circuit",
    form="sop",
)
print(verilog)

solver.generate_html_report(
    filename="kmap_report.html",
    form="sop",
    module_name="logic_circuit",
)
```

## Repository Structure

```text
stanlogic/
├── StanLogic/
│   ├── src/stanlogic/              # Installable Python package
│   │   ├── __init__.py             # Public exports and package version
│   │   ├── BoolMin2D.py            # 2D K-map minimization, SOP/POS, reports
│   │   ├── BoolMinGeo.py           # Geometric and hierarchical minimization
│   │   ├── BoolMinHcal.py          # Chunked large-scale minimization
│   │   ├── kmapsolver3D.py         # 3D K-map solver implementation
│   │   └── ones_complement.py      # One’s-complement arithmetic utility
│   │
│   ├── docs/                       # Algorithm notes and mathematical background
│   │   ├── kmapsolver.md           # K-map solver documentation
│   │   ├── ones_complement.md      # One’s-complement documentation
│   │   └── pseudocode/              # Algorithm pseudocode
│   │
│   ├── tests/
│   │   ├── KMapSolver/
│   │   │   ├── benchmarks/         # Performance comparisons and timing runs
│   │   │   ├── analysis/           # Result and equivalence analysis
│   │   │   ├── cluster_analysis/   # Cluster behaviour and density studies
│   │   │   ├── decay_analysis/     # Behaviour beyond practical thresholds
│   │   │   ├── demos/              # Demonstrations and examples
│   │   │   ├── outputs/            # Generated benchmark outputs
│   │   │   └── 24_bits_test/       # Multicore large-system experiments
│   │   └── ones_complement/        # One’s-complement demonstrations/tests
│   │
│   ├── prototypes/                 # Earlier algorithm prototypes
│   ├── images/                     # Project logos and visual assets
│   ├── app.py                      # Web/application entry point
│   ├── kmap-solver-visualizer.html # Browser visualizer
│   ├── pyproject.toml              # Modern package and pytest configuration
│   ├── setup.py                    # Setuptools compatibility configuration
│   ├── requirements.txt            # Runtime and optional dependency notes
│   ├── CITATION.cff                # Citation metadata
│   └── README.md                   # Package-level documentation
│
├── CONTRIBUTING.md
├── COMMERCIAL_LICENSE_REQUEST.md
├── LICENCE
├── TRADEMARKS.md
└── README.md                       # This project overview
```

## Research and Experiments

The `StanLogic/tests/KMapSolver/` tree is more than a conventional unit-test directory. It contains the experimental record for the project, including:

- Benchmarks against alternative symbolic and Boolean tooling.
- Coverage and equivalence checks for generated expressions.
- Cluster-density and decay analyses.
- Demonstrations of the geometric minimizers.
- Large 24-variable multicore experiments using worker processes and generated outputs.

The project’s central research question is how Boolean hypercubes collapse: when local groups in one K-map repeat across adjacent maps, those repeated structures can be treated as higher-dimensional clusters and represented with fewer fixed literals.

## Documentation

- [Package documentation](StanLogic/docs/)
- [K-map solver notes](StanLogic/docs/kmapsolver.md)
- [One’s-complement notes](StanLogic/docs/ones_complement.md)
- [Package README](StanLogic/README.md)
- [Contribution guidelines](CONTRIBUTING.md)
- [Commercial license request](COMMERCIAL_LICENSE_REQUEST.md)

## Conventions and Notes

- Boolean variables are emitted as `x1`, `x2`, …, with `'` indicating complementation.
- SOP expressions join product terms with `+`; POS expressions join sum terms with `*`.
- Don’t-care cells are written as `'d'`.
- Gray-code ordering is used for K-map coordinates.
- Internal method names are part of an active research codebase and may change as algorithms are refined.
- `minimize_heirarchical()` retains the historical spelling in the current implementation; use the public auto-selector `minimize()` when possible.

## Citation

If you use StanLogic in research, teaching, benchmarking, or software, cite the repository using the metadata in [`StanLogic/CITATION.cff`](StanLogic/CITATION.cff).

```text
Somtochukwu Stanislus Emeka-Onwuneme. StanLogic: A Python Package for Boolean Simplification and Logic Computation. 
```

## License

StanLogic is licensed under [MIT LICENSE](LICENSE)

---

<div align="center">

**Somtochukwu Stanislus Emeka-Onwuneme** 

</div>
