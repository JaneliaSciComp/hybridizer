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

    # Create figure
    fig = plot.figure()
    fig.suptitle('calibration data',fontsize=14,fontweight='bold')
    fig.subplots_adjust(top=0.85)
    colors = ['b','g','r','c','m','y','k','b']
    markers = ['o','o','o','o','o','o','o','^']

    order = 3

    output_data = {}

    fill_durations = numpy.int16(calibration_data['fill_duration'])
    fill_durations_set = list(set(fill_durations))
    fill_durations_set.sort()

    cylinders = [cylinders[0]]

    # Axis 1
    ax1 = fig.add_subplot(121)

    index = 0
    for cylinder in cylinders:
        color = colors[index]
        marker = markers[index]
        index += 1
        volume_means = []
        volume_stds = []
        for fill_duration in fill_durations_set:
            measured_data = calibration_data[fill_durations==fill_duration]
            volume_data = numpy.float64(measured_data[cylinder])
            volume_mean = numpy.mean(volume_data)
            volume_means.append(volume_mean)
            volume_std = numpy.std(volume_data)
            volume_stds.append(volume_std)
        fill_durations_array = numpy.array(fill_durations_set)
        volume_means_array = numpy.array(volume_means)
        volume_stds_array = numpy.array(volume_stds)
        volume_thresh = 9.5
        fill_durations_array = fill_durations_array[volume_means_array<volume_thresh]
        volume_means_array = volume_means_array[volume_means_array<volume_thresh]
        volume_stds_array = volume_stds_array[volume_means_array<volume_thresh]
        ax1.errorbar(volume_means_array,
                    fill_durations_array,
                    None,
                    volume_stds_array,
                    linestyle='--',
                    color=color)
        coefficients = polyfit(volume_means_array,
                               fill_durations_array,
                               order)
        coefficients_list = [float(coefficient) for coefficient in coefficients]
        output_data[cylinder] = {'volume_to_fill_duration':coefficients_list}
        poly_fit = Polynomial(coefficients)
        fill_durations_fit = poly_fit(volume_means_array)
        ax1.plot(volume_means_array,
                fill_durations_fit,
                linestyle='-',
                linewidth=2,
                color=color,
                label=cylinder)
    ax1.set_xlabel('volume (ml)')
    ax1.set_ylabel('fill duration (ms)')
    ax1.legend(loc='best')

    ax1.grid(True)

    # Axis 2
    ax2 = fig.add_subplot(122)
    index = 0
    for cylinder in cylinders:
        color = colors[index]
        marker = markers[index]
        index += 1
        volume_data = []
        adc_data = []
        for fill_duration in fill_durations_set:
            measured_data = calibration_data[fill_durations==fill_duration]
            volume_data_run = numpy.float64(measured_data[cylinder])
            volume_data.append(volume_data_run)
            adc_data_run = numpy.int16(measured_data[cylinder+'_adc_low'])
            adc_data.append(adc_data_run)
        run_count = len(volume_data[0])
        data_point_count = len(volume_data)
        coefficients_sum = None
        # for run in range(run_count):
        for run in range(1):
            volume_data_points = []
            adc_data_points = []
            for data_n in range(data_point_count):
                volume_data_point = volume_data[data_n][run]
                volume_data_points.append(volume_data_point)
                adc_data_point = adc_data[data_n][run]
                adc_data_points.append(adc_data_point)
            print(adc_data_points)
            volume_array = numpy.array(volume_data_points,dtype='float64')
            adc_array = numpy.array(adc_data_points,dtype='int')
            adc_array = adc_array[volume_array<=6]
            volume_array = volume_array[volume_array<=6]
            ax2.plot(volume_array,
                     adc_array,
                     linestyle='--',
                     linewidth=1,
                     color=color)
            coefficients = polyfit(volume_array,adc_array,order)
            if coefficients_sum is None:
                coefficients_sum = coefficients
            else:
                coefficients_sum = polyadd(coefficients_sum,coefficients)
        coefficients_average = coefficients_sum/run_count
        poly_fit = Polynomial(coefficients_average)
        adc_fit = poly_fit(volume_array)
        ax2.plot(volume_array,
                 adc_fit,
                 linestyle='-',
                 linewidth=2,
                 label=cylinder,
                 color=color)
        coefficients_list = [float(coefficient) for coefficient in coefficients_average]
        output_data[cylinder]['volume_to_adc_low'] = coefficients_list
    ax2.set_xlabel('volume (ml)')
    ax2.set_ylabel('adc low value (adc units)')
    ax2.legend(loc='best')

    ax2.grid(True)

    # Axis 3
    # ax3 = fig.add_subplot(133)
    # index = 0
    # for cylinder in cylinders:
    #     color = colors[index]
    #     marker = markers[index]
    #     index += 1
    #     volume_data = []
    #     adc_data = []
    #     for fill_duration in fill_durations_set:
    #         measured_data = calibration_data[fill_durations==fill_duration]
    #         volume_data_run = numpy.float64(measured_data[cylinder])
    #         volume_data.append(volume_data_run)
    #         adc_data_run = numpy.int16(measured_data[cylinder+'_adc_high'])
    #         adc_data.append(adc_data_run)
    #     run_count = len(volume_data[0])
    #     data_point_count = len(volume_data)
    #     coefficients_sum = None
    #     for run in range(run_count):
    #         volume_data_points = []
    #         adc_data_points = []
    #         for data_n in range(data_point_count):
    #             volume_data_point = volume_data[data_n][run]
    #             volume_data_points.append(volume_data_point)
    #             adc_data_point = adc_data[data_n][run]
    #             adc_data_points.append(adc_data_point)
    #         volume_array = numpy.array(volume_data_points,dtype='float64')
    #         adc_array = numpy.array(adc_data_points,dtype='int')
    #         adc_array = adc_array[volume_array>=6]
    #         volume_array = volume_array[volume_array>=6]
    #         ax3.plot(volume_array,
    #                  adc_array,
    #                  linestyle='--',
    #                  linewidth=1,
    #                  color=color)
    #         coefficients = polyfit(volume_array,adc_array,order)
    #         if coefficients_sum is None:
    #             coefficients_sum = coefficients
    #         else:
    #             coefficients_sum = polyadd(coefficients_sum,coefficients)
    #     coefficients_average = coefficients_sum/run_count
    #     poly_fit = Polynomial(coefficients_average)
    #     adc_fit = poly_fit(volume_array)
    #     ax3.plot(volume_array,
    #              adc_fit,
    #              linestyle='-',
    #              linewidth=2,
    #              label=cylinder,
    #              color=color)
    #     coefficients_list = [float(coefficient) for coefficient in coefficients_average]
    #     output_data[cylinder]['volume_to_adc_high'] = coefficients_list
    # ax3.set_xlabel('volume (ml)')
    # ax3.set_ylabel('adc high value (adc units)')
    # ax3.legend(loc='best')

    # ax3.grid(True)

    # print(output_data)
    with open('calibration.yaml', 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False)

    plot.show()
