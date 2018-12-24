import argparse
import sys
from .tardis import assemble_files


def cli():
    parser = argparse.ArgumentParser(description='AoC 2018 Tardis VM Assembler')

    parser.add_argument('infile', nargs='*', default=sys.stdin, type=argparse.FileType('r'),
        help='assembly file')
    parser.add_argument('-o', '--outfile', nargs='?', default=sys.stdout, type=argparse.FileType('w'),
        help='assembly file')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='print details')

    args = parser.parse_args()

    assemble_files(
        args.infile,
        args.outfile,
        verbose=args.verbose
    )
