from lib.aoclib import AOCLib

def solve_puzzle(dependencies):
    prerequisites = {}
    all_steps = set()
    unavailable_steps = set()

    for dependency in dependencies:
        step = dependency[36]
        depends_on = dependency[5]
        prerequisite = prerequisites.get(step, None)
        if prerequisite:
            prerequisite.add(depends_on)
        else:
            prerequisites[step] = {depends_on}
            all_steps.add(depends_on)
        unavailable_steps.add(step)
        all_steps.add(step)

    aoc.print_solution(1, do_work(all_steps, unavailable_steps.copy(),
                                  prerequisites)[1])

    aoc.print_solution(2, do_work(all_steps, unavailable_steps.copy(),
                                  prerequisites, num_workers=5,
                                  time_calc=lambda x: 60 + x))

def do_work(all_steps, unavailable_steps, prerequisites,
            num_workers=1, time_calc=lambda x: 1):
    step_order = ''
    workers = {}

    available_steps = all_steps - unavailable_steps

    completed_steps = set()

    second = 0

    while completed_steps != all_steps:
        # Assign workers to available work
        while available_steps and len(workers) < num_workers:
            next_step = min(available_steps)
            available_steps.discard(next_step)
            completion_time = second + time_calc(ord(next_step) - 64)
            workers[completion_time] = next_step

        # Get the next event

        second = min(workers.keys())
        completed_step = workers.pop(second)
        step_order += completed_step
        completed_steps.add(completed_step)
        for step in unavailable_steps:
            if prerequisites[step].issubset(completed_steps):
                available_steps.add(step)
        unavailable_steps.difference_update(
            available_steps.union(completed_steps))

    return second, step_order

# Main Program

puzzle = (2018, 7)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

solve_puzzle(puzzle_input)
