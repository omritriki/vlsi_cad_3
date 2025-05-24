from models.circuit import Circuit, Gate, Pad
from typing import List, Set, Tuple
import copy



def containment(partition_gates: List[Gate], circuit: Circuit, left_limit: int, right_limit: int) -> Circuit:
    """
    Handle containment for a partition:
    - Keep ONLY the gates from partition_gates
    - Convert connected gates from circuit (not in partition_gates) to pads at x=50
    - Move existing pads connected to partition gates to the closest limit
    - Remove all other gates
    - Preserve original gate IDs
    """
    circuit_copy = copy.deepcopy(circuit)
    gates_to_convert = []
    partition_gate_ids = {gate.GateID for gate in partition_gates}
    next_pad_id = max(pad.PinID for pad in circuit_copy.pads) + 1
    
    # First, keep only the partition gates
    circuit_copy.gates = [gate for gate in circuit_copy.gates if gate.GateID in partition_gate_ids]
    circuit_copy.G = len(circuit_copy.gates)
    
    # Move existing pads connected to partition gates to the closest limit
    for pad in circuit_copy.pads:
        for gate in partition_gates:
            if pad.NetNumberConnectedTo in gate.connected_nets:
                # Move pad to closest limit
                if abs(pad.PinX - left_limit) <= abs(pad.PinX - right_limit):
                    pad.PinX = left_limit
                else:
                    pad.PinX = right_limit
                break
    
    # Process gates from original circuit that are not in partition_gates
    for gate in circuit.gates:
        if gate.GateID not in partition_gate_ids:
            # Check if connected to any partition gate
            connected_to_partition = False
            for net_id in gate.connected_nets:
                for partition_gate in partition_gates:
                    if net_id in partition_gate.connected_nets:
                        connected_to_partition = True
                        break
                if connected_to_partition:
                    break
            
            if connected_to_partition:
                # Convert to pad at x=50
                gates_to_convert.append((gate, next_pad_id))
                next_pad_id += 1
    
    # Convert connected gates to pads at x=50
    for gate, pad_id in gates_to_convert:
        new_pad = Pad(
            PinID=pad_id,
            NetNumberConnectedTo=gate.connected_nets[0],
            PinX=50,  # Fixed at x=50
            PinY=gate.floatYcoordinate  # Preserve Y coordinate
        )
        circuit_copy.pads.append(new_pad)
    
    return circuit_copy
