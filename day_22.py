from lib.aoclib import AOCLib
from lib.pqueue import PriorityQueue

class CaveSystem:
    def __init__(self, target_location, target_depth):
        self.cave_data = {}
        self.target = target_location
        self.depth = target_depth

    def get_type(self, location):
        if location not in self.cave_data:
            for yy in range(location[1] + 1):
                for xx in range(location[0] + 1):
                    if (xx, yy) not in self.cave_data:
                        if (xx, yy) in [(0, 0), self.target]:
                            geologic_index = 0
                        elif yy == 0:
                            geologic_index = xx * 16807
                        elif xx == 0:
                            geologic_index = yy * 48271
                        else:
                            geologic_index = (self.cave_data[(xx - 1, yy)][0] *
                                              self.cave_data[(xx, yy - 1)][0])
                        erosion_level = (geologic_index + self.depth) % 20183
                        self.cave_data[(xx, yy)] = (erosion_level,
                                                  erosion_level % 3)

        return self.cave_data[location][1]

puzzle = (2018, 22)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

depth = int(puzzle_input[0].split(' ')[1])
target = tuple(map(int, puzzle_input[1].split(' ')[1].split(',')))

cave = CaveSystem(target, depth)

cave.get_type((target[0] + 50, target[1] + 50))

total_risk = 0

for y in range(target[1] + 1):
    for x in range(target[0] + 1):
        total_risk += cave.get_type((x, y))

aoc.print_solution(1, total_risk)

start_state = (0, 0, 0)
target_state = (target[0], target[1], 0)
valid_tools = ((0, 1), (1, 2), (0, 2))

node_set = PriorityQueue()
expanded = set()

node_set.push(0, (0, 0, 0))

node_distance = -1

while node_set.size() > 0:
    node_distance, min_node = node_set.pop()

    print(min_node, node_distance)

    if min_node == target_state:
        break

    if min_node not in expanded:
        expanded.add(min_node)
        x, y, t = min_node
        region_type = cave.get_type((x, y))
        tools = valid_tools[region_type]
        change_tool_node = (x, y, tools[1-tools.index(t)])
        if change_tool_node not in expanded:
            node_set.rekey(change_tool_node, node_distance + 7)

        for d in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            x_2, y_2 = x + d[0], y + d[1]
            if x_2 >= 0 and y_2 >= 0 and x_2 < target[1] + 20:
                region_type_2 = cave.get_type((x_2, y_2))
                tools_2 = valid_tools[region_type_2]
                if t in tools_2:
                    move_node = (x_2, y_2, t)
                    if move_node not in expanded:
                        node_set.rekey(move_node, node_distance + 1)

aoc.print_solution(2, node_distance)
