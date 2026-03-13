import math
import os

import numpy as np

import calc_torque_avg_rip, calc_cogging
import taguchi01_def

if __name__ == '__main__':
    avg = []
    rip = []
    cog = []
    for i in range(len(taguchi01_def.df1)):
        X1 = taguchi01_def.df1.iloc[i, 0]
        X2 = taguchi01_def.df1.iloc[i, 1]
        X3 = taguchi01_def.df1.iloc[i, 2]
        X4 = taguchi01_def.df1.iloc[i, 3]
        X5 = taguchi01_def.df1.iloc[i, 4]
        X6 = taguchi01_def.df1.iloc[i, 5]
        X7 = taguchi01_def.df1.iloc[i, 6]
        X8 = taguchi01_def.df1.iloc[i, 7]
        X9 = taguchi01_def.df1.iloc[i, 8]

        res = calc_torque_avg_rip.torque_avg_rip(30, X1, X2, X3, X4, X5, X6, X7, X8, X9)

        avg.append(-1*res[0])
        rip.append(res[1])

        res = calc_cogging.cogging(0, X1, X2, X3, X4, X5, X6, X7, X8, X9)

        cog.append(res)

    Norm_avg = [(i - min(avg)) / (max(avg) - min(avg)) for i in avg]
    Norm_rip = [(i - min(rip)) / (max(rip) - min(rip)) for i in rip]
    Norm_cog = [(i - min(cog)) / (max(cog) - min(cog)) for i in cog]

    df = taguchi01_def.df1
    df['Tavg'] = avg
    df['Trip'] = rip
    df['Tcog'] = cog
    df['Navg'] = Norm_avg
    df['Nrip'] = Norm_rip
    df['Ncog'] = Norm_cog

    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/taguchi_res_raw.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)
