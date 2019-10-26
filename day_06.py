from lib.aoclib import AOCLib

puzzle = (2018, 6)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

coordinates = [tuple(map(int, coordinate.split(', '))) for
               coordinate in puzzle_input]

max_x = max(coordinates, key=lambda coordinate: coordinate[0])[0]
max_y = max(coordinates, key=lambda coordinate: coordinate[1])[1]
extreme = max_x if max_x > max_y else max_y

sniff_distance = 0
distance_map = {}

sniffed = set()

areas = {coordinate:0 for coordinate in coordinates}

for sniff_distance in range(extreme + 1):
    for coordinate in coordinates:
        if coordinate not in sniffed:
            found_edge = True
            for y in range(-sniff_distance, sniff_distance + 1):
                for x in {abs(y) - sniff_distance,
                          sniff_distance - abs(y)}:
                    candidate = (coordinate[0] + x, coordinate[1] + y)
                    if (candidate[0] >= 0 and candidate[0] <= max_x and
                        candidate[1] >= 0 and candidate[1] <= max_y):
                        if candidate in distance_map:
                            if distance_map[candidate][1] == sniff_distance:
                                areas[distance_map[candidate][0]] -= 1
                                distance_map[candidate] = (None, -1)
                        else:
                            distance_map[candidate] = (coordinate,
                                                       sniff_distance)
                            found_edge = False
                            areas[coordinate] += 1
            if found_edge:
                sniffed.add(coordinate)

for check in range(extreme + 1):
    for check_coord in ((0, check), (check, 0),
                        (max_x, check), (check, max_y)):
        check_value = distance_map.get(check_coord, None)
        if check_value:
            areas.pop(check_value[0], None)

aoc.print_solution(1, max(areas.values()))

max_distance = 10000
num_coordinates = len(coordinates)
min_x = min(coordinates, key=lambda coordinate: coordinate[0])[0]
min_y = min(coordinates, key=lambda coordinate: coordinate[1])[1]
sum_x_coords = sum([coordinate[0] for coordinate in coordinates])
sum_y_coords = sum([coordinate[1] for coordinate in coordinates])
ceiling_distance = -(-max_distance//num_coordinates)

smallest_possible_x = min_x - ceiling_distance
smallest_possible_y = min_y - ceiling_distance
largest_possible_x = max_x + ceiling_distance
largest_possible_y = max_y + ceiling_distance

area_size = 0

for y in range(smallest_possible_y, largest_possible_y + 1):
    for x in range(smallest_possible_x, largest_possible_x + 1):
        distance = sum([abs(x - coordinate[0]) + abs(y - coordinate[1])
                        for coordinate in coordinates])
        if distance < max_distance:
            area_size += 1

aoc.print_solution(2, area_size)
