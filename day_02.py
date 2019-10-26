from lib.aoclib import AOCLib

puzzle = (2018, 2)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

repeat_counts = {}

for box_id in puzzle_input:
    letter_counts = {}
    for letter in box_id:
        letter_counts[letter] = letter_counts.get(letter, 0) + 1

    box_letter_runs = {}
    for count in letter_counts.values():
        box_letter_runs[count] = box_letter_runs.get(count, 0) + 1

    for run_length, number in box_letter_runs.items():
        repeat_counts[run_length] = repeat_counts.get(run_length, 0) + 1

aoc.print_solution(1, repeat_counts[2] * repeat_counts[3])

difference_pos = None
correct_box_id = None

for box_number, box_id_1 in enumerate(puzzle_input):
    for box_id_2 in puzzle_input[:box_number]:
        for index, (letter_1, letter_2) in enumerate(zip(box_id_1,
                                                         box_id_2)):
            if letter_1 != letter_2:
                if difference_pos:
                    difference_pos = None
                    break
                else:
                    difference_pos = index
        if difference_pos:
            break
    if difference_pos:
        correct_box_id = (box_id_1[:difference_pos] +
                          box_id_1[difference_pos+1:])
        break

if correct_box_id:
    aoc.print_solution(2, correct_box_id)
else:
    print('Something went wrong!')
