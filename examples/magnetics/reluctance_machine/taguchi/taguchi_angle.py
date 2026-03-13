import os

import calc_max_torque_angle
import taguchi_def

if __name__ == '__main__':
    for J0 in [30]:
        ang = []
        rip = []
        for i in range(len(taguchi_def.df)):
            try:
                X1 = taguchi_def.df.iloc[i, 0]
                X2 = taguchi_def.df.iloc[i, 1]
                X3 = taguchi_def.df.iloc[i, 2]
                X4 = taguchi_def.df.iloc[i, 3]
                X5 = taguchi_def.df.iloc[i, 4]
                X6 = taguchi_def.df.iloc[i, 5]

                res = calc_max_torque_angle.max_torque_angle(J0, X1, X2, X3, X4, X5, X6)

                ang.append(res)

            except ValueError:
                ang.append(0)

        df = taguchi_def.df
        df['MaxAng'] = ang

        current_file_path = os.path.abspath(__file__)
        folder_path = os.path.dirname(current_file_path)
        file_path = os.path.join(folder_path, f'results/taguchi_{J0}A_MaxAng.csv')
        df.to_csv(file_path, encoding='utf-8', index=False)
