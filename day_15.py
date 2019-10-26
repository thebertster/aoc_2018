from lib.aoclib import AOCLib

def travel(from_here, that_way):
    return (from_here[0] + that_way[0],
            from_here[1] + that_way[1])

def find_distance(start_square, end_square, max_distance):
    candidates = [(None, start_square)]
    metric = 0
    visited = set()
    visited.add(start_square)

    while candidates and metric <= max_distance:
        new_candidates = []
        for first_step, candidate in candidates:
            if candidate == end_square:
                # First candidate path found will be both the
                # shortest distance and have the step that is first
                # in reading order since the first steps were added to
                # the queue based on reading order.
                return first_step, metric

            neighbours = (travel(candidate, direction)
                          for direction in directions)
            for new_candidate in neighbours:
                if (current_map[new_candidate] == '.' and
                    new_candidate not in visited):
                    visited.add(new_candidate)
                    new_candidates.append((new_candidate
                                           if metric == 0
                                           else first_step, new_candidate))

        candidates = new_candidates
        metric += 1

    return None, max_distance + 1

puzzle = (2018, 15)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

initial_map = {}
initial_unit_positions = {}

reading_order = lambda p: p[0][1]*dungeon_width + p[0][0]

infinity = 999999
start_hit_points = 200
initial_attempt = 3
attack_power = {'G': 3, 'E': initial_attempt}
dungeon_width = len(puzzle_input[0])
directions = ((0, -1), (-1, 0), (1, 0), (0, 1))

unit_count = {'G': 0, 'E': 0}

for y, line in enumerate(puzzle_input):
    for x, point in enumerate(line):
        if point in 'GE':
            initial_unit_positions[((x, y),
                                    point,
                                    unit_count[point])] = start_hit_points
            unit_count[point] += 1
        initial_map[(x, y)] = point

elves_victorious = False

while not elves_victorious:
    rounds = 0
    battle_in_progress = True
    unit_positions = initial_unit_positions.copy()
    current_map = initial_map.copy()

    while battle_in_progress:
        units = sorted(unit_positions.keys(),
                       key=reading_order)

        for position, unit_type, unit in units:
            if (position, unit_type, unit) not in unit_positions:
                # Unit was already killed earlier in the round!
                continue

            enemies = [target for target in
                       unit_positions.items() if target[0][1] != unit_type]

            if not enemies:
                # No enemies are left
                battle_in_progress = False
                hit_point_total = sum(unit_positions.values())

                if attack_power['E'] == initial_attempt:
                    aoc.print_solution(1, rounds * hit_point_total)
                elif (unit_type == 'E' and
                      attack_power['E'] > initial_attempt):
                    # Elves were successful
                    aoc.print_solution(2, rounds * hit_point_total)
                    elves_victorious = True
                break

            squares_in_range = [travel(position, direction)
                                for direction in directions]

            if not any(enemy[0][0] in squares_in_range
                       for enemy in enemies):
                # Move
                open_squares = set()
                for enemy in enemies:
                    for direction in directions:
                        square = travel(enemy[0][0], direction)
                        if current_map[square] == '.':
                            open_squares.add(square)

                if not open_squares:
                    # There are no in-range squares - end of turn
                    continue

                # Optimisation: Pre-sort the candidate squares by
                # manhattan distance.

                manhattan = lambda s, p=position: (abs(p[0] - s[0]) +
                                                   abs(p[1] - s[1]))

                open_squares_sorted = sorted(open_squares,
                                             key=manhattan)

                best_move = (None, None, infinity)
                for open_square in open_squares_sorted:
                    move, distance = find_distance(position,
                                                   open_square,
                                                   best_move[2])
                    if distance < best_move[2]:
                        best_move = (move, open_square, distance)
                    elif (distance == best_move[2] and
                          (open_square[1] < best_move[1][1] or
                           (open_square[1] == best_move[1][1] and
                            open_square[0] < best_move[1][0]))):
                        best_move = (move, open_square, distance)

                if best_move[0]:
                    hit_points = unit_positions.pop((position,
                                                     unit_type,
                                                     unit))
                    current_map[position] = '.'
                    current_map[best_move[0]] = unit_type
                    unit_positions[(best_move[0],
                                    unit_type, unit)] = hit_points
                    squares_in_range = [travel(best_move[0], direction)
                                        for direction in directions]
                else:
                    # No path to any in-range squares - end of turn
                    continue

            # Attack
            victim = [None, infinity]
            for target in (enemy for enemy in enemies
                           if enemy[0][0] in squares_in_range):
                if target[1] < victim[1]:
                    victim = target
                elif (target[1] == victim[1] and
                      (target[0][0][1] < victim[0][0][1] or
                       (target[0][0][1] == victim[0][0][1] and
                        target[0][0][0] < victim[0][0][0]))):
                    victim = target
            if victim[0]:
                unit_positions[victim[0]] -= attack_power[unit_type]
                if unit_positions[victim[0]] <= 0:

                    if (unit_type == 'G' and
                        attack_power['E'] > initial_attempt):
                        # If an elf has died and we are doing the second
                        # part of the puzzle, may as well abort!
                        battle_in_progress = False
                        break

                    current_map[victim[0][0]] = '.'
                    unit_positions.pop(victim[0])

        rounds += 1

    attack_power['E'] += 1
