from file_io.parser import parse
from file_io.writer import write_placement, verify_placement
from placement.placer import placer
from placement.partitioner import partitioner
from placement.containment import containment
from models.circuit import Circuit, Gate, Pad


BENCHMARKS = {
    'toy1': {
        'path': 'benchmarks/3QP/toy1',
        'gates': 18,
        'nets': 20,
        'pads': 6,
        'points': 20
    },
    'toy2': {
        'path': 'benchmarks/3QP/toy2',
        'gates': 32,
        'nets': 42,
        'pads': 10,
        'points': 20
    },
    'fract': {
        'path': 'benchmarks/3QP/fract',
        'gates': 125,
        'nets': 147,
        'pads': 24,
        'points': 20
    },
    'primary1': {
        'path': 'benchmarks/3QP/primary1',
        'gates': 752,
        'nets': 902,
        'pads': 107,
        'points': 20
    },
    'struct': {
        'path': 'benchmarks/3QP/struct',
        'gates': 1888,
        'nets': 1920,
        'pads': 64,
        'points': 20
    }
}

def main():
    # Convert benchmarks to list for indexed access
    benchmark_list = list(BENCHMARKS.items())
    
    # 1: toy1, 2: toy2, 3: fract, 4: primary1, 5: struct
    SELECTED_BENCHMARK = 1
        
    name, info = benchmark_list[SELECTED_BENCHMARK - 1]
    path = info['path']
    output_path = f'output.txt'

    input_circuit = parse(path)
    print(f"Circuit {path} contains {input_circuit.G} gates and {input_circuit.N} nets")

    # This looks okay
    QP1: Circuit = placer(input_circuit, 0, 100) 

    # This looks okay
    left_half, right_half = partitioner(QP1)  

    contained_left: Circuit = containment(left_half, QP1, 0, 50)

    QP2: Circuit = placer(contained_left, 0, 50)

    contained_right = containment(right_half, QP1, 50, 100)

    QP3 = placer(contained_right, 50, 100)

    # Merge the two partitions - QP2 and QP3
    # merged = Circuit(
    #     G=input_circuit.G,  # Keep original gate count
    #     N=input_circuit.N,  # Keep original net count
    #     gates=QP2.gates + QP3.gates,
    #     pads=input_circuit.pads  # Pads remain the same as original
    # )

    # write_placement(merged, output_path)
    write_placement(QP3, output_path)
    return 0


if __name__ == '__main__':
    main()