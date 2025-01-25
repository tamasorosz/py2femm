import numpy as np
import pandas as pd
import itertools

# Specify the path to your CSV file
csv_file_path = "results/torq_res_avg.csv"

# Open the file using open() and read it with pandas
with open(csv_file_path, 'r') as file:
    df = pd.read_csv(file)

for i in range(len(df['AVG'])):
    df.loc[i, 'AVG'] = [float(j) for j in df.loc[i, 'AVG'].split(',')]

range1 = range(4, 7)
range2 = range(7, 10)
range3 = range(11, 14)
range4 = range(14, 17)


combinations = list(itertools.combinations(range(21), 4))
lst=[]
for x1, x2, x3, x4 in combinations:
    result = [(a + b + c + d + e) / 5 for a, b, c, d, e in zip(df['AVG'][x1], df['AVG'][x2], df['AVG'][5], df['AVG'][x3], df['AVG'][x4])]

    avg = np.average(result)
    rip = 100 * (np.max(result) - np.min(result)) / avg


    lst.append(rip)
print(min(lst))
# import calc_torque_avg_rip
# if __name__ == '__main__':
#     calc_torque_avg_rip.torque_avg_rip(30, 21, 15, 1, 0.5, 3, 1.0, 1.5, 12, 17, 10, 0)
