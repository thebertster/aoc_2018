from lib.aoclib import AOCLib

puzzle = (2018, 20)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

empty_room = {'N': None, 'E': None, 'S': None, 'W': None}
directions = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
backtrack = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}

current_position = (0, 0)
maze = {current_position: empty_room.copy()}
index = 1
bracket_stack = []

while True:
    c = puzzle_input[index]
    if c == '$':
        break
    elif c == '|':
        current_position = bracket_stack[-1]
    elif c == ')':
        bracket_stack.pop()
    elif c == '(':
        bracket_stack.append(current_position)
    else:
        new_position = (current_position[0] + directions[c][0],
                        current_position[1] + directions[c][1])
        if new_position not in maze:
            maze[new_position] = empty_room.copy()
        maze[new_position][backtrack[c]] = current_position
        maze[current_position][c] = new_position
        current_position = new_position
    index += 1

doors_passed_through = -1
next_rooms = [(0, 0)]
visited = set()
less_than_1000_doors = 0

while next_rooms:
    if doors_passed_through == 999:
        less_than_1000_doors = len(visited)
    doors_passed_through += 1
    new_next_rooms = []
    for next_room in next_rooms:
        new_next_rooms.extend([room for room in maze[next_room].values()
                               if room and room not in visited])
        visited.add(next_room)
    next_rooms = new_next_rooms

aoc.print_solution(1, doors_passed_through)
aoc.print_solution(1, len(visited) - less_than_1000_doors)
