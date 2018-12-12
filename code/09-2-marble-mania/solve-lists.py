#!/usr/bin/env pypy3 -OO
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
    w *= 100

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


if __name__ == '__main__':
    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
