#!/usr/bin/env python
from util import *
import argparse


def tile_full(args, work_area, window):
    print(args)
    border, title_bar = get_window_decoration_sizes(window.id)
    gap = args.gap

    w = work_area.w - 2 * gap - 2 * border
    h = work_area.h - 2 * gap - border - title_bar

    x = gap + work_area.x + border
    y = gap + work_area.y + title_bar

    move_window(window.id, x, y, w, h)


def tile_halves(args, work_area, window):
    border, title_bar = get_window_decoration_sizes(window.id)
    gap = args.gap

    x, y, w, h = [0] * 4

    if args.direction in ['W', 'E']:
        w = (work_area.w - 3 * gap - 4 * border) // 2
        h = work_area.h - 2 * gap - border - title_bar
    else:
        w = work_area.w - 2 * gap - 2 * border
        h = (work_area.h - 3 * gap - border - 2 * title_bar) // 2

    if args.direction in ['W', 'N']:
        x = gap + work_area.x
        y = gap + work_area.y
    elif args.direction == 'E':
        x = (work_area.w + gap) // 2 + work_area.x
        y = gap + work_area.y
    elif args.direction == 'S':
        x = gap + work_area.x
        y = (work_area.h + gap) // 2 + work_area.y

    x += border
    y += title_bar

    move_window(window.id, x, y, w, h)


def tile_thirds(args, work_area, window):
    border, title_bar = get_window_decoration_sizes(window.id)
    gap = args.gap

    x, y, w, h = [0] * 4

    if args.vertical:
        w = (work_area.w - 6 * border - 4 * gap) // 3
        h = work_area.h - 2 * gap - border - title_bar
        x = work_area.x + args.position * work_area.w // 3 + gap // 2
        y = work_area.y + gap
    else:
        w = work_area.w - 2 * gap - 2 * border
        h = (work_area.h - 4 * gap - 3 * border - 3 * title_bar) // 3
        x = work_area.x + gap
        y = work_area.y + args.position * work_area.h // 3 + gap // 2

    x += border
    y += title_bar

    move_window(window.id, x, y, w, h)


def tile_quarters(args, work_area, window):
    border, title_bar = get_window_decoration_sizes(window.id)
    gap = args.gap

    w = (work_area.w - 3 * gap - 4 * border) // 2
    h = (work_area.h - 3 * gap - border - 2 * title_bar) // 2

    direction = {
        'NW': (0, 0),
        'NE': (1, 0),
        'SW': (0, 1),
        'SE': (1, 1),
    }[args.direction]

    x = work_area.x + direction[0] * work_area.w // 2 + gap // (1 + direction[0]) + border
    y = work_area.y + direction[1] * work_area.h // 2 + gap // (1 + direction[1]) + title_bar

    move_window(window.id, x, y, w, h)


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
