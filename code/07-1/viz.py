#!/usr/bin/env python
import graphviz
import os


def main(fn):
    g = graphviz.Digraph('Sleigh')
    g.node_attr['shape'] = 'box'
    g.node_attr['style'] = 'rounded'

    with open(fn, 'r') as f:
        for line in f.readlines():
            p = line.split()
            g.edge(p[1], p[7])

    fn,_ = os.path.splitext(os.path.basename(fn))
    fn = g.render(filename=fn, format='pdf', cleanup=True)
    print(fn)


if __name__ == '__main__':
    import sys
    main(sys.argv[1])
