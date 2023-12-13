from argparse import ArgumentParser
from pathlib import Path
from engine import Engine

def substitute() -> None:
    pass

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('in_file', type=Path, help='Path to the input file with source code')
    parser.add_argument('out_file', type=Path, help='Path to the output file with source code')
    parser.add_argument('-m,--mapping', type=str, help='One or more mappings to use', nargs='+')

    args = parser.parse_args()

if __name__ == '__main__':
    main()