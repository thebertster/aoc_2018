from lib.aoclib import AOCLib


def process_data_structure(raw_ds, index, node, metadata_sum):
    child_nodes = raw_ds[index]
    metadata_len = raw_ds[index + 1]
    node['child_nodes'] = []
    index += 2
    for child in range(child_nodes):
        child_node = {}
        node['child_nodes'].append(child_node)
        index, metadata_sum = process_data_structure(raw_ds, index,
                                                     child_node,
                                                     metadata_sum)

    node['metadata'] = raw_ds[index:index + metadata_len]

    return index + metadata_len, metadata_sum + sum(node['metadata'])


def get_node_value(node):
    children = len(node['child_nodes'])
    if children:
        return sum([get_node_value(node['child_nodes'][child - 1])
                    for child in node['metadata'] if child <= children])

    return sum(node['metadata'])


puzzle = (2018, 8)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1])

raw_data_structure = tuple(map(int, puzzle_input.split(' ')))

root_node = {}

checksum = process_data_structure(raw_data_structure, 0, root_node, 0)[1]

aoc.print_solution(1, checksum)
aoc.print_solution(2, get_node_value(root_node))
