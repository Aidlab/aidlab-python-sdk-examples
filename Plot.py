#
# Plot.py
# Aidlab-SDK
# Created by Szymon Gesicki on 10.05.2020.
#

import platform
import time

import matplotlib.pyplot as pyplot
import numpy as np
from matplotlib.lines import Line2D

if platform.system() == 'Darwin' and int(platform.release().split('.')[0]) <= 20:
    # For older mac versions
    import matplotlib

    matplotlib.use('TkAgg')

buffer_size = 750

class Plot:
    def __init__(self):
        self.y = [0] * buffer_size
        self.line: Line2D | None = None
        self.time = time.time() * 1000
        self.sample_index = 0

    def live_plotter(self):
        if self.line is None:
            # This is the call to matplotlib that allows dynamic plotting
            pyplot.ion()
            self.fig = pyplot.figure(figsize=(13, 6))
            axis = self.fig.add_subplot(111)

            # Create a variable for the line so we can later update it
            (self.line,) = axis.plot(self.y, "", alpha=0.8)
            pyplot.show()

        # After the figure, axis, and line are created, we only need to update the
        # y-data
        self.line.set_ydata(self.y)

        # Adjust limits if new data goes beyond bounds
        min_y = float(np.min(self.y))
        max_y = float(np.max(self.y))
        padding = float(np.std(self.y))
        if min_y == max_y:
            padding = max(padding, 1e-3)
        pyplot.ylim([min_y - padding, max_y + padding])

        # This pauses the data so the figure/axis can catch up - the amount of pause
        # can be altered above
        self.fig.canvas.flush_events()

    def add(self, value):
        self.y = self.y[1:] + [value]  # shift values in the buffer and append new one
        self.sample_index += 1

        if time.time() * 1000 - self.time > 200:
            self.time = time.time() * 1000
            self.live_plotter()
