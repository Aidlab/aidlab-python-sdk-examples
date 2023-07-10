#
# Plot.py
# Aidlab-SDK
# Created by Szymon Gesicki on 10.05.2020.
#

import numpy as np
import time
import matplotlib.pyplot as pyplot
import platform

if platform.system() == 'Darwin':
    # For older mac versions
    if int(platform.release().split('.')[0]) <= 20:
        import matplotlib
        matplotlib.use('TkAgg')

buffer_size = 750

class Plot:
    def __init__(self):
        self.y = [0] * buffer_size
        self.line = []
        self.time = time.time() * 1000
        self.sample_index = 0

    def live_plotter(self):
        if self.line == []:
            # This is the call to matplotlib that allows dynamic plotting
            pyplot.ion()
            self.fig = pyplot.figure(figsize=(13, 6))
            axis = self.fig.add_subplot(111)

            # Create a variable for the line so we can later update it
            self.line, = axis.plot(self.y, '', alpha=0.8)
            pyplot.show()

        # After the figure, axis, and line are created, we only need to update the
        # y-data
        self.line.set_ydata(self.y)

        # Adjust limits if new data goes beyond bounds
        pyplot.ylim([np.min(self.y) - np.std(self.y), np.max(self.y) + np.std(self.y)])

        # This pauses the data so the figure/axis can catch up - the amount of pause
        # can be altered above
        self.fig.canvas.flush_events()

    def add(self, value):
        self.y = self.y[1:] + [value]  # shift values in the buffer and append new one
        self.sample_index += 1

        if time.time() * 1000 - self.time > 200:
            self.time = time.time() * 1000
            self.live_plotter()
