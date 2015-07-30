# -*- coding: utf-8 -*-
from __future__ import print_function, division
import matplotlib.pyplot as plot
import numpy
from numpy.polynomial.polynomial import polyfit,polyadd,Polynomial
import yaml


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
    # Load VA data
    data_file = 'hall_effect_data_va.csv'
    hall_effect_data_va = load_numpy_data(data_file)
    distances_va = numpy.float64(hall_effect_data_va['distance'])
    A1_VA = numpy.float64(hall_effect_data_va['A1'])
    A9_VA = numpy.float64(hall_effect_data_va['A9'])
    A4_VA = numpy.float64(hall_effect_data_va['A4'])
    A12_VA = numpy.float64(hall_effect_data_va['A12'])
    A2_VA = numpy.float64(hall_effect_data_va['A2'])
    A10_VA = numpy.float64(hall_effect_data_va['A10'])
    A5_VA = numpy.float64(hall_effect_data_va['A5'])
    A13_VA = numpy.float64(hall_effect_data_va['A13'])

    # Massage VA data
    volumes_va = distances_va/INCHES_PER_ML
    A1_VA = numpy.reshape(A1_VA,(-1,1))
    A9_VA = numpy.reshape(A9_VA,(-1,1))
    A4_VA = numpy.reshape(A4_VA,(-1,1))
    A12_VA = numpy.reshape(A12_VA,(-1,1))
    A2_VA = numpy.reshape(A2_VA,(-1,1))
    A10_VA = numpy.reshape(A10_VA,(-1,1))
    A5_VA = numpy.reshape(A5_VA,(-1,1))
    A13_VA = numpy.reshape(A13_VA,(-1,1))

    data_va = numpy.hstack((A1_VA,A9_VA,A4_VA,A12_VA,A2_VA,A10_VA,A5_VA,A13_VA))
    data_va = data_va/VOLTS_PER_ADC_UNIT

    # Load OA data
    data_file = 'hall_effect_data_oa.csv'
    hall_effect_data_oa = load_numpy_data(data_file)
    distances_oa = numpy.float64(hall_effect_data_oa['distance'])
    A9_OA = numpy.float64(hall_effect_data_oa['A9'])
    A10_OA = numpy.float64(hall_effect_data_oa['A10'])
    A11_OA = numpy.float64(hall_effect_data_oa['A11'])
    A12_OA = numpy.float64(hall_effect_data_oa['A12'])

    # Massage OA data
    volumes_oa = distances_oa/INCHES_PER_ML
    A9_OA = numpy.reshape(A9_OA,(-1,1))
    A10_OA = numpy.reshape(A10_OA,(-1,1))
    A11_OA = numpy.reshape(A11_OA,(-1,1))
    A12_OA = numpy.reshape(A12_OA,(-1,1))

    data_oa = numpy.hstack((A9_OA,A10_OA,A11_OA,A12_OA))
    data_oa = data_oa/VOLTS_PER_ADC_UNIT

    # Create figure
    fig = plot.figure()
    fig.suptitle('hall effect sensors',fontsize=14,fontweight='bold')
    fig.subplots_adjust(top=0.85)
    colors = ['b','g','r','c','m','y','k','b']
    markers = ['o','o','o','o','o','o','o','^']

    # Axis 1
    ax1 = fig.add_subplot(121)
    for column_index in range(0,data_va.shape[1]):
        color = colors[column_index]
        marker = markers[column_index]
        ax1.plot(data_va[:,column_index],volumes_va,marker=marker,linestyle='--',color=color)
    # for column_index in range(0,data_oa.shape[1]):
    #     color = colors[column_index]
    #     marker = markers[column_index]
    #     ax1.plot(data_oa[:,column_index],volumes_oa,marker=marker,linestyle='--',color=color)
    ax1.set_xlabel('mean signals (ADC units)')
    ax1.set_ylabel('volume (ml)')

    ax1.grid(True)

    # Axis 2
    for column_index in range(0,data_va.shape[1]):
        data_va[:,column_index] -= data_va[:,column_index].min()

    MAX_VA = 120
    data_va = data_va[numpy.all(data_va<MAX_VA,axis=1)]
    length = data_va.shape[0]
    volumes_va = volumes_va[-length:]

    # for column_index in range(0,data_oa.shape[1]):
    #     data_oa[:,column_index] -= data_oa[:,column_index].max()

    ax2 = fig.add_subplot(122)
    for column_index in range(0,data_va.shape[1]):
        color = colors[column_index]
        marker = markers[column_index]
        ax2.plot(data_va[:,column_index],volumes_va,marker=marker,linestyle='--',color=color)
    # for column_index in range(0,data_oa.shape[1]):
    #     color = colors[column_index]
    #     marker = markers[column_index]
    #     ax2.plot(data_oa[:,column_index],volumes_oa,marker=marker,linestyle='--',color=color)
    ax2.set_xlabel('offset mean signals (ADC units)')
    ax2.set_ylabel('volume (ml)')

    ax2.grid(True)

    order = 3

    sum_va = None
    for column_index in range(0,data_va.shape[1]):
        coefficients_va = polyfit(data_va[:,column_index],volumes_va,order)
        if sum_va is None:
            sum_va = coefficients_va
        else:
            sum_va = polyadd(sum_va,coefficients_va)
    average_va = sum_va/data_va.shape[1]
    with open('adc_to_volume_va.yaml', 'w') as f:
        yaml.dump(average_va, f, default_flow_style=False)

    round_digits = 8
    average_va = [round(i,round_digits) for i in average_va]

    poly = Polynomial(average_va)
    ys_va = poly(data_va[:,-1])
    ax2.plot(data_va[:,-1],ys_va,'r',linewidth=3)

    ax2.text(5,7.5,r'$v = c_0 + c_1s + c_2s^2 + c_3s^3$',fontsize=20)
    ax2.text(5,6.5,str(average_va),fontsize=18,color='r')

    plot.show()
