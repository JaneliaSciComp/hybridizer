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
A3 = [1.86,1.74,1.65,1.58,1.52,1.47,1.42,1.39,1.36,1.33,1.31]
A3_ADC = [i/volts_per_ADC_unit for i in A3]
A5 = [1.98,1.85,1.74,1.67,1.60,1.55,1.50,1.47,1.43,1.40,1.38]
A5_ADC = [i/volts_per_ADC_unit for i in A5]

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    fig = plot.figure()
    fig.suptitle('hall effect sensors', fontsize=14, fontweight='bold')
    fig.subplots_adjust(top=0.85)

    # Axis 1
    order = 2
    round_digits = 2

    ax1 = fig.add_subplot(121)
    ax1.plot(volumes,A1_ADC,'ro',volumes,A4_ADC,'go',volumes,A3_ADC,'bo',volumes,A5_ADC,'co')
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

    coefficients_A3_ADC = numpy.polyfit(volumes,A3_ADC,order)
    coefficients_A3_ADC = [round(i,round_digits) for i in coefficients_A3_ADC]
    polynomial_A3_ADC = numpy.poly1d(coefficients_A3_ADC)
    ys_A3_ADC = polynomial_A3_ADC(volumes)
    ax1.plot(volumes,ys_A3_ADC,'b--')
    ax1.text(0.5,380,str(coefficients_A3_ADC),fontsize=18,color='b')

    coefficients_A5_ADC = numpy.polyfit(volumes,A5_ADC,order)
    coefficients_A5_ADC = [round(i,round_digits) for i in coefficients_A5_ADC]
    polynomial_A5_ADC = numpy.poly1d(coefficients_A5_ADC)
    ys_A5_ADC = polynomial_A5_ADC(volumes)
    ax1.plot(volumes,ys_A5_ADC,'c--')
    ax1.text(0.5,370,str(coefficients_A5_ADC),fontsize=18,color='c')

    # Axis 2
    order = 2
    round_digits = 5

    ax2 = fig.add_subplot(122)
    ax2.plot(A1_ADC,volumes,'ro',A4_ADC,volumes,'go',A3_ADC,volumes,'bo',A5_ADC,volumes,'co')
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

    coefficients_A3_ADC = numpy.polyfit(A3_ADC,volumes,order)
    coefficients_A3_ADC = [round(i,round_digits) for i in coefficients_A3_ADC]
    polynomial_A3_ADC = numpy.poly1d(coefficients_A3_ADC)
    ys_A3_ADC = polynomial_A3_ADC(A3_ADC)
    ax2.plot(A3_ADC,ys_A3_ADC,'b--')
    ax2.text(270,5.0,str(coefficients_A3_ADC),fontsize=18,color='b')

    coefficients_A5_ADC = numpy.polyfit(A5_ADC,volumes,order)
    coefficients_A5_ADC = [round(i,round_digits) for i in coefficients_A5_ADC]
    polynomial_A5_ADC = numpy.poly1d(coefficients_A5_ADC)
    ys_A5_ADC = polynomial_A5_ADC(A5_ADC)
    ax2.plot(A5_ADC,ys_A5_ADC,'b--')
    ax2.text(270,4.5,str(coefficients_A5_ADC),fontsize=18,color='b')

    plot.show()
