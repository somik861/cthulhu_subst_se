from pathlib import Path
from common import IMapping


class Engine:
    def __init__(self) -> None:
        self.mappings: dict[str, IMapping] = {}

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
                    res = [line]
                new_lines.extend(res)

            lines = new_lines

        return lines

    def _load_mappings(self) -> None:
        directory = Path(__file__).parent/'mappings'
        for entry in directory.iterdir():
            if entry.suffix != '.py':
                continue

            if entry.stem.startswith('__'):
                continue

        self.mappings[entry.stem] = getattr(__import__('mappings', fromlist=[entry.stem]), entry.stem).Mapping

    def _try_map(self, line: str, mappings: set[str]) -> list[str] | None:
        stripped = line.strip()
        # TODO: map line

        return None
