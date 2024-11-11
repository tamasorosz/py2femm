import math
import os

import numpy as np

import calc_torque_avg_rip, calc_cogging
import taguchi01_def

if __name__ == '__main__':
    for J0 in [30]:
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
            X10 = taguchi01_def.df1.iloc[i, 9]
            X11 = taguchi01_def.df1.iloc[i, 10]

            res = calc_torque_avg_rip.torque_avg_rip(J0, X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, X11)

            avg.append(-1*res[0])
            rip.append(res[1])

            res = calc_cogging.cogging(0, X1, X2, X3, X4, X5, X6, X7, X8, X9,  X10, X11)

            cog.append(res)

        Norm_avg = [(i - min(avg)) / (max(avg) - min(avg)) for i in avg]
        Norm_rip = [(i - min(rip)) / (max(rip) - min(rip)) for i in rip]
        Norm_cog = [(i - min(cog)) / (max(cog) - min(cog)) for i in cog]

        Mean_avg = np.mean(Norm_avg)
        Mean_rip = np.mean(Norm_rip)
        Mean_cog = np.mean(Norm_cog)

        SSW_avg = [(i - Mean_avg) ** 2 for i in Norm_avg]
        SSW_rip = [(i - Mean_rip) ** 2 for i in Norm_rip]
        SSW_cog = [(i - Mean_cog) ** 2 for i in Norm_cog]

        # print(avg)
        # print(Norm_avg)
        # print(SSW_avg)
        # print()
        # print(rip)
        # print(Norm_rip)
        # print(SSW_rip)
        # print()
        # print(cog)
        # print(Norm_cog)
        # print(SSW_cog)

        df = taguchi01_def.df1
        df['Tavg'] = avg
        df['Trip'] = rip
        df['Tcog'] = cog
        df['ANavg'] = SSW_avg
        df['ANrip'] = SSW_rip
        df['ANcog'] = SSW_cog

        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)
        file_path = os.path.join(folder_path, f'results/taguchi_res_all.csv')
        df.to_csv(file_path, encoding='utf-8', index=False)
