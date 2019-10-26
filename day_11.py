from lib.aoclib import AOCLib

puzzle = (2018, 11)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], int)

grid_power_levels = {}
best_subgrid = {}

# Calculate power levels of each grid size using one of three methods:
#
# If grid_size == 1, use the provided formula to calculate the cell power level
#
# If grid_size is even, just sum the four quarter-grids which we have
# calculated previously.
#
# otherwise add up the top-left and bottom-right grids one smaller than the
# current size; this counts the centre grid of size grid_size-2 twice, so
# subtract this. Finally, add the cells at the bottom-left and top-right.

for grid_size in range(1, 301):
    grid_power_levels[grid_size] = {}
    if grid_size == 1:
        for x in range(1, 301):
            rack_id = x + 10
            for y in range(1, 301):
                power_level = (((y*rack_id + puzzle_input) *
                                rack_id) // 100) % 10 - 5
                grid_power_levels[1][(x, y)] = power_level
    elif grid_size % 2 == 0:
        half = grid_size / 2
        for x in range(1, 302 - grid_size):
            for y in range(1, 302 - grid_size):
                power_level = (grid_power_levels[half][(x, y)] +
                               grid_power_levels[half][(x + half, y)] +
                               grid_power_levels[half][(x, y + half)] +
                               grid_power_levels[half][(x + half, y + half)])
                grid_power_levels[grid_size][(x, y)] = power_level
    else:
        for x in range(1, 302 - grid_size):
            for y in range(1, 302 - grid_size):
                tl = grid_power_levels[grid_size - 1][(x, y)]
                br = grid_power_levels[grid_size - 1][(x + 1, y + 1)]
                c = grid_power_levels[grid_size - 2][(x + 1, y + 1)]
                bl = grid_power_levels[1][(x, y + grid_size - 1)]
                tr = grid_power_levels[1][(x + grid_size - 1, y)]
                power_level = tl + br - c + bl + tr

                grid_power_levels[grid_size][(x, y)] = power_level

    best_subgrid[grid_size] = max(grid_power_levels[grid_size].items(),
                                  key=lambda p: p[1])
    if grid_size == 3:
        aoc.print_solution(1, '%d,%d' % (best_subgrid[3][0][0],
                                         best_subgrid[3][0][1]))

best_overall = max(best_subgrid.items(), key=lambda p: p[1][1])

aoc.print_solution(2, '%d,%d,%d' % (best_overall[1][0][0],
                                    best_overall[1][0][1],
                                    best_overall[0]))
