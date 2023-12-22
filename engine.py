from pathlib import Path
from common import IMapping, Instruction


class Engine:
    def __init__(self) -> None:
        self.mappings: dict[str, IMapping] = {}
        self._load_mappings()

    def get_valid_mappings(self) -> set[str]:
        return set(self.mappings.keys())

    def apply_mappings(self, lines: list[str], mappings: set[str]) -> list[str]:
        all_finished = False

        while not all_finished:
            new_lines: list[str] = []
            all_finished = True

            for line in lines:
                res = self._try_map(line, mappings)
                if res is None:
                    new_lines.append(line)
                else:
                    all_finished = False
                    indent = len(line) - len(line.lstrip())
                    for new_line in res:
                        new_lines.append(indent * ' ' + new_line)

            lines = new_lines

        return lines

    def _load_mappings(self) -> None:
        directory = Path(__file__).parent/'mappings'
        for entry in directory.iterdir():
            if entry.suffix != '.py':
                continue

            if entry.stem.startswith('__'):
                continue

            self.mappings[entry.stem] = getattr(__import__(
                'mappings', fromlist=[entry.stem]), entry.stem).Mapping()

    def _try_map(self, line: str, mappings: set[str]) -> list[str] | None:
        stripped = line.strip()

        if stripped == '':  # empty line
            return None
        if stripped.startswith('$'):  # constant
            return None
        if stripped.startswith('#'):  # is comment
            return None
        if stripped.endswith(':'):  # is dict or stack declaration
            return None
        if '=>' in stripped:  # dict mapping
            return None

        parts = stripped.split(' ')
        instruction = Instruction(parts[0], parts[1], parts[2:])
        for mapping in mappings:
            res = self.mappings[mapping].apply(instruction)
            if res is not None:
                return list(map(lambda x: ' '.join([x.domain, x.operation] + x.operands) + '\n', res))

        return None
