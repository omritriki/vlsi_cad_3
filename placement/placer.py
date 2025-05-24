from collections import defaultdict
import numpy as np
from models.circuit import Circuit, Gate, Pad


def placer(input_circuit: Circuit, left_limit: int, right_limit: int) -> Circuit:
    G = input_circuit.G                
    C = [[0.0] * G for _ in range(G)]  

    # Create mapping from gate IDs to matrix indices
    gate_id_to_index = {gate.GateID: i for i, gate in enumerate(input_circuit.gates)}

    # Build C with a hash map: net -> list of GateIDs 
    net_to_gates = defaultdict(list)
    for g in input_circuit.gates:
        for net in g.connected_nets:
            net_to_gates[net].append(gate_id_to_index[g.GateID])       

    for gate_indices in net_to_gates.values():
        k = len(gate_indices)
        if k < 2:
            continue
        w = 1.0 / (k - 1)                                
        for i in range(k):
            for j in range(i + 1, k):
                a, b = gate_indices[i], gate_indices[j]
                C[a][b] += w
                C[b][a] += w

    # Build A (Laplacian + pad degrees) 
    A = [[-C[i][j] for j in range(G)] for i in range(G)]
    for g in input_circuit.gates:
        i = gate_id_to_index[g.GateID]
        pad_deg = 0.0
        for net in g.connected_nets:
            for pad in input_circuit.pads:
                if net == pad.NetNumberConnectedTo:       
                    pad_deg += 1
        A[i][i] = -sum(A[i]) + pad_deg                    

    # Build b vectors 
    b_x = [0.0] * G
    b_y = [0.0] * G
    for g in input_circuit.gates:
        i = gate_id_to_index[g.GateID]
        for net in g.connected_nets:
            for pad in input_circuit.pads:
                if net == pad.NetNumberConnectedTo:
                    b_x[i] += 1 * pad.PinX
                    b_y[i] += 1 * pad.PinY

    # Solve Ax = b 
    A_np = np.array(A, dtype=float)
    try:
        x = np.linalg.solve(A_np, b_x)
        y = np.linalg.solve(A_np, b_y)
    except np.linalg.LinAlgError:
        x = np.linalg.lstsq(A_np, b_x, rcond=None)[0]
        y = np.linalg.lstsq(A_np, b_y, rcond=None)[0]

    # Assign coordinates 
    for i, gate in enumerate(input_circuit.gates):
        gate.floatXcoordinate = max(left_limit, min(right_limit, x[i]))
        gate.floatYcoordinate = max(0.0, min(100.0, y[i]))

    return input_circuit
