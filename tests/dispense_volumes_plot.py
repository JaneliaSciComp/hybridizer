# -*- coding: utf-8 -*-
from __future__ import print_function, division
import matplotlib.pyplot as plot
import numpy
from numpy.polynomial.polynomial import polyfit,polyadd,Polynomial

INCHES_PER_ML = 0.078
VOLTS_PER_ADC_UNIT = 0.0049

def load_numpy_data(path):
    with open(path,'r') as fid:
        header = fid.readline().rstrip().split(',')

    dt = numpy.dtype({'names':header,'formats':['S25']*len(header)})
    numpy_data = numpy.loadtxt(path,dtype=dt,delimiter=",",skiprows=1)
    return numpy_data

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    # Load data
    data_file = 'dispense_data.csv'
    dispense_data = load_numpy_data(data_file)
    cylinders = list(dispense_data.dtype.names)
    cylinders.remove('dispense_goal')
    cylinders.remove('initial_weight')
    print(cylinders)
    cylinder_count = len(cylinders)
    print(cylinder_count)
    dispense_goals = numpy.int16(dispense_data['dispense_goal'])
    dispense_goal_set = list(set(dispense_goals))
    dispense_goal_set.sort(reverse=True)
    print(dispense_goal_set)
    goal_count = len(dispense_goal_set)
    print(goal_count)

    index = numpy.arange(goal_count)
    index = index*cylinder_count
    bar_width = 0.35

    fig, ax = plot.subplots()

    opacity = 0.6
    error_config = {'ecolor': '0.3'}
    colors = ['b','g','r','c','m','y','k','b']

    for cylinder_n in range(cylinder_count):
        cylinder_means = []
        cylinder_stds = []
        for dispense_goal in dispense_goal_set:
            goal_data = dispense_data[dispense_goals==dispense_goal]
            cylinder_data = numpy.float64(goal_data[cylinders[cylinder_n]])
            cylinder_mean = numpy.mean(cylinder_data)
            cylinder_means.append(cylinder_mean)
            cylinder_std = numpy.std(cylinder_data)
            cylinder_stds.append(cylinder_std)
        print(cylinder_n)
        print(cylinder_means)
        print(cylinder_stds)
        print('')
        plot.bar(index+bar_width*(cylinder_n),
                 cylinder_means,
                 bar_width,
                 alpha=opacity,
                 color=colors[cylinder_n],
                 yerr=cylinder_stds,
                 error_kw=error_config,
                 label=cylinders[cylinder_n])

plot.xlabel('Dispense Volume Goal (ml)')
plot.ylabel('Dispense Volume Measured (ml)')
plot.title('ELF Dispense Tests')
plot.xticks(index+(bar_width*cylinder_count/2),dispense_goal_set)
plot.legend()
plot.grid(True)
plot.ylim((0,11))
plot.yticks(numpy.arange(0,11,1.0))

plot.tight_layout()
plot.show()
