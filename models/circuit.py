from dataclasses import dataclass
from typing import List

@dataclass
class Gate:
    id: int
    connected_nets: List[int]

@dataclass
class Pad:
    id: int
    net_id: int
    x: int
    y: int

@dataclass
class Circuit:
    num_gates: int
    num_nets: int
    gates: List[Gate]
    pads: List[Pad]