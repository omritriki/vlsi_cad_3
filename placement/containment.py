from models.circuit import Circuit, Gate, Pad
from typing import List, Set, Tuple
import copy



def containment(partition_gates: List[Gate], circuit: Circuit, left_limit: int, right_limit: int) -> Circuit:
    """
    Handle containment for a partition:
    - Keep partition_gates in their original positions
    - Convert connected outside gates to pads at partition boundary
    - Remove unconnected outside gates
    """
    circuit_copy = copy.deepcopy(circuit)
    gates_to_remove = []
    gates_to_convert = []
    partition_gate_ids = {gate.GateID for gate in partition_gates}
    next_pad_id = max(pad.PinID for pad in circuit_copy.pads) + 1
    
    # Move existing pads to limits if outside bounds
    for pad in circuit_copy.pads:
        if not _is_within_limits(pad.PinX, left_limit, right_limit):
            pad.PinX = left_limit if pad.PinX < left_limit else right_limit
    
    # Process only non-partition gates
    for gate in circuit_copy.gates:
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
                # Convert to pad at partition boundary
                boundary = left_limit if gate.floatXcoordinate < left_limit else right_limit
                gates_to_convert.append((gate, next_pad_id, boundary))
                next_pad_id += 1
            else:
                gates_to_remove.append(gate)
    
    # Convert gates to pads at boundaries
    for gate, pad_id, boundary in gates_to_convert:
        new_pad = Pad(
            PinID=pad_id,
            NetNumberConnectedTo=gate.connected_nets[0],
            PinX=boundary,
            PinY=gate.floatYcoordinate  # Preserve Y coordinate
        )
        circuit_copy.pads.append(new_pad)
        circuit_copy.gates.remove(gate)
    
    # Remove unconnected gates
    for gate in gates_to_remove:
        circuit_copy.gates.remove(gate)
    
    print(f"Containment results for {len(partition_gates)} partition gates:")
    print(f"- Converted {len(gates_to_convert)} connected gates to boundary pads")
    print(f"- Removed {len(gates_to_remove)} unconnected gates")
    print(f"- Remaining gates: {len(circuit_copy.gates)}")
    
    return circuit_copy


def _is_within_limits(x: float, left: int, right: int) -> bool:
    """Check if coordinate is within partition limits"""
    return left <= x <= right


def _find_connected_elements(gate: Gate, circuit_copy: Circuit) -> Set[int]:
    """Find all elements connected to a gate through nets"""
    connected = set()
    for net_id in gate.connected_nets:
        for other_gate in circuit_copy.gates:
            if net_id in other_gate.connected_nets:
                connected.add(other_gate.GateID)
        for pad in circuit_copy.pads:
            if pad.NetNumberConnectedTo == net_id:
                connected.add(pad.PinID)
    return connected