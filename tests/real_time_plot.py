# -*- coding: utf-8 -*-
from __future__ import print_function, division
from modular_device import ModularDevice
import time


# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

# def update_line(num, data, line):
#     line.set_data(data[...,:num])
#     return line,

# fig1 = plt.figure()

# data = np.random.rand(2, 25)
# l, = plt.plot([], [], 'r-')
# plt.xlim(0, 1)
# plt.ylim(0, 1)
# plt.xlabel('x')
# plt.title('test')
# line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l),
#     interval=50, blit=True)
# #line_ani.save('lines.mp4')

# plt.show()

# import matplotlib.pyplot as plot
# import numpy
# from numpy.polynomial.polynomial import polyfit,polyadd,Polynomial

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    print("Setting up mixed_signal_controller...")
    dev = ModularDevice()
    sample_count = 1000

    print("Example analog input:")
    ain_values = dev.get_analog_inputs()
    print(str(ain_values))

    print("Collecting {0} analog input samples...".format(sample_count))
    start_time = time.time()
    for sample_n in range(sample_count):
        ain_values = dev.get_analog_inputs()
    stop_time = time.time()
    print("samples/s = {0}".format(sample_count/(stop_time-start_time)))
