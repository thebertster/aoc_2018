from lib.aoclib import AOCLib

puzzle = (2018, 14)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

recipe_scores = [3, 7]

elf_1 = 0
elf_2 = 1

target_length = int(puzzle_input) + 10
target_ending = [int(d) for d in puzzle_input]
target_ending_length = len(target_ending)

solved = 0

while solved < 2:
    recipe_sum = recipe_scores[elf_1] + recipe_scores[elf_2]
    for digit in [recipe_sum] if recipe_sum < 10 else [1, recipe_sum % 10]:
        recipe_scores.append(digit)

        if len(recipe_scores) == target_length:
            aoc.print_solution(1, ''.join(str(d)
                                          for d in recipe_scores[-10:]))
            solved += 1
        if recipe_scores[-target_ending_length:] == target_ending:
            aoc.print_solution(2, len(recipe_scores) - target_ending_length)
            solved += 1

    elf_1 = (elf_1 + recipe_scores[elf_1] + 1) % len(recipe_scores)
    elf_2 = (elf_2 + recipe_scores[elf_2] + 1) % len(recipe_scores)
