from common import IMapping, Instruction


def _make_unique_args(instr: Instruction, input_ops: int) -> list[Instruction] | None:
    if len(set(instr.operands)) == len(instr.operands):
        return None

    op_ints = list(map(lambda x: int(x), instr.operands))
    already_used = set(op_ints)
    taken: set[int] = set()
    new_op_ints = [-1] * len(op_ints)
    for i, op in enumerate(op_ints):
        # current position is valid
        if not op in taken:
            new_op_ints[i] = op
            taken.add(op)
            continue
        # find new position
        for j in range(1, 6):
            if j in already_used:
                continue
            new_op_ints[i] = j
            already_used.add(j)
            taken.add(j)
            break

    # build new instruction
    new_instrs: list[Instruction] = []
    for idx, (src, dest) in enumerate(zip(op_ints, new_op_ints)):
        # place instruction
        if idx == input_ops:
            new_instrs.append(Instruction(instr.domain, instr.operation, list(
                map(lambda x: str(x), new_op_ints))))

        # old and new positions are the same ... ignore
        if src == dest:
            continue

        # we are dealing with input op
        if idx < input_ops:
            new_instrs.append(Instruction(
                instr.domain, 'move', [str(src), str(dest)]))
        else:  # we are dealing with output op
            new_instrs.append(Instruction(
                instr.domain, 'move', [str(dest), str(src)]))

    return new_instrs


class Mapping(IMapping):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, instr: Instruction) -> list[Instruction] | None:
        match instr.operation:
            case 'move' | 'swap':
                if instr.operands[0] == instr.operands[1]:
                    return []
                return None

            case 'dup':
                return _make_unique_args(instr, 1)
            case 'add' | 'sub' | 'mul' | 'div' | 'mod' | 'eq' | 'neq' | 'lt' | 'le' | 'gt' | 'ge' | 'and' | 'xor' | 'or' | 'land' | 'lor':
                return _make_unique_args(instr, 2)
            case 'neg':
                return _make_unique_args(instr, 1)

        return None
