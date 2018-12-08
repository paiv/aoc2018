#!/usr/bin/env python


class Node:
    def __init__(self, parent=None):
        self.parent = parent
        if parent:
            parent.children.append(self)
        self.children = list()
        self.meta = list()

    def __repr__(self):
        return '{}-{}'.format(tuple(self.meta), self.children)

    def value(self):
        if not self.children:
            return sum(self.meta)
        return sum((self.children[i-1].value() if 0 < i <= len(self.children) else 0)
            for i in self.meta)


def solve(t):
    reader = map(int, t.split())

    def parse_node(reader, parent=None, level=0):
        state = 1

        while state:
            x = next(reader)

            if state == 1:
                npending = x
                node = Node(parent)
                state = 2

            elif state == 2:
                mpending = x

                for _ in range(npending):
                    parse_node(reader, node, level=level+1)

                state = 3 if mpending else 0

            elif state == 3:
                node.meta.append(x)
                mpending -= 1
                state = 3 if mpending else 0

        return node

    root = parse_node(reader)

    return root.value()


def test():
    assert solve('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2') == 66


if __name__ == '__main__':
    test()

    import fileinput
    with fileinput.input() as f:
        text = ''.join(f).strip('\n')

    print(solve(text))
