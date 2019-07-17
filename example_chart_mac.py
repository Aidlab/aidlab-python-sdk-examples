from Aidlab import AidlabBLECommunication as communication
import numpy as np
import time

# Uncomment if you encounter any problems with plotting
# import matplotlib
# matplotlib.use('TkAgg')

import matplotlib.pyplot as pyplot

second_in_milliseconds = 1000
buffer_size = 2000  # The bigger the buffer, the more we see


def live_plotter(x, y, line):

    if line == []:

        # This is the call to matplotlib that allows dynamic plotting
        pyplot.ion()
        fig = pyplot.figure(figsize=(13, 6))
        axis = fig.add_subplot(111)

        # Create a variable for the line so we can later update it
        line, = axis.plot(x, y, '', alpha=0.8)
        pyplot.show()

    # After the figure, axis, and line are created, we only need to update the
    # y-data
    line.set_ydata(y)

    # Adjust limits if new data goes beyond bounds
    pyplot.ylim([np.min(y) - np.std(y), np.max(y) + np.std(y)])

    # This pauses the data so the figure/axis can catch up - the amount of pause
    # can be altered above
    pyplot.pause(0.001)

    # Return line so we can update it again in the next iteration
    return line


class MainManager(communication.AidlabManager):

    def __init__(self):
        self.x = []
        self.y = []
        self.line = []
        self.time = self.current_time_in_milliseconds()
        self.sample_index = 0

        for i in range(buffer_size):
            self.x.append(i)
            self.y.append(0)

    def is_connected(self, address):
        print("Connected to: ", address)

    def is_disconnected(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def data_receiver(self, aidlab, characteristicName, data):

        self.sample_index += 1
        chart_refresh_rate_in_milliseconds = 100
        self.y[self.sample_index % buffer_size] = data[5]

        if self.current_time_in_milliseconds() - self.time > chart_refresh_rate_in_milliseconds:
            self.time = self.current_time_in_milliseconds()
            self.line = live_plotter(self.x, self.y, self.line)

    def current_time_in_milliseconds(self):
        global second_in_milliseconds
        return int(round(time.time() * second_in_milliseconds))


if __name__ == '__main__':

    characteristics = ["respiration"]

    main_manager = MainManager()
    main_manager.connect(characteristics)

    while True:
        pass
