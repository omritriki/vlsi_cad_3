from models.circuit import Circuit, Gate, Pad

def parse(file_path: str) -> Circuit:
    """
    Parse circuit description file and return Circuit object
    """    
    with open(file_path, 'r') as f:
        # Parse first line: number of gates and nets
        G, N = map(int, f.readline().split())
        
        # Parse gates
        gates = []
        for _ in range(G):
            line = list(map(int, f.readline().split()))
            GateID = line[0]
            num_connections = line[1]
            connected_nets = line[2:2+num_connections]
            gates.append(Gate(GateID, connected_nets))
            
        # Parse number of pads
        P = int(f.readline())
        
        # Parse pads
        pads = []
        for _ in range(P):
            PadID, NetID, x, y = map(int, f.readline().split())
            pads.append(Pad(PadID, NetID, x, y))
            
        return Circuit(G, N, gates, pads)