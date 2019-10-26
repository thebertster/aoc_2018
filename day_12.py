from lib.aoclib import AOCLib

class TuringPots:
    def __init__(self):
        self._pots = set()

    def populate_pots(self, initial_string):
        for i, plant in enumerate(initial_string):
            if plant == '#':
                self._pots.add(i)

    def potsum(self):
        return sum(self._pots)

    def get_pots(self, pot, extent):
        return ''.join('#' if p in self._pots else '.'
                        for p in range(pot - extent//2,
                                       pot + extent//2 + 1))

    def start_generation(self):
        self._newpots = self._pots.copy()

    def set_state(self, pot, state):
        if state:
            self._newpots.add(pot)
        elif pot in self._newpots:
            self._newpots.remove(pot)

    def end_generation(self):
        self._pots = self._newpots
        del self._newpots

    def get_extent(self):
        return (min(self._pots) if self._pots else 0,
                max(self._pots) if self._pots else 0)

    def get_pattern(self):
        leftmost = self.get_extent()[0]
        return [pot - leftmost for pot in self._pots]

puzzle = (2018, 12)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

rules = {}

for puzzle_line in puzzle_input[2:]:
    rule = puzzle_line.split(' => ')
    rules[rule[0]] = (rule[1] == '#')

pattern_len = 5

pots = TuringPots()
pots.populate_pots(puzzle_input[0][15:])

generation = 1
generations = [pots.get_pattern()]
potsums = [pots.potsum()]
repeat_generation = None

while True:
    left, right = pots.get_extent()
    pots.start_generation()
    for pot_to_check in range(left - pattern_len//2,
                              right + pattern_len//2 + 1):
        match = pots.get_pots(pot_to_check, pattern_len)
        if match in rules:
            pots.set_state(pot_to_check, rules[match])
        else:
            pots.set_state(pot_to_check, False)
    pots.end_generation()

    potsum = pots.potsum()

    if generation == 20:
        aoc.print_solution(1, potsum)

    plants = pots.get_pattern()
    if plants in generations:
        repeat_generation = generations.index(plants)
        cycle = generation - repeat_generation
        potsum_difference = potsum - potsums[repeat_generation]
    if repeat_generation and generation >= 20:
        break

    generations.append(plants)
    potsums.append(potsum)

    generation += 1

big_number = 50000000000

number_of_cycles = (big_number - repeat_generation) // cycle
additional_cycles = (big_number - repeat_generation) % cycle

aoc.print_solution(2, potsum_difference*number_of_cycles +
                   potsums[repeat_generation + additional_cycles])
