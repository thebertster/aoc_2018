from lib.aoclib import AOCLib

def get_factors(n):
    factors = []
    trial = 1
    while (trial * trial) <= n:
        if n % trial == 0:
            factors.append(trial)
            factors.append(n // trial)
        trial += 1
    return factors

puzzle = (2018, 19)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

program = []

for line in puzzle_input[1:]:
    decoded = line.split(' ')
    program.append((decoded[0], tuple(int(v) for v in decoded[1:])))

program_length = len(program)

pc_reg = int(puzzle_input[0].split(' ')[1])

for reg_0_value in (0, 1):
    pc = 0
    registers = [reg_0_value, 0, 0, 0, 0, 0]
    while 0 <= pc < program_length:
        if pc == 1:
            # Program is calculating the sum of the factors of N
            # where N = registers[4] when PC == 1
            aoc.print_solution(1 + reg_0_value,
                               sum(get_factors(registers[4])))
            break
        op = program[pc][0]
        a, b, c = program[pc][1]
        registers[pc_reg] = pc
        if op[:3] == 'add':
            registers[c] = registers[a] + (b if op[3] == 'i'
                                           else registers[b])
        elif op[:3] == 'mul':
            registers[c] = registers[a] * (b if op[3] == 'i'
                                           else registers[b])
        elif op[:3] == 'ban':
            registers[c] = registers[a] & (b if op[3] == 'i'
                                           else registers[b])
        elif op[:3] == 'bor':
            registers[c] = registers[a] | (b if op[3] == 'i'
                                           else registers[b])
        elif op[:3] == 'set':
            registers[c] = a if op[3] == 'i' else registers[a]
        elif op[:2] == 'gt':
            registers[c] = int((a if op[2] == 'i' else registers[a]) >
                       (b if op[3] == 'i' else registers[b]))
        elif op[:2] == 'eq':
            registers[c] = int((a if op[2] == 'i' else registers[a]) ==
                       (b if op[3] == 'i' else registers[b]))
        else:
            raise ValueError('Unknown opcode')
        pc = registers[pc_reg] + 1
