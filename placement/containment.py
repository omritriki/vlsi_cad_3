from models.circuit import Circuit, Gate, Pad
from typing import List, Set


def containment(gates: List[Gate], circuit: Circuit, side: int) -> Circuit:
    partition_gate_ids = {gate.GateID for gate in gates}
    
    connected_elements = set()
    for gate in gates:
        connected_elements.update(_find_connected_elements(gate, circuit))
    
    elements_to_move = connected_elements - partition_gate_ids
    
    for gate in circuit.gates:
        if gate.GateID in elements_to_move:
            if gate.floatXcoordinate is not None and (
                (side == 0 and gate.floatXcoordinate > 50) or
                (side == 1 and gate.floatXcoordinate < 50)
            ):
                gate.floatXcoordinate = 50.0
    
    for pad in circuit.pads:
        if pad.PinID in elements_to_move:
            if (side == 0 and pad.PinX > 50) or \
               (side == 1 and pad.PinX < 50):
                pad.PinX = 50
    
    side_name = "left" if side == 0 else "right"
    print(f"Moved {len(elements_to_move)} elements to centerline for {side_name} containment")
    return circuit


def _find_connected_elements(gate, circuit):
    connected = set()
    for net_id in gate.connected_nets:
        for other_gate in circuit.gates:
            if net_id in other_gate.connected_nets:
                connected.add(other_gate.GateID)
        for pad in circuit.pads:
            if pad.NetNumberConnectedTo == net_id:
                connected.add(pad.PinID)
    return connected