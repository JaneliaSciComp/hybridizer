# -*- coding: utf-8 -*-
from __future__ import print_function, division
import matplotlib.pyplot as plot
import numpy
from numpy.polynomial.polynomial import polyfit,polyadd,Polynomial
import argparse
import copy
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
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file_path",help="Path to csv data file.")
    # parser.add_argument("plot_title",help="Plot title.")
    args = parser.parse_args()
    data_file_path = args.data_file_path
    # plot_title = args.plot_title
    print("Data File Path: {0}".format(data_file_path))
    # print("Plot title: {0}".format(plot_title))

    # Load data
    calibration_data = load_numpy_data(data_file_path)
    header = list(calibration_data.dtype.names)
    cylinders = copy.copy(header)
    cylinders.remove('fill_duration')
    cylinders.remove('initial_weight')
    cylinders = [column for column in cylinders if 'adc' not in column]
    print(cylinders)

    # Create figure
    fig = plot.figure()
    fig.suptitle('calibration data',fontsize=14,fontweight='bold')
    fig.subplots_adjust(top=0.85)
    colors = ['b','g','r','c','m','y','k','b']
    markers = ['o','o','o','o','o','o','o','^']

    output_data = {}
    # Axis 1
    ax1 = fig.add_subplot(131)
    index = 0
    for cylinder in cylinders:
        color = colors[index]
        marker = markers[index]
        ax1.plot(calibration_data['fill_duration'],
                 calibration_data[cylinder],
                 marker=marker,
                 linestyle='--',
                 color=color,
                 label=cylinder)
        index += 1
    ax1.set_xlabel('fill duration (ms)')
    ax1.set_ylabel('volume (ml)')
    ax1.legend(loc='best')
    plot.yticks(range(0,11,1))

    ax1.grid(True)

    order = 3

    # Axis 2
    ax2 = fig.add_subplot(132)
    index = 0
    for cylinder in cylinders:
        color = colors[index]
        marker = markers[index]
        volumes_all = numpy.float64(calibration_data[cylinder])
        volumes = volumes_all[volumes_all<=6]
        adc_values = numpy.float64(calibration_data[cylinder+'_adc_low'])
        adc_values = adc_values[volumes_all<=6]
        ax2.plot(volumes,
                 adc_values,
                 marker=marker,
                 linestyle='--',
                 color=color,
                 label=cylinder)
        coefficients = polyfit(volumes,
                               adc_values,
                               order)
        poly_fit = Polynomial(coefficients)
        adc_values_fit = poly_fit(volumes)
        ax2.plot(volumes,
                 adc_values_fit,
                 marker=None,
                 linestyle='-',
                 color=color,
                 label=cylinder)
        coefficients_list = [float(coefficient) for coefficient in coefficients]
        output_data[cylinder] = {'low':coefficients_list}
        print(coefficients)
        index += 1
    ax2.set_xlabel('volume (ml)')
    ax2.set_ylabel('adc low value (adc units)')
    ax2.legend(loc='best')

    ax2.grid(True)

    # Axis 3
    ax3 = fig.add_subplot(133)
    index = 0
    for cylinder in cylinders:
        color = colors[index]
        marker = markers[index]
        volumes_all = numpy.float64(calibration_data[cylinder])
        volumes = volumes_all[volumes_all>=6]
        adc_values = numpy.float64(calibration_data[cylinder+'_adc_high'])
        adc_values = adc_values[volumes_all>=6]
        ax3.plot(volumes,
                 adc_values,
                 marker=marker,
                 linestyle='--',
                 color=color,
                 label=cylinder)
        coefficients = polyfit(volumes,
                               adc_values,
                               order)
        poly_fit = Polynomial(coefficients)
        adc_values_fit = poly_fit(volumes)
        ax3.plot(volumes,
                 adc_values_fit,
                 marker=None,
                 linestyle='-',
                 color=color,
                 label=cylinder)
        coefficients_list = [float(coefficient) for coefficient in coefficients]
        output_data[cylinder]['high'] = coefficients_list
        print(coefficients)
        index += 1
    ax3.set_xlabel('volume (ml)')
    ax3.set_ylabel('adc high value (adc units)')
    ax3.legend(loc='best')

    ax3.grid(True)

    print(output_data)
    with open('calibration.yaml', 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False)

    plot.show()
#     header = list(calibration_data.dtype.names)
#     header.remove('dispense_goal')
#     header.remove('initial_weight')
#     cylinders = [cylinder for cylinder in cylinders if 'jumps' not in cylinder and 'adc' not in cylinder]
#     print(cylinders)
#     cylinder_count = len(cylinders)
#     print(cylinder_count)
#     dispense_goals = numpy.int16(calibration_data['dispense_goal'])
#     dispense_goal_set = list(set(dispense_goals))
#     dispense_goal_set.sort(reverse=True)
#     print(dispense_goal_set)
#     goal_count = len(dispense_goal_set)
#     print(goal_count)

#     index = numpy.arange(goal_count)
#     index = index*cylinder_count
#     bar_width = 0.35

#     fig, ax = plot.subplots()

#     opacity = 0.6
#     error_config = {'ecolor': '0.3'}
#     colors = ['b','g','r','c','m','y','k','b']

#     for cylinder_n in range(cylinder_count):
#         cylinder_means = []
#         cylinder_stds = []
#         for dispense_goal in dispense_goal_set:
#             goal_data = calibration_data[dispense_goals==dispense_goal]
#             cylinder_data = numpy.float64(goal_data[cylinders[cylinder_n]])
#             cylinder_mean = numpy.mean(cylinder_data)
#             cylinder_means.append(cylinder_mean)
#             cylinder_std = numpy.std(cylinder_data)
#             cylinder_stds.append(cylinder_std)
#         print(cylinder_n)
#         print(cylinder_means)
#         print(cylinder_stds)
#         print('')
#         plot.bar(index+bar_width*(cylinder_n),
#                  cylinder_means,
#                  bar_width,
#                  alpha=opacity,
#                  color=colors[cylinder_n],
#                  yerr=cylinder_stds,
#                  error_kw=error_config,
#                  label=cylinders[cylinder_n])

# plot.xlabel('Dispense Volume Goal (ml)')
# plot.ylabel('Dispense Volume Measured (ml)')
# plot.title('ELF Dispense Test: ' + plot_title)
# plot.xticks(index+(bar_width*cylinder_count/2),dispense_goal_set)
# plot.legend()
# plot.grid(True)
# plot.ylim((0,11))
# plot.yticks(numpy.arange(0,11,1.0))

# plot.tight_layout()
