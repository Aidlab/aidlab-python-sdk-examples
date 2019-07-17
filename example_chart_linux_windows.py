from Aidlab import AidlabBLECommunication as comunication
import numpy as np
from multiprocessing import Process, Queue, Array
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation

buffer_size = 2000
result = None
x = []
y = []

# Fill the buffer
for i in range(1, buffer_size + 1):
    x.append(i)

figure = pyplot.figure()
axis = figure.add_subplot(1, 1, 1)


class MainManager(comunication.AidlabManager):

    def __init__(self):
        self.sample_index = 0

    def is_connected(self, address):
        global result,buffer_size
        print("Connected to: ", address)
        result = Array('d', buffer_size)
        Process(target=self.chart, args=(result,)).start()

    def is_disconnected(self, aidlab):
        print("Disconnected from: ", aidlab.address)

    def animate(self, i):
        global y
        axis.clear()
        axis.plot(x, y)
        pyplot.ylim([np.min(y) - np.std(y), np.max(y) + np.std(y)])

    def chart(self, result):
        global y
        y=result
        ani=animation.FuncAnimation(figure, self.animate, interval=2)
        pyplot.show()

    def data_receiver(self, aidlab, characteristic_name, data):
        global result,buffer_size
        self.sample_index += 1
        result[self.sample_index % buffer_size] = data[5]


if __name__ == '__main__':

    characteristics = ["respiration"]

    main_manager = MainManager()
    main_manager.connect(characteristics)

    # Start the connection
    while True:
        pass
