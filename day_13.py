from lib.aoclib import AOCLib

puzzle = (2018, 13)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

# Preprocess layout to find the carts etc.

cart_directions_chars = '<^>v'
cart_directions = ((-1, 0), (0, -1), (1, 0), (0, 1))

track = {}
cart_positions = {}

for y, line in enumerate(puzzle_input):
    for x, point in enumerate(line):
        if point in cart_directions_chars:
            direction = cart_directions_chars.index(point)
            cart = {'direction': direction, 'memory': 0}
            cart_positions[(x, y)] = cart
        elif point in '\\/+':
            track[(x, y)] = point

track_width = len(puzzle_input[0])

first_collision = True

while len(cart_positions) > 1:
    carts = sorted(cart_positions.items(),
                   key=lambda p: p[0][1]*track_width + p[0][0])
    for position, cart in carts:
        if position not in cart_positions:
            # Cart has already been collided with this tick!
            continue

        new_position = (position[0] + cart_directions[cart['direction']][0],
                        position[1] + cart_directions[cart['direction']][1])

        point = track.get(new_position, '?')

        turn = 0

        if point == '+':
            if cart['memory'] == 0:
                turn = -1
            elif cart['memory'] == 2:
                turn = 1
            cart['memory'] = (cart['memory'] + 1) % 3
        elif ((point == '\\' and cart['direction'] in [0, 2]) or
              (point == '/' and cart['direction'] in [1, 3])):
            turn = 1
        elif point in '\\/':
            turn = -1

        if turn:
            cart['direction'] = (cart['direction'] + turn) % 4

        cart_positions.pop(position)

        if new_position in cart_positions:
            cart_positions.pop(new_position)
            if first_collision:
                aoc.print_solution(1, '%d,%d' % (new_position[0],
                                                 new_position[1]))
                first_collision = False
        else:
            cart_positions[new_position] = cart

remaining_cart_position = list(cart_positions.keys())[0]

aoc.print_solution(2, '%d,%d' % (remaining_cart_position[0],
                                 remaining_cart_position[1]))
