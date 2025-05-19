from typing import List, Tuple
from models.circuit import Circuit, Gate, Pad


def partitioner(input_circuit: Circuit) -> Tuple[List[Gate], List[Gate]]:
    if not hasattr(input_circuit.gates[0], 'floatXcoordinate'):
        raise AttributeError("Gates must have floatXcoordinate and floatYcoordinate attributes")

    sorted_gates = sorted(
        input_circuit.gates,
        key=lambda g: (g.floatXcoordinate if g.floatXcoordinate is not None else 0.0) * 100000 +
                      (g.floatYcoordinate if g.floatYcoordinate is not None else 0.0)
    )

    left_half = sorted_gates[:input_circuit.G // 2]
    right_half = sorted_gates[input_circuit.G // 2:]

    print(len(left_half), len(right_half))


    return left_half, right_half
