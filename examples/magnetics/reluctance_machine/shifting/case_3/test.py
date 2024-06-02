import csv
import math
import os
import re

import pandas as pd
from matplotlib import pyplot as plt

import machine_model_synrm
import calc_max_torque_angle
import calc_cogging
import calc_torque_avg_rip

# if __name__ == "__main__":
#     x = calc_cogging.cogging(0, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, 7.5, 7.5, 7.5, 7.5)
#
#     print(x[0], x[1])
#     plt.plot(x[2])
#     plt.show()
#     plt.bar([str(i) for i in range(len(x[3]))], x[3])
#     plt.show()

if __name__ == "__main__":
    x = calc_max_torque_angle.max_torque_angle(30, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, 10, 10, 10, 10)

    print(x[0])
    plt.plot(x[1])
    plt.show()
#
# if __name__ == "__main__":
#     x = calc_torque_avg_rip.torque_avg_rip(30, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, 7.5, 0, 7.5, 7.5)
#
#     print(x[0], x[1])
#     plt.plot(x[2])
#     plt.show()



# variables = machine_model_synrm.VariableParameters(fold='ang',
#                                                    out='ang',
#                                                    counter=0,
#                                                    JAp=10,
#                                                    JAn=-10,
#                                                    JBp=-5,
#                                                    JBn=5,
#                                                    JCp=-5,
#                                                    JCn=5,
#
#                                                    ang_co=24.3,
#                                                    deg_co=91.5,
#                                                    bd=1.0,
#                                                    bw=0.5,
#                                                    bh=2.4,
#                                                    bg=1.5,
#
#                                                    ia=0,
#                                                    ang_m=20,
#                                                    mh=1.5
#                                                    )
#
# from examples.magnetics.reluctance_machine.optimisation.case_2 import calc_torque_avg_rip
# #
# if __name__ == "__main__":
#     # x = calc_max_torque_angle.max_torque_angle(30, 25.0, 147.1, 1.1, 1.0, 2.5, 0.5, 5.1, 1.5)
#     # x = calc_torque_avg_rip.torque_avg_rip(0, 25.0, 147.1, 1.1, 1.0, 2.5, 0.5, 5.1, 1.5)
#
#     # x = calc_max_torque_angle.max_torque_angle(30, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 14.9, 1.5)
#     x = calc_torque_avg_rip.torque_avg_rip(0, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 14.9, 1.5)
#
#
#     df = pd.DataFrame({'Torque': x[2], 'MaxAngle': list(range(0, 121))})
#     current_file_path = os.path.abspath(__file__)
#     folder_path = os.path.dirname(current_file_path)
#     file_path = os.path.join(folder_path, f'results/pmasynrm_span15_cogging.csv')
#     df.to_csv(file_path, encoding='utf-8', index=False)
#     print(x[0])
#     print(x[1])
#     plt.plot(x[2])
#     plt.show()

import numpy as np


# import matplotlib.pyplot as plt
# import numpy as np
# import warnings
#
#
# def fftPlot(sig, dt=None, plot=True):
#     # Here it's assumes analytic signal (real signal...) - so only half of the axis is required
#
#     if dt is None:
#         dt = 1
#         t = np.arange(0, sig.shape[-1])
#         xLabel = 'samples'
#     else:
#         t = np.arange(0, sig.shape[-1]) * dt
#         xLabel = 'freq [Hz]'
#
#     if sig.shape[0] % 2 != 0:
#         warnings.warn("signal preferred to be even in size, autoFixing it...")
#         t = t[0:-1]
#         sig = sig[0:-1]
#
#     sigFFT = np.fft.fft(sig) / t.shape[0]  # Divided by size t for coherent magnitude
#
#     freq = np.fft.fftfreq(t.shape[0], d=dt)
#
#     # Plot analytic signal - right half of frequence axis needed only...
#     firstNegInd = np.argmax(freq < 0)
#     freqAxisPos = freq[0:firstNegInd]
#     sigFFTPos = 2 * sigFFT[0:firstNegInd]  # *2 because of magnitude of analytic signal
#
#     if plot:
#         plt.figure()
#         plt.plot(freqAxisPos, np.abs(sigFFTPos))
#         plt.xlabel(xLabel)
#         plt.ylabel('mag')
#         plt.title('Analytic FFT plot')
#         plt.show()
#
#     return sigFFTPos, freqAxisPos
#
#
# if __name__ == "__main__":
#     lista = []
#     with open("D:\Respositories\py2femm\examples\magnetics/reluctance_machine\optimisation\case_2/results\optimised\pmasynrm_span5_cogging.csv") as f:
#         reader = csv.reader(f, delimiter=",")
#         for i in reader:
#             lista.append(i[0])
#     del lista[0]
#     lista = list(map(float, lista))
#     lista = np.array(lista)
#
#     sine = np.array([10 * math.sin(i) for i in np.linspace(0, 4 * math.pi, 121)])
#     # fftPlot(lista, 1/1000)
#     # fftPlot(np.array([10*math.sin(i) for i in np.linspace(0, 4*math.pi, 121)]), 1/1000)
#     #
#     plt.plot(lista)
#     plt.plot(np.array([10*math.sin(i) for i in np.linspace(0, 4*math.pi, 121)]))
#     plt.show()
#
#     # print(np.abs(fftPlot(lista, 1/50, plot=True)[0]))
#     # print(fftPlot(lista, 1/50, plot=False)[1])
#
#     def thd(abs_data):
#         sq_sum = 0.0
#         for r in range(len(abs_data)):
#             sq_sum = sq_sum + (abs_data[r]) ** 2
#
#         sq_harmonics = sq_sum - ((abs_data[1])) ** 2.0
#         thd = 100 * sq_harmonics ** 0.5 / abs_data[1]
#
#         return thd
#     x = np.round(np.abs(fftPlot(lista, 1/(3*120), plot=True)[1]), 3)
#
#     y = np.round(np.abs(fftPlot(lista, 1 / (3 * 120), plot=True)[0]), 3)
#
#     y[0] = 0
#     print(list(x))
#     print(list(y))
#
#     fund = next(i for i, v in enumerate(y) if v > 1)
#     refined_y = [i for i, j in zip(y, range(len(y))) if j % fund == 0]
#
#     print(fund)
#
#     print(refined_y)
#
#     # Specify the full filename path
#     filename = r'D:\Respositories\py2femm\examples\magnetics\reluctance_machine\shifting\case_3\results\thd/FFT_span5.csv'
#
#     # Ensure the directory exists
#     os.makedirs(os.path.dirname(filename), exist_ok=True)
#
#     # Open the file in write mode
#     with open(filename, mode='w', newline='') as file:
#         writer = csv.writer(file)
#
#         # Write each element of refined_y to a new row in the CSV
#         for item in refined_y:
#             writer.writerow([item])
#
#     print(thd(refined_y))
# def thd(abs_data):
#     sq_sum = 0.0
#     for r in range(len(abs_data)):
#         sq_sum = sq_sum + (abs_data[r]) ** 2
#
#     sq_harmonics = sq_sum - ((abs_data[1])) ** 2.0
#     thd = 100 * sq_harmonics ** 0.5 / abs_data[1]
#
#     return thd
# y = [0, 0.1, 0, 0, 0, 0, 0, 0, 0]
# try:
#     fund = next((i for i, v in enumerate(y) if v > 1), None)
#     if fund is None:
#         raise StopIteration
#     refined_y = [i for i, j in zip(y, range(len(y))) if j % fund == 0]
#     res_thd = thd(refined_y)
# except StopIteration:
#     try:
#         fund = next((i for i, v in enumerate(y) if v > 0.5), None)
#         if fund is None:
#             raise StopIteration
#         refined_y = [i for i, j in zip(y, range(len(y))) if j % fund == 0]
#         res_thd = thd(refined_y)
#         print('First safety case')
#     except StopIteration:
#         try:
#             fund = next((i for i, v in enumerate(y) if v > 0.25), None)
#             if fund is None:
#                 raise StopIteration
#             refined_y = [i for i, j in zip(y, range(len(y))) if j % fund == 0]
#             res_thd = thd(refined_y)
#             print('Second safety case')
#         except StopIteration:
#             try:
#                 fund = next((i for i, v in enumerate(y) if v > 0.1), None)
#                 if fund is None:
#                     raise StopIteration
#                 refined_y = [i for i, j in zip(y, range(len(y))) if j % fund == 0]
#                 res_thd = thd(refined_y)
#                 print('Third safety case')
#             except StopIteration:
#                 res_thd = 100
#                 print('Fourth safety case')