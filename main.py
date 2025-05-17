from file_io.parser import parse
from file_io.writer import write_placement, verify_placement
from placement.placer import placer

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
    SELECTED_BENCHMARK = 5
        
    name, info = benchmark_list[SELECTED_BENCHMARK - 1]
    path = info['path']
    output_path = f'output.txt'

    circuit = parse(path)
    print(f"Circuit {path} contains {circuit.G} gates and {circuit.N} nets")

    QP1 = placer(circuit) 

    write_placement(QP1, output_path)
    
    return 0

if __name__ == '__main__':
    main()