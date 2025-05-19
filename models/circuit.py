from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Gate:
    GateID: int
    connected_nets: List[int]
    floatXcoordinate: Optional[float] = 0
    floatYcoordinate: Optional[float] = 0

@dataclass
class Pad:
    PinID: int
    NetNumberConnectedTo: int
    PinX: int
    PinY: int

@dataclass
class Circuit:
    G: int
    N: int
    gates: List[Gate]
    pads: List[Pad]