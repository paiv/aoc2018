import argparse
import sys
from .tardis import assemble_files


def cli():
    parser = argparse.ArgumentParser(description='AoC 2018 Tardis VM Assembler')

    parser.add_argument('infile', nargs='*', default=sys.stdin, type=argparse.FileType('r'),
        help='Input assembly')
    parser.add_argument('-o', '--outfile', default=sys.stdout, type=argparse.FileType('w'),
        help='Write output to file')
    parser.add_argument('-g', '--generator', default='c', choices='c c-asm py'.split(),
        help='Select code generator')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='print details')

    args = parser.parse_args()

    assemble_files(
        args.infile,
        args.outfile,
        generator=args.generator,
        verbose=args.verbose,
    )
