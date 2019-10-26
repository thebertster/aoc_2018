from lib.aoclib import AOCLib

puzzle = (2018, 21)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

magic_1 = int(puzzle_input[8].split(' ')[1])
magic_2 = int(puzzle_input[12].split(' ')[2])

# I hated this. Really hated it. Not enjoyable in any way shape or form.

part_1 = None
part_2 = None

history = set()

r4 = 0
while part_2 is None:
    r5 = r4 | 0x10000
    r4 = magic_1
    while True:
        r4 = (((r4 + (r5 & 0xff)) & 0xFFFFFF) * magic_2) & 0xFFFFFF
        if r5 < 256:
            if part_1 is None:
                part_1 = r4
                aoc.print_solution(1, part_1)
            else:
                if r4 not in history:
                    history.add(r4)
                    last_seen = r4
                else:
                    part_2 = last_seen
                break
        else:
            r5 //= 256

aoc.print_solution(1, part_2)
