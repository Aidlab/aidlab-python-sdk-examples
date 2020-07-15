from Aidlab.Aidlab import Aidlab
import numpy as np
from multiprocessing import Process, Queue, Array
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

buffer_size = 500
result = None
x = [i for i in range(buffer_size)]
y = []

figure = pyplot.figure()
axis = figure.add_subplot(1, 1, 1)


def animate(i):
    global y
    axis.clear()
    axis.plot(x, y)
    pyplot.ylim([np.min(y) - np.std(y), np.max(y) + np.std(y)])


def chart(result):
    global y
    y = result
    ani = animation.FuncAnimation(figure, animate, interval=2)
    pyplot.show()


class MainManager(Aidlab):

    def __init__(self):
        super().__init__()
        self.sample_index = 0
        self.skip = 0

    def did_connect(self, aidlab):
        print("Connected to: ", aidlab.address)

    def did_disconnect(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def did_receive_ecg(self, aidlab, timestamp, value):
        self.skip += 1
        if self.skip % 12 == 0:
            global result, buffer_size
            self.sample_index += 1
            result[self.sample_index % buffer_size] = value


if __name__ == '__main__':
    # create process  for Plot
    result = Array('d', buffer_size)
    Process(target=chart, args=(result,)).start()

    signals = ["ecg"]

    main_manager = MainManager()
    main_manager.connect(signals)

    # Start the connection
    while True:
        pass
