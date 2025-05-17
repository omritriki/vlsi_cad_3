from models.circuit import Circuit, Gate, Pad

def parse(file_path: str) -> Circuit:
    """
    Parse circuit description file and return Circuit object
    """
    print(f'Parsing {file_path}')
    
    with open(file_path, 'r') as f:
        # Parse first line: number of gates and nets
        num_gates, num_nets = map(int, f.readline().split())
        
        # Parse gates
        gates = []
        for _ in range(num_gates):
            line = list(map(int, f.readline().split()))
            gate_id = line[0]
            num_connections = line[1]
            connected_nets = line[2:2+num_connections]
            gates.append(Gate(gate_id, connected_nets))
            
        # Parse number of pads
        num_pads = int(f.readline())
        
        # Parse pads
        pads = []
        for _ in range(num_pads):
            pad_id, net_id, x, y = map(int, f.readline().split())
            pads.append(Pad(pad_id, net_id, x, y))
            
        return Circuit(num_gates, num_nets, gates, pads)