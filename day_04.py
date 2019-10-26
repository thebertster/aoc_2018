from datetime import datetime, date, time, timedelta
from lib.aoclib import AOCLib

puzzle = (2018, 4)

# Initialise the helper library

aoc = AOCLib(puzzle[0])

puzzle_input = aoc.get_puzzle_input(puzzle[1], AOCLib.lines_to_list)

guard_days = {}
sleep_start_times = []
wake_start_times = []

for entry in puzzle_input:
    entry_date = date(int(entry[1:5]),
                               int(entry[6:8]),
                               int(entry[9:11]))
    entry_time = time(int(entry[12:14]),
                               int(entry[15:17]))

    entry_type = entry[19]

    if entry_type == 'G':
        guard_number = int(entry[26:].split(' ')[0])
        if entry_time.hour != 0:
            entry_date += timedelta(days=1)
        guard_days[entry_date] = guard_number
    elif entry_type == 'f':
        sleep_start_times.append(datetime.combine(entry_date, entry_time))
    elif entry_type == 'w':
        wake_start_times.append(datetime.combine(entry_date, entry_time))

guard_sleep_cycles = {}

for sleep_start in sleep_start_times:
    guard_number = guard_days[sleep_start.date()]
    if guard_number not in guard_sleep_cycles:
        guard_sleep_cycles[guard_number] = [0] * 60
    for minute in range(sleep_start.minute, 60):
        guard_sleep_cycles[guard_number][minute] += 1

for wake_start in wake_start_times:
    guard_number = guard_days[wake_start.date()]
    for minute in range(wake_start.minute, 60):
        guard_sleep_cycles[guard_number][minute] -= 1

sleepiest_guard = max(guard_sleep_cycles.items(), key=lambda x: sum(x[1]))[0]

guard_sleep_cycle = enumerate(guard_sleep_cycles[sleepiest_guard])

sleepiest_minute = max(guard_sleep_cycle, key=lambda x: x[1])[0]

aoc.print_solution(1, sleepiest_minute * sleepiest_guard)

sleep_matrix = {(guard, minute): sleep_count for (guard, guard_sleep_cycle)
                in guard_sleep_cycles.items() for (minute, sleep_count)
                in enumerate(guard_sleep_cycle)}

opportune_moment = max(sleep_matrix.items(), key=lambda x: x[1])[0]

aoc.print_solution(2, opportune_moment[0] * opportune_moment[1])
