from .defaults import default_time_line


def duration_lint(schedule_name, pair):
    if pair['type'] == 'Laboratory':
        return

    time = pair['time']

    start_time = time['start']
    end_time = time['end']

    start_i = -1
    end_i = -1

    for (i, (s, e)) in enumerate(default_time_line()):
        if start_i != -1 and end_i != -1:
            break

        if start_time == s:
            start_i = i

        if end_time == e:
            end_i = i

    if pair['title'] == 'Учебная практика' and pair['type'] == 'Seminar' and end_i - start_i == 2:
        return

    if end_i - start_i > 0:
        print(f'WARNING {schedule_name} - возможно неправильная длинна пары - {pair}')
