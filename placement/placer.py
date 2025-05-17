from collections import defaultdict
import numpy as np
from models.circuit import Circuit, Gate, Pad


def placer(input_circuit: Circuit, pad_weight: float = 1.0, limit: float = 100.0) -> Circuit:
    """
    Quadratic placer (single global solve) with
    • clique-model weights 1/(k-1)
    • correct pad handling (+=, not overwrite)
    • == instead of is
    • optional clamping to [0, limit] box
    """

    G = input_circuit.G                # number of gates
    C = [[0.0] * G for _ in range(G)]  # connectivity (weights)

    # ----- build C with a hash map: net -> list of GateIDs -----
    net_to_gates = defaultdict(list)
    for g in input_circuit.gates:
        for net in g.connected_nets:
            net_to_gates[net].append(g.GateID - 1)       # zero-based index

    for gate_indices in net_to_gates.values():
        k = len(gate_indices)
        if k < 2:
            continue
        w = 1.0 / (k - 1)                                 # clique scaling
        for i in range(k):
            for j in range(i + 1, k):
                a, b = gate_indices[i], gate_indices[j]
                C[a][b] += w
                C[b][a] += w

    # ----- build A (Laplacian + pad degrees) -----
    A = [[-C[i][j] for j in range(G)] for i in range(G)]
    for g in input_circuit.gates:
        i = g.GateID - 1
        pad_deg = 0.0
        for net in g.connected_nets:
            for pad in input_circuit.pads:
                if net == pad.NetNumberConnectedTo:       # equality, not identity
                    pad_deg += pad_weight
        A[i][i] = -sum(A[i]) + pad_deg                    # diagonal

    # ----- build b vectors -----
    b_x = [0.0] * G
    b_y = [0.0] * G
    for g in input_circuit.gates:
        i = g.GateID - 1
        for net in g.connected_nets:
            for pad in input_circuit.pads:
                if net == pad.NetNumberConnectedTo:
                    b_x[i] += pad_weight * pad.PinX
                    b_y[i] += pad_weight * pad.PinY

    # ----- solve Ax = b (dense; OK for small/medium designs) -----
    A_np = np.array(A, dtype=float)
    try:
        x = np.linalg.solve(A_np, b_x)
        y = np.linalg.solve(A_np, b_y)
    except np.linalg.LinAlgError:
        # fall back to least-squares if A is singular (all-floating sub-circuit)
        x = np.linalg.lstsq(A_np, b_x, rcond=None)[0]
        y = np.linalg.lstsq(A_np, b_y, rcond=None)[0]

    # ----- assign coordinates (clamped to chip box) -----
    for i, gate in enumerate(input_circuit.gates):
        gate.floatXcoordinate = max(0.0, min(limit, x[i]))
        gate.floatYcoordinate = max(0.0, min(limit, y[i]))

    return input_circuit
