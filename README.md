# Quadratic Gate Placer (3QP) – VLSI CAD: Logic to Layout

This repository contains my implementation of the 3QP (Three Quadratic Placements) analytical placer, as part of the third programming assignment in the VLSI CAD course by Prof. Rob A. Rutenbar.

## 📌 Overview

The placer optimizes gate positions to minimize quadratic wirelength over a 100x100 chip area, using a recursive cut-and-contain strategy. It performs:
1. Initial full-chip quadratic placement (QP1)
2. Vertical partitioning at x=50
3. Left-side containment and placement (QP2)
4. Right-side containment and placement (QP3)
5. Final merged placement

## 💡 Features

- Reads standard-format netlists with gates and fixed I/O pad positions
- Builds Laplacian matrix for net connectivity
- Solves sparse linear systems (Ax = bx, Ay = by) for coordinates
- Implements recursive partitioning with centerline containment
- Supports various benchmark sizes from 18 to 1888 gates
- Outputs precise gate coordinates (8 decimal places)

## 🧪 Benchmarks

Supported test cases with statistics:
| Name     | Gates | Nets | Pads | Points |
|----------|-------|------|------|--------|
| toy1     | 18    | 20   | 6    | 20     |
| toy2     | 32    | 42   | 10   | 20     |
| fract    | 125   | 147  | 24   | 20     |
| primary1 | 752   | 902  | 107  | 20     |
| struct   | 1888  | 1920 | 64   | 20     |

## 📁 File Structure

```
├── benchmarks/         # Input netlists
│   └── 3QP/           # Test cases
├── file_io/           # File handling
│   ├── __init__.py
│   ├── parser.py      # Circuit parser
│   └── writer.py      # Placement writer
├── models/            # Data structures
│   ├── __init__.py
│   └── circuit.py     # Circuit model
├── placement/         # Core algorithms
│   ├── __init__.py
│   ├── placer.py      # QP solver
│   ├── partitioner.py # Bisection
│   └── containment.py # Boundary handling
├── main.py           # Entry point
└── README.md
```

## 🔧 Requirements

- Python 3.x
- NumPy: Matrix operations
- SciPy: Sparse linear solver

Install dependencies:
```bash
pip install numpy scipy
```

## ▶️ Usage

1. Select benchmark in main.py (1-5):
```python
SELECTED_BENCHMARK = 1  # toy1
```

2. Run the placer:
```bash
python main.py
```

3. Check output.txt for gate coordinates

## 📈 Visualization

View placements using the official visualizer:
**[3QP Visualizer Tool](https://spark-public.s3.amazonaws.com/vlsicad/javascript_tools/visualize.html)**

Features:
- Interactive placement viewer
- Drag & drop output files
- Shows gates, pads, and nets
- Validates coordinate bounds

## 📚 Credits

- Course: VLSI CAD: Logic to Layout
- Institution: University of Illinois at Urbana-Champaign
- Instructor: Prof. Rob A. Rutenbar

---

For implementation details, see individual source files.
