#
# Plot.py
# Aidlab-SDK
# Created by Szymon Gesicki on 10.05.2020.
#
import numpy as np
import time

# Uncomment if you encounter any problems with plotting
# import matplotlib
# matplotlib.use('TkAgg')

import matplotlib.pyplot as pyplot

second_in_milliseconds = 1000
# The bigger the buffer, the more we see
buffer_size = 1000


class Plot:

    def __init__(self):
        self.x = [i for i in range(buffer_size)]
        self.y = [0] * buffer_size
        self.line = []
        self.time = self.current_time_in_milliseconds()
        self.sample_index = 0
        self.skip = 0

    def live_plotter(self):

        if self.line == []:

            # This is the call to matplotlib that allows dynamic plotting
            pyplot.ion()
            self.fig = pyplot.figure(figsize=(13, 6))
            axis = self.fig.add_subplot(111)

            # Create a variable for the line so we can later update it
            self.line, = axis.plot(self.x, self.y, '', alpha=0.8)
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
        self.skip += 1

        if self.skip % 6 == 0:
            self.sample_index += 1

            chart_refresh_rate_in_milliseconds = 100
            # shift left
            self.y[:-1] = self.y[1:]
            self.y[-1] = value

            if self.current_time_in_milliseconds() - self.time > chart_refresh_rate_in_milliseconds:
                self.time = self.current_time_in_milliseconds()
                self.live_plotter()

    def current_time_in_milliseconds(self):
        global second_in_milliseconds
        return int(round(time.time() * second_in_milliseconds))
