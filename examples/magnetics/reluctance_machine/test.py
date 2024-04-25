# import machine_model_synrm
#
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
#                                                    ang_co=16,
#                                                    deg_co=120,
#                                                    bd=1,
#                                                    bw=0.6,
#                                                    bh=2,
#                                                    bg=1.5,
#
#                                                    ia=0
#                                                    )
# machine_model_synrm.run_model(variables)
import pandas as pd

import calc_max_torque_angle as calc
import calc_torque_avg_rip as tg

# if __name__ == '__main__':
#     print(tg.torque_avg_rip(50, 10, 90, 2, 1, 2, 1))
# import csv
# import os
# import re
#
# current_file_path = os.path.abspath(__file__)
# folder_path = os.path.dirname(current_file_path)
#
# with open(os.path.join(folder_path, f'temp_ang/ang{0}.csv'), 'r') as file:
#     csvfile = [i for i in csv.reader(file)]
#     number = re.findall(r"[-+]?\d*\.\d+|\d+", csvfile[0][0])
#     torque = float(number[1])
#
# print(torque)


# Sample DataFrames
data1 = {'X1': [1, 2], 'X2': [3, 4]}
data2 = {'X1': [5, 6], 'X2': [7, 8]}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Convert each row into a list
list1 = df1.iloc[0].tolist()
list2 = df2.iloc[0].tolist()

# Concatenate the lists
combined_list = list1 + list2

# Create a new DataFrame with the combined list as a new column
df_combined = pd.DataFrame({'X3': [combined_list]})

print(df_combined)