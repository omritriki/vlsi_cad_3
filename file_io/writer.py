from typing import List, Tuple
from models.circuit import Circuit

def write_placement(output_circuit: Circuit, output_path: str) -> None:
    """Write gate placements to output file in required format"""
    with open(output_path, 'w') as f:
        # Write one line per gate with ID and coordinates
        for gate in output_circuit.gates:
            x = gate.floatXcoordinate
            y = gate.floatYcoordinate
            f.write(f"{gate.GateID:2d} {x:.8f} {y:.8f}\n")

def verify_placement(coordinates: List[Tuple[float, float]]) -> bool:
    """Verify all coordinates are within valid bounds"""
    for x, y in coordinates:
        if not (0 <= x <= 100 and 0 <= y <= 100):
            return False
    return True