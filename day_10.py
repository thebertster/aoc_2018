from lib.aoclib import AOCLib

puzzle = (2018, 10)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

x_coords = []
y_coords = []
velocities = []

for point in puzzle_input:
    x_coords.append(int(point[10:16]))
    y_coords.append(int(point[18:24]))
    velocities.append((int(point[36:38]), int(point[40:42])))

prev_height = None
second = 0

# Assume that the message will be displayed when the bounding box
# of the pattern has minimum height. This is not given in the
# problem definition, but is a reasonable first guess...
# ...which turned out to be correct.

while True:
    new_x_coords = []
    new_y_coords = []
    for x, y, (dx, dy) in zip(x_coords, y_coords, velocities):
        new_x_coords.append(x + dx)
        new_y_coords.append(y + dy)

    min_y = min(new_y_coords)
    max_y = max(new_y_coords)

    if prev_height and (max_y - min_y) > prev_height:
        break
    else:
        prev_height = (max_y - min_y)
    x_coords = new_x_coords
    y_coords = new_y_coords
    second += 1

min_y = min(y_coords)
min_x = min(x_coords)
max_y = max(y_coords)
max_x = max(x_coords)

width = (max_x - min_x) + 1
height = (max_y - min_y) + 1

blank_line = [' '] * width
screen = [blank_line[:] for line in range(height)]

for x, y in zip(x_coords, y_coords):
    screen[y - min_y][x - min_x] = '#'

message = '\n' + '\n'.join(''.join(line) for line in screen)

aoc.print_solution(1, message)

aoc.print_solution(2, second)
