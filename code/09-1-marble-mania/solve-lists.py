#!/usr/bin/env python -OO
import re


class Node:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev or self
        self.next = next or self

    def insert(self, value):
        n = Node(value, prev=self, next=self.next)
        self.next.prev = n
        self.next = n
        return n

    def pop(self):
        self.next.prev = self.prev
        self.prev.next = self.next
        return self.next


def solve(t):
    n, w = map(int, re.findall(r'-?\d+', t))

    cur = Node(0)
    score = [0] * n

    for x in range(1, w + 1):
        p = (x - 1) % n

        if x % 23 == 0:
            i = cur
            for _ in range(7):
                i = i.prev
            score[p] += (x + i.value)
            cur = i.pop()
        else:
            i = cur.next
            cur = i.insert(x)

    return max(score)


def test():
    assert solve('9 players; last marble is worth 25 points') == 32
    assert solve('10 players; last marble is worth 1618 points') == 8317
    assert solve('13 players; last marble is worth 7999 points') == 146373
    assert solve('17 players; last marble is worth 1104 points') == 2764
    assert solve('21 players; last marble is worth 6111 points') == 54718
    assert solve('30 players; last marble is worth 5807 points') == 37305


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
