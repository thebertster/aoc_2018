from lib.aoclib import AOCLib

# Could use deque for this, but trying to avoid using
# libraries, even 'simple' ones like 'collections'!

class FunkyStructure:
    def __init__(self, initial_value):
        self.pointer = [initial_value]
        self.pointer.extend([self.pointer] * 2)

    def add(self, value):
        new_node = [value, self.pointer, self.pointer[2]]
        self.pointer[2][1] = self.pointer[2] = self.pointer = new_node

    def rotate_by(self, amount):
        prev_or_next = 1 if amount > 0 else 2
        for click in range(abs(amount)):
            self.pointer = self.pointer[prev_or_next]

    def pop_tail(self):
        value = self.pointer[0]
        self.pointer[1][2] = self.pointer[2]
        self.pointer = self.pointer[2][1] = self.pointer[1]
        return value

puzzle = (2018, 9)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1]).split(' ')

number_of_players = int(puzzle_input[0])
last_marble = int(puzzle_input[6])

scores = [0] * number_of_players

marble_to_play = 1

marbles = FunkyStructure(0)

for puzzle_part in (1, 2):
    while marble_to_play <= last_marble:
        if marble_to_play % 23 == 0:
            marbles.rotate_by(7)
            removed_marble = marbles.pop_tail()
            scores[marble_to_play %
                   number_of_players] += marble_to_play + removed_marble
            marbles.rotate_by(-1)
        else:
            marbles.rotate_by(-1)
            marbles.add(marble_to_play)
        marble_to_play += 1

    aoc.print_solution(puzzle_part, max(scores))

    last_marble *= 100
