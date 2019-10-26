from lib.aoclib import AOCLib

def process_instruction(op, a, b, c, r):
    if op[:3] == 'add':
        r[c] = r[a] + (b if op[3] == 'i' else r[b])
    elif op[:3] == 'mul':
        r[c] = r[a] * (b if op[3] == 'i' else r[b])
    elif op[:3] == 'ban':
        r[c] = r[a] & (b if op[3] == 'i' else r[b])
    elif op[:3] == 'bor':
        r[c] = r[a] | (b if op[3] == 'i' else r[b])
    elif op[:3] == 'set':
        r[c] = a if op[3] == 'i' else r[a]
    elif op[:2] == 'gt':
        r[c] = int((a if op[2] == 'i' else r[a]) >
                   (b if op[3] == 'i' else r[b]))
    elif op[:2] == 'eq':
        r[c] = int((a if op[2] == 'i' else r[a]) ==
                   (b if op[3] == 'i' else r[b]))
    else:
        raise ValueError('Unknown opcode')

puzzle = (2018, 16)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

puzzle_parts = [part.splitlines() for part in
                puzzle_input.split('\n\n\n\n')]

opcodes = ('addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr',
           'bori', 'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir',
           'eqri', 'eqrr')

start_states = []
instructions = []
end_states = []

for puzzle_block in range(0, len(puzzle_parts[0]), 4):
    start_states.append([int(reg) for reg
                   in puzzle_parts[0][puzzle_block][9:-1].split(',')])
    instructions.append([int(instruction_byte) for instruction_byte
                         in puzzle_parts[0][puzzle_block + 1].split(' ')])
    end_states.append([int(reg) for reg
                   in puzzle_parts[0][puzzle_block + 2][9:-1].split(',')])

opcode_behaves_like = {i: set() for i in range(len(opcodes))}
behaves_like_count = []

for start_state, instruction, end_state in zip(start_states,
                                               instructions,
                                               end_states):
    behaves_like_count.append(0)
    for opcode in opcodes:
        registers = start_state.copy()
        process_instruction(opcode,
                            instruction[1], instruction[2], instruction[3],
                            registers)
        if registers == end_state:
            opcode_behaves_like[instruction[0]].add(opcode)
            behaves_like_count[-1] += 1

aoc.print_solution(1, sum(1 for sample in behaves_like_count
                          if sample >= 3))
known_opcodes = {}

while len(known_opcodes) < len(opcodes):
    determined = list(number for number, opcode in
                  opcode_behaves_like.items() if len(opcode) == 1)
    for number in determined:
        (opcode,) = opcode_behaves_like.pop(number)
        known_opcodes[number] = opcode
        for other_number in opcode_behaves_like.keys():
            opcode_behaves_like[other_number].discard(opcode)

registers = [0, 0, 0, 0]

for program_line in puzzle_parts[1]:
    instruction = [int(instruction_byte) for instruction_byte
                   in program_line.split(' ')]
    process_instruction(known_opcodes[instruction[0]],
                        instruction[1], instruction[2], instruction[3],
                        registers)

aoc.print_solution(2, registers[0])
