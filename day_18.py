from lib.aoclib import AOCLib

puzzle = (2018, 18)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

width = len(puzzle_input[0])
height = len(puzzle_input)

grid = {}

for y, line in enumerate(puzzle_input):
    for x, char in enumerate(line):
        grid[(x, y)] = char

minute = 0

past_grids = [tuple(grid.values())]

while True:
    minute += 1
    new_grid = {}
    for coords, square in grid.items():
        adjacent_squares = [grid[(x, y)]
                            for x in range(coords[0] - 1,
                                           coords[0] + 2)
                            for y in range(coords[1] - 1,
                                           coords[1] + 2)
                            if ((0 <= x < width) and
                                (0 <= y < height) and
                                not (x == coords[0] and y == coords[1]))]
        if square == '.':
            if adjacent_squares.count('|') >= 3:
                square = '|'
        elif square == '|':
            if adjacent_squares.count('#') >= 3:
                square = '#'
        elif square == '#':
            if (adjacent_squares.count('#') == 0 or
                    adjacent_squares.count('|') == 0):
                square = '.'
        new_grid[coords] = square
    grid = new_grid
    this_grid = tuple(grid.values())
    if this_grid in past_grids:
        cycle = past_grids.index(this_grid)
        break
    else:
        past_grids.append(this_grid)
    if minute == 10:
        aoc.print_solution(1, (this_grid.count('|') *
                               this_grid.count('#')))

final_grid = past_grids[cycle + (1000000000 - cycle) % (minute - cycle)]

aoc.print_solution(2, (final_grid.count('|') *
                       final_grid.count('#')))
