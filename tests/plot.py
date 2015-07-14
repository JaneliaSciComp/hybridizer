# -*- coding: utf-8 -*-
from __future__ import print_function, division
import matplotlib.pyplot as plot
import numpy

inches_per_ml = 0.078
volts_per_ADC_unit = 0.0049

positions = [0.50,0.45,0.40,0.35,0.30,0.25,0.20,0.15,0.10,0.05,0.00]
volumes = [position/inches_per_ml for position in positions]
A1 = [1.90,1.78,1.68,1.60,1.54,1.48,1.43,1.40,1.37,1.34,1.32]
A1_ADC = [i/volts_per_ADC_unit for i in A1]
A4 = [1.98,1.85,1.75,1.66,1.60,1.54,1.49,1.45,1.42,1.40,1.37]
A4_ADC = [i/volts_per_ADC_unit for i in A4]

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    fig = plot.figure()
    fig.suptitle('hall effect sensors', fontsize=14, fontweight='bold')
    fig.subplots_adjust(top=0.85)

    # Axis 1
    order = 2
    round_digits = 2

    ax1 = fig.add_subplot(121)
    ax1.plot(volumes,A1_ADC,'ro',volumes,A4_ADC,'go')
    ax1.set_xlabel('volume (ml)')
    ax1.set_ylabel('mean signal (ADC units)')

    ax1.text(0.5,410,r'$s = c_0v^2 + c_1v + c_2$',fontsize=20)
    ax1.grid(True)

    coefficients_A1_ADC = numpy.polyfit(volumes,A1_ADC,order)
    coefficients_A1_ADC = [round(i,round_digits) for i in coefficients_A1_ADC]
    polynomial_A1_ADC = numpy.poly1d(coefficients_A1_ADC)
    ys_A1_ADC = polynomial_A1_ADC(volumes)
    ax1.plot(volumes,ys_A1_ADC,'r--')
    ax1.text(0.5,390,str(coefficients_A1_ADC),fontsize=18,color='r')

    coefficients_A4_ADC = numpy.polyfit(volumes,A4_ADC,order)
    coefficients_A4_ADC = [round(i,round_digits) for i in coefficients_A4_ADC]
    polynomial_A4_ADC = numpy.poly1d(coefficients_A4_ADC)
    ys_A4_ADC = polynomial_A4_ADC(volumes)
    ax1.plot(volumes,ys_A4_ADC,'g--')
    ax1.text(0.5,400,str(coefficients_A4_ADC),fontsize=18,color='g')

    # Axis 2
    order = 2
    round_digits = 5

    ax2 = fig.add_subplot(122)
    ax2.plot(A1_ADC,volumes,'ro',A4_ADC,volumes,'go')
    ax2.set_xlabel('mean signal (ADC units)')
    ax2.set_ylabel('volume (ml)')
    ax2.grid(True)

    ax2.text(270,6.5,r'$v = c_0s^2 + c_1s + c_2$',fontsize=20)

    coefficients_A1_ADC = numpy.polyfit(A1_ADC,volumes,order)
    coefficients_A1_ADC = [round(i,round_digits) for i in coefficients_A1_ADC]
    polynomial_A1_ADC = numpy.poly1d(coefficients_A1_ADC)
    ys_A1_ADC = polynomial_A1_ADC(A1_ADC)
    ax2.plot(A1_ADC,ys_A1_ADC,'r--')
    ax2.text(270,6.0,str(coefficients_A1_ADC),fontsize=18,color='r')

    coefficients_A4_ADC = numpy.polyfit(A4_ADC,volumes,order)
    coefficients_A4_ADC = [round(i,round_digits) for i in coefficients_A4_ADC]
    polynomial_A4_ADC = numpy.poly1d(coefficients_A4_ADC)
    ys_A4_ADC = polynomial_A4_ADC(A4_ADC)
    ax2.plot(A4_ADC,ys_A4_ADC,'g--')
    ax2.text(270,5.5,str(coefficients_A4_ADC),fontsize=18,color='g')

    # coefficients_array =  a = numpy.vstack((coefficients_A1_ADC,coefficients_A4_ADC))
    # coefficients_average = numpy.average(coefficients_array,0)
    # polynomial_average = numpy.poly1d(coefficients_average)
    # ys_average_A1_ADC = polynomial_average(A1_ADC)
    # ax2.plot(A1_ADC,ys_average_A1_ADC,'b')
    # ys_average_A4_ADC = polynomial_average(A4_ADC)
    # ax2.plot(A4_ADC,ys_average_A4_ADC,'b')
    # ax2.text(270,5.0,str(coefficients_average),fontsize=18,color='b')

    plot.show()
