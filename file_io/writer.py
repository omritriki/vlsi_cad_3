from typing import List, Tuple
from models.circuit import Circuit

def write_placement(output_circuit: Circuit, output_path: str) -> None:
    with open(output_path, 'w') as f:
        # Write one line per gate with ID and coordinates
        for gate_id in range(1, output_circuit.G + 1):
            x, y = output_circuit.gates[gate_id - 1].floatXcoordinate, output_circuit.gates[gate_id - 1].floatYcoordinate
            f.write(f"{gate_id:2d} {x:.8f} {y:.8f}\n")

def verify_placement(coordinates: List[Tuple[float, float]]) -> bool:
    for x, y in coordinates:
        if not (0 <= x <= 100 and 0 <= y <= 100):
            return False
    return True