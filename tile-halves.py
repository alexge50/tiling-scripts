#!/usr/bin/env python
from util import *
import argparse


def tile_full(args, work_area, window):
    pass


def tile_halves(args, work_area, window):
    pass


def tile_thirds(args, work_area, window):
    pass


def tile_quarters(args, work_area, window):
    pass


parser = argparse.ArgumentParser(description='')
parser.add_argument(
    '--work-area-padding',
    nargs=4,
    default=[0, 0, 0, 0],
    help='workspace padding in pixels, format: <bottom> <upper> <left> <right>',
    dest='padding')
parser.add_argument(
    '--gap',
    nargs=1,
    default=0,
    type=int,
    help='workspace padding in pixels, format: <bottom> <upper> <left> <right>',
    dest='padding')
subparser = parser.add_subparsers('')
tile_full_parser = subparser.add_parser('tile-full', help='tile active window on the entire work area')
tile_full_parser.set_defaults(func=tile_full)
tile_halves_parser = subparser.add_parser('tile-halves', help='tile active window on half of the work area')
tile_halves_parser.add_argument('direction', default='N')
tile_halves_parser.set_defaults(func=tile_halves)
tile_thirds_parser = subparser.add_parser('tile-thirds', help='tile active window on a third of the work area')
tile_thirds_parser.add_argument('--horizontal', help='tile windows horizontally, defaults to vertical tiling')
tile_thirds_parser.add_argument('position', default=0, type=int)
tile_thirds_parser.set_defaults(func=tile_thirds)
tile_quarters_parser = subparser.add_parser('tile-quarters', help='tile active window on the work area')
tile_quarters_parser.add_argument('direction', default='NW')
tile_quarters_parser.set_defaults(func=tile_quarters)

args = parser.parse_args()
padding = [int(x) for x in args.padding]

current_display = get_current_display(get_displays())
window = get_active_window()

work_area = Display(
    current_display.x + padding[3],  # right padding
    current_display.y + padding[1],  # upper padding
    current_display.w - padding[2] - padding[3],  # left and right padding
    current_display.h - padding[0] - padding[1],  # bottom and upper padding
)

args.func(args, work_area, window)
