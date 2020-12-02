from lib.aoclib import AOCLib


def scan_clay(boundary, y, direction):
    while True:
        boundary += direction
        if (boundary, y + 1) not in scan:
            # Water leaks down
            if y <= max_y:
                scan[(boundary, y)] = '|'
                water_squares.append((boundary, y))
                if y < max_y:
                    scan[(boundary, y + 1)] = '|'
                    water_squares.append((boundary, y + 1))
            return None
        check_flow = scan.get((boundary, y), ' ')
        if check_flow == '#':
            return boundary
        if check_flow == '|':
            if (boundary + direction, y) not in scan:
                return None
        scan[(boundary, y)] = '|'


puzzle = (2018, 17)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

scan = {}

for scan_line in puzzle_input:
    clay = scan_line.split(', ')
    coords = [coord.split('=') for coord in clay]
    coord_a = int(coords[0][1])
    coord_range = [int(value) for value in coords[1][1].split('..')]
    swap = (coords[0][0] == 'y')
    for coord_b in range(coord_range[0], coord_range[1] + 1):
        scan[(coord_b, coord_a) if swap else (coord_a, coord_b)] = '#'

min_y = min([coord[1] for coord in scan])
max_y = max([coord[1] for coord in scan])

scan[(500, min_y)] = '|'
water_squares = [(500, min_y)]

while water_squares:
    water_square = water_squares[-1]
    square_below = scan.get((water_square[0], water_square[1] + 1), ' ')
    if square_below in '#~':
        # We've hit bottom - let's go sideways
        water_squares.pop()
        left_boundary = scan_clay(water_square[0], water_square[1], -1)
        right_boundary = scan_clay(water_square[0], water_square[1], 1)
        if left_boundary and right_boundary:
            for x in range(left_boundary + 1, right_boundary):
                scan[(x, water_square[1])] = '~'
    elif square_below == ' ':
        if water_square[1] < max_y:
            scan[(water_square[0], water_square[1] + 1)] = '|'
            water_squares.append((water_square[0], water_square[1] + 1))
        else:
            water_squares.pop()
    elif square_below == '|':
        water_squares.pop()

accessible_water_squares = sum((1 for v in scan.values() if v in '|~'))

aoc.print_solution(1, accessible_water_squares)

undrained_water_squares = sum((1 for v in scan.values() if v in '~'))

aoc.print_solution(1, undrained_water_squares)
