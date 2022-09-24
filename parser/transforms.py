from .defaults import default_time_line


def duration_fixer(pair):
    if pair['type'] == 'Lecture':
        pair['time'] = {
            'start': pair['time']['start'],
            'end': _end_time_for(pair['time'], offset=0)
        }
    elif pair['type'] == 'Seminar':
        if pair['title'] == 'Учебная практика':
            pair['time'] = {
                'start': pair['time']['start'],
                'end': _end_time_for(pair['time'], offset=2)
            }
        else:
            pair['time'] = {
                'start': pair['time']['start'],
                'end': _end_time_for(pair['time'], offset=0)
            }
    elif pair['type'] == 'Laboratory':
        pair['time'] = {
            'start': pair['time']['start'],
            'end': _end_time_for(pair['time'], offset=1)
        }

    return pair


def _end_time_for(time, offset=0):
    for (i, (s, e)) in enumerate(default_time_line()):
        if s == time['start']:
            if offset == 0:
                return e
            else:
                return default_time_line()[i + offset][1]

    return time['end']
