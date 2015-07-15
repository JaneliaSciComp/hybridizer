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
    data_file = 'hall_effect_data.csv'
    hall_effect_data = load_numpy_data(data_file)
    distances = numpy.float64(hall_effect_data['distance'])
    A1 = numpy.float64(hall_effect_data['A1'])
    A9 = numpy.float64(hall_effect_data['A9'])
    A4 = numpy.float64(hall_effect_data['A4'])
    A12 = numpy.float64(hall_effect_data['A12'])
    A2 = numpy.float64(hall_effect_data['A2'])
    A10 = numpy.float64(hall_effect_data['A10'])
    A5 = numpy.float64(hall_effect_data['A5'])
    A13 = numpy.float64(hall_effect_data['A13'])

    # Massage data
    volumes = distances/INCHES_PER_ML
    A1 = numpy.reshape(A1,(-1,1))
    A9 = numpy.reshape(A9,(-1,1))
    A4 = numpy.reshape(A4,(-1,1))
    A12 = numpy.reshape(A12,(-1,1))
    A2 = numpy.reshape(A2,(-1,1))
    A10 = numpy.reshape(A10,(-1,1))
    A5 = numpy.reshape(A5,(-1,1))
    A13 = numpy.reshape(A13,(-1,1))

    data = numpy.hstack((A1,A9,A4,A12,A2,A10,A5,A13))
    data = data/VOLTS_PER_ADC_UNIT

    # Create figure
    fig = plot.figure()
    fig.suptitle('hall effect sensors', fontsize=14, fontweight='bold')
    fig.subplots_adjust(top=0.85)
    colors = ['b','g','r','c','m','y','k','b']
    markers = ['o','o','o','o','o','o','o','^']

    # Axis 1
    ax1 = fig.add_subplot(121)
    for column_index in range(0,data.shape[1]):
        color = colors[column_index]
        marker = markers[column_index]
        ax1.plot(data[:,column_index], volumes, marker=marker, linestyle='--', color=color)
    ax1.set_xlabel('mean signals (ADC units)')
    ax1.set_ylabel('volume (ml)')

    ax1.grid(True)

    # Axis 2
    for column_index in range(0,data.shape[1]):
        data[:,column_index] -= data[:,column_index].min()

    ax2 = fig.add_subplot(122)
    for column_index in range(0,data.shape[1]):
        color = colors[column_index]
        marker = markers[column_index]
        ax2.plot(data[:,column_index], volumes, marker=marker, linestyle='--', color=color)
    ax2.set_xlabel('offset mean signals (ADC units)')
    ax2.set_ylabel('volume (ml)')

    ax2.grid(True)

    MAX = 300
    data = data[numpy.all(data<MAX,axis=1)]
    length = data.shape[0]
    volumes = volumes[-length:]
    order = 3

    sum = None
    for column_index in range(0,data.shape[1]):
        coefficients = polyfit(data[:,column_index],volumes,order)
        if sum is None:
            sum = coefficients
        else:
            sum = polyadd(sum,coefficients)
    average = sum/data.shape[1]

    round_digits = 8
    average = [round(i,round_digits) for i in average]

    poly = Polynomial(average)
    ys = poly(data[:,-1])
    ax2.plot(data[:,-1],ys,'r',linewidth=3)

    ax2.text(5,7.5,r'$v = c_0 + c_1s + c_2s^2 + c_3s^3$',fontsize=20)
    ax2.text(5,6.5,str(average),fontsize=18,color='r')

    plot.show()
