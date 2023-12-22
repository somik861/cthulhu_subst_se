from argparse import ArgumentParser
from pathlib import Path
from engine import Engine


def substitute(in_file: Path, out_file: Path, eng: Engine, mappings: set[str]) -> None:
    with open(in_file, 'r', encoding='utf-8') as inf, \
            open(out_file, 'w', encoding='utf-8', newline='\n') as outf:
        outf.writelines(eng.apply_mappings(inf.readlines(), mappings))


def main() -> None:
    eng = Engine()
    parser = ArgumentParser()
    parser.add_argument('in_file', type=Path,
                        help='Path to the input file with source code')
    parser.add_argument('out_file', type=Path,
                        help='Path to the output file with source code')
    parser.add_argument('-m', '--mapping', type=str,
                        help=f'One or more mappings to use',
                        choices=eng.get_valid_mappings(), nargs='+')

    args = parser.parse_args()
    substitute(args.in_file, args.out_file, eng, set(args.mapping))


if __name__ == '__main__':
    main()
