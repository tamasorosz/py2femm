import math
import os

from numpy import NaN

import calc_torque_avg_rip
import taguchi_def

if __name__ == '__main__':
    for J0 in [15]:
        avg = []
        rip = []
        for i in range(len(taguchi_def.df)):
            try:
                X1 = taguchi_def.df.iloc[i, 0]
                X2 = taguchi_def.df.iloc[i, 1]
                X3 = taguchi_def.df.iloc[i, 2]
                X4 = taguchi_def.df.iloc[i, 3]
                X5 = taguchi_def.df.iloc[i, 4]
                X6 = taguchi_def.df.iloc[i, 5]

                res = calc_torque_avg_rip.torque_avg_rip(J0, X1, X2, X3, X4, X5, X6)

                avg.append(res[0])
                rip.append(res[1])

            except ValueError:
                avg.append(0)
                rip.append(0)

        SNavg = [0 if i == 0 else -10 * math.log10(1 / (i ** 2)) for i in avg]
        SNrip = [0 if i == 0 else -10 * math.log10(i ** 2) for i in rip]

        df = taguchi_def.df
        df['Tavg'] = avg
        df['SNavg'] = SNavg
        df['Trip'] = rip
        df['SNrip'] = SNrip

        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)
        file_path = os.path.join(folder_path, f'results/taguchi_{J0}A.csv')
        df.to_csv(file_path, encoding='utf-8', index=False)
