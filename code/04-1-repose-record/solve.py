#!/usr/bin/env python -OO
from collections import Counter, defaultdict
from datetime import datetime


def solve(input):
    def parse(s):
        dt = datetime.strptime(s[1:17], '%Y-%m-%d %H:%M')
        n, id, *_ = s[19:].split()
        if n == 'Guard':
            id = int(id[1:])
            return dt, n, id
        return dt, n, None

    data = defaultdict(Counter)
    gid = None
    start = None
    for dt, wat, id in sorted(map(parse, input.splitlines())):
        if wat == 'Guard':
            gid = id
        elif wat == 'falls':
            start = dt
        elif wat == 'wakes':
            data[gid] += Counter({i:1 for i in range(start.minute, dt.minute)})

    xs = [(sum(c.values()), id, c.most_common(1)[0]) for id, c in data.items() if c]

    _, id, (m, _) = max(xs)
    return id * m



def test():
    t = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""".strip('\n')

    assert solve(t) == 240


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
