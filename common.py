from dataclasses import dataclass


@dataclass
class Instruction:
    domain: str
    operation: str
    operands: list[str]


class IMapping:
    def apply(self, instr: Instruction) -> list[Instruction] | None:
        raise NotImplementedError()
