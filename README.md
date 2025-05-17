# Quadratic Gate Placer (3QP) – VLSI CAD: Logic to Layout

This repository contains my implementation of the 3QP (Three Quadratic Placements) analytical placer, as part of the third programming assignment in the VLSI CAD course by Prof. Rob A. Rutenbar.

## 📌 Overview

The placer optimizes gate positions to minimize quadratic wirelength over a 100x100 chip area, using a recursive cut-and-contain strategy. It performs:
- One full-chip quadratic placement.
- One placement for gates on the left half.
- One placement for gates on the right half.

These steps simulate a realistic analytical placer by solving sparse linear systems derived from netlist connectivity.

## 💡 Features

- Reads standard-format netlists with gates and fixed I/O pad positions.
- Builds Laplacian matrix for net connectivity and solves Ax = bx, Ay = by for coordinates.
- Divides gates using a vertical partition at X=50.
- Performs containment to represent inter-region connections.
- Outputs precise gate coordinates for visualization or further use.

## 🧪 Benchmarks

Supports all official Coursera testcases:
- toy1, toy2
- fract
- primary1
- struct

Each test includes hundreds to thousands of gates and nets.

## 📁 File Structure

```
├── src/                # Core placement logic and matrix construction
├── benchmarks/         # Input netlists for testing
├── output/             # Output placement files
├── utils/              # Helper functions
└── README.md
```

## 🔧 Requirements

- Python 3.x
- NumPy
- SciPy

Install dependencies:
```bash
pip install numpy scipy
```

## ▶️ Run

```bash
python main.py --input benchmarks/toy1.txt --output output/toy1.out
```

## 📈 Visualization

To visualize the output placements, use the web tool:
**[Visualizer Tool](https://spark-public.s3.amazonaws.com/vlsicad/javascript_tools/visualize.html)**  
Drag and drop your output file for instant rendering.

## 📜 Output Format

Each line of the output file includes:
```
GateID  X-coordinate  Y-coordinate
```
Coordinates are in floating point with 8-digit precision.

## 🏆 Extra Credit (Optional)

Includes a scalable framework for recursive 8x8 partitioning to implement full chip-level placement with deeper cuts.

## 📚 Credits

This project is based on materials from the **University of Illinois at Urbana-Champaign**.  
Assignment by **Prof. Rob A. Rutenbar** and teaching team.

---

Feel free to fork or reuse the implementation.
