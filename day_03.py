from lib.aoclib import AOCLib

puzzle = (2018, 3)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

cloth = {}
claims = set()
non_viable = set()
oversubscription = 0

for claim in puzzle_input:
    parse = claim.split(' ')
    claim_number = int(parse[0][1:])
    claims.add(claim_number)
    corner = [int(coord) for coord in parse[2][:-1].split(',')]
    size = [int(dimension) for dimension in parse[3].split('x')]
    for y in range(size[1]):
        for x in range(size[0]):
            inch = (corner[0] + x, corner[1] + y)
            claimed_inch = cloth.get(inch, None)
            if not claimed_inch:
                cloth[inch] = [claim_number]
            else:
                if len(claimed_inch) == 1:
                    non_viable.add(claimed_inch[0])
                    oversubscription += 1
                claimed_inch.append(claim_number)
                non_viable.add(claim_number)

aoc.print_solution(1, oversubscription)

aoc.print_solution(2, claims - non_viable)
