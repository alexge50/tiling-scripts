import subprocess
from collections import namedtuple
import re

Window = namedtuple('Window', 'id desktop x y w h title')
Display = namedtuple('Display', 'x y w h')


def shell_command(command: str):
    return subprocess.check_output(['/bin/sh', '-c', command]).decode('utf-8')


def parse_window(line: str):
    line = [x for x in line.split(' ') if x != '']

    if len(line) == 0:
        return None

    return Window(
        line[0],
        line[1],
        int(line[2]),
        int(line[3]),
        int(line[4]),
        int(line[5]),
        ' '.join(line[7:])
    )


def get_displays():
    output = shell_command('xrandr')
    unparsed_geometries = re.compile(r'\bconnected (?:primary )?(?P<geometry>[0-9x+]+\b)').findall(output)

    def parse(geometry):
        numbers = re.compile('([0-9]+)').findall(geometry)
        return Display(
            int(numbers[2]),
            int(numbers[3]),
            int(numbers[0]),
            int(numbers[1])
        )

    return [parse(geometry) for geometry in unparsed_geometries]


def get_current_display(displays):
    output = shell_command('xdotool getmouselocation')
    output = output.split(' ')
    x = int(output[0][2:])
    y = int(output[1][2:])

    for display in displays:
        if display.x <= x <= display.x + display.w \
                and display.y <= y <= display.y + display.h:
            return display


def get_current_desktop():
    return shell_command("xprop -notype -root _NET_CURRENT_DESKTOP | cut -c 24-").strip()


def is_window_on_display(window, display, desktop):
    return window.desktop == desktop \
           and display.x <= window.x <= display.x + display.w \
           and display.y <= window.y <= display.y + display.h


def order_by_stack(desktop, windows):
    output = shell_command(f"xdotool search --all --onlyvisible --desktop {desktop} ''")
    window_dict = {
        int(window.id, base=16): window for window in windows
    }
    ids = [int(x.strip()) for x in output.split('\n')[1:] if x.strip() != '']

    return [window_dict[i] for i in ids if i in window_dict]


def get_windows():
    windows = [parse_window(line) for line in shell_command('wmctrl -l -G').split('\n')]
    return [window for window in windows if windows is not None]


def move_window(window_id, x, y, w, h):
    shell_command(f'xdotool windowsize {window_id} {w} {h}')
    shell_command(f'xdotool windowmove {window_id} {x} {y}')


def get_active_window():
    window_id = shell_command("printf 0x%08x `xdotool getactivewindow`")

    return parse_window(shell_command(f'wmctrl -l -G | grep {window_id}'))


def get_window_decoration_sizes(window_id):
    output = shell_command(f'xwininfo -id {window_id}')
    pattern = re.compile(r'(Relative upper-left [XY]: +[0-9]+)')
    relative_coords = [
        int(x.split(' ')[-1]) for x in pattern.findall(output)
    ]

    return relative_coords[0], relative_coords[1]

