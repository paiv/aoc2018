#!/usr/bin/env python
import ctypes


def solve(text):
    solver = ctypes.cdll.LoadLibrary('build/solve.dylib')

    atype = ctypes.c_char_p * len(text)

    return solver.solve(len(text), len(text[0]), atype(*text))


if __name__ == '__main__':
    import fileinput
    with fileinput.input(mode='rb') as f:
        text = list(s.rstrip(b'\n') for s in f)
    print(solve(text))
