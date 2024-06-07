import math
import os

import calc_torque_avg_rip
import taguchi_def
from examples.magnetics.reluctance_machine.shifting.case_3n import calc_cogging

if __name__ == '__main__':

    avg = []
    rip = []
    cog = []
    thd = []

    for i in range(len(taguchi_def.df)):
        try:
            X1 = taguchi_def.df.iloc[i, 0]
            X2 = taguchi_def.df.iloc[i, 1]
            X3 = taguchi_def.df.iloc[i, 2]
            X4 = taguchi_def.df.iloc[i, 3]

            f = calc_torque_avg_rip.torque_avg_rip(30, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, X1, X2, X3, X4)
            g = calc_cogging.cogging(0, 22.1, 146.5, 1.0, 1.0, 3.0, 0.5, 1.5, X1, X2, X3, X4)

            avg.append(f[0])
            rip.append(f[1])
            cog.append(g[0])
            thd.append(g[1])

        except ValueError:
            print('Not feasible!')
            avg.append(0)
            rip.append(0)
            cog.append(0)
            thd.append(0)

    SNavg = [0 if i == 0 else -10 * math.log10(1 / (i ** 2)) for i in avg]
    SNrip = [0 if i == 0 else -10 * math.log10(i ** 2) for i in rip]
    SNcog = [0 if i == 0 else -10 * math.log10(i ** 2) for i in cog]
    SNthd = [0 if i == 0 else -10 * math.log10(i ** 2) for i in thd]

    df = taguchi_def.df
    df['Tavg'] = avg
    df['SNavg'] = SNavg
    df['Trip'] = rip
    df['SNrip'] = SNrip
    df['Tcog'] = cog
    df['SNcog'] = SNcog
    df['Tthd'] = thd
    df['SNthd'] = SNthd

    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/taguchi_res_os.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)