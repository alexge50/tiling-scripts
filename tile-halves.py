#!/usr/bin/env python
from util import *

current_desktop = get_current_desktop()
windows = get_windows()
displays = get_displays()
current_display = get_current_display(get_displays())

filtered_windows = [
    window for window in windows
    if is_window_on_display(window, current_display, current_desktop)]

filtered_windows = order_by_stack(current_desktop, filtered_windows)

if len(filtered_windows) < 2:
    import sys
    sys.exit()

window_1 = filtered_windows[-1]
window_2 = filtered_windows[-2]

gap = 10
padding_bottom = 33

w = (current_display.w - 3 * gap) // 2
h = current_display.h - 2 * gap - padding_bottom - 35

x = gap + current_display.x
y = gap + current_display.y

move_window(window_1.id, x, y, w, h)
move_window(window_2.id, x + w + gap, y, w, h)
