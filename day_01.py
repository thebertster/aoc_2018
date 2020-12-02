from lib.aoclib import AOCLib

puzzle = (2018, 1)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list_int)

one_full_iteration = sum(puzzle_input)

aoc.print_solution(1, one_full_iteration)

# If one_full_iteration == 0 then the first repeated frequency either
# occurs somewhere within the first iteration, or is zero.
#
# If one_full_iteration != 0 then:
#
# Observation 1:
#
# The repeated frequency must occur during the first iteration through
# the frequencies. Each iteration produces a set of frequencies
# incremented by exactly one_full_iteration from the previous set and so
# if a frequency f is repeated in positions x and y in iterations m and n
# then frequency f-one_full_iteration was repeated in positions x and y
# in iterations m-1 and n-1. By descent, a repeated frequency must occur
# in a situation where either m or n is 1.
#
# Observation 2:
#
# If the repeated frequency f occurs in position x in the first iteration
# and position y in the nth iteration, then the frequency at position y
# in the first iteration must be congruent to f modulo one_full_iteration.
#
# We therefore search through pairs of frequencies f, q in the first
# iteration such that f = q mod one_full_iteration and such that the
# number of iterations separating the repeated frequency is minimal.

smallest_difference = None
repeated_frequency = None
accumulator = []

for change in puzzle_input:
    f = accumulator[-1] + change if accumulator else change
    if f == 0:
        repeated_frequency = 0
        break
    for q in accumulator:
        if f == q:
            repeated_frequency = f
            break
        if one_full_iteration != 0 and (f - q) % one_full_iteration == 0:
            difference = abs((f - q) // one_full_iteration)
            if (smallest_difference is None or
                    difference < smallest_difference):
                smallest_difference = difference
                repeated_frequency = (max(f, q) if one_full_iteration > 0
                                      else min(f, q))
    accumulator.append(f)

if repeated_frequency is not None:
    aoc.print_solution(2, repeated_frequency)
else:
    print('Something went wrong!')
