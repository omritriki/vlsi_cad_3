from file_io.parser import parse


def main():
    toy1_path = 'benchmarks/3QP/toy1'
    circuit = parse(toy1_path)
    
    # Print parsed data
    print(f"Circuit contains {circuit.num_gates} gates and {circuit.num_nets} nets")
    print("\nGates:")
    for gate in circuit.gates:
        print(f"Gate {gate.id} is connected to nets: {gate.connected_nets}")
    print("\nPads:")
    for pad in circuit.pads:
        print(f"Pad {pad.id} is connected to net {pad.net_id} at position ({pad.x}, {pad.y})")
    
    return 0

if __name__ == '__main__':
    main()