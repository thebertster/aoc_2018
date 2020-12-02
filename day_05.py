from lib.aoclib import AOCLib


def reduce_polymer(polymer_string, skip_unit=None):
    polymer = list(polymer_string)
    char_to_check = 0

    while char_to_check < len(polymer) - 1:
        while char_to_check < len(polymer) - 1:
            c1 = polymer[char_to_check]
            c1_lower = c1.lower()
            if c1_lower == skip_unit:
                polymer.pop(char_to_check)
            else:
                break
        while char_to_check < len(polymer) - 1:
            c2 = polymer[char_to_check + 1]
            c2_lower = c2.lower()
            if c2_lower == skip_unit:
                polymer.pop(char_to_check + 1)
            else:
                break
        else:
            c2_lower = None
        if (c1_lower == c2_lower and not c1.isupper() == c2.isupper()):
            polymer.pop(char_to_check)
            polymer.pop(char_to_check)
            if char_to_check > 0:
                char_to_check -= 1
        else:
            char_to_check += 1
    return len(polymer)


puzzle = (2018, 5)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

aoc.print_solution(1, reduce_polymer(puzzle_input))

polymers = []

for skip in 'abcdefghijklmnopqrstuvwxyz':
    polymers.append(reduce_polymer(puzzle_input, skip))

aoc.print_solution(2, min(polymers))
