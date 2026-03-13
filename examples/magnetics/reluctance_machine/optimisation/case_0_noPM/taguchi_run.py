import math
import os

import calc_torque_avg_rip
import taguchi_def

if __name__ == '__main__':
    avg = []
    rip = []
    for i in range(len(taguchi_def.df)):
        X1 = taguchi_def.df.iloc[i, 0]
        X2 = taguchi_def.df.iloc[i, 1]
        X3 = taguchi_def.df.iloc[i, 2]
        X4 = taguchi_def.df.iloc[i, 3]
        X5 = taguchi_def.df.iloc[i, 4]

        res = calc_torque_avg_rip.torque_avg_rip(30, X1, X2, X3, 0.5, X4, X5)

        avg.append(res[0])
        rip.append(res[1])

    SNavg = [0 if i == 0 else -10 * math.log10(1 / (i ** 2)) for i in avg]
    SNrip = [0 if i == 0 else -10 * math.log10(i ** 2) for i in rip]

    df = taguchi_def.df
    df['Tavg'] = avg
    df['SNavg'] = SNavg
    df['Trip'] = rip
    df['SNrip'] = SNrip

    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path = os.path.join(folder_path, f'results/taguchi_30A.csv')
    df.to_csv(file_path, encoding='utf-8', index=False)
