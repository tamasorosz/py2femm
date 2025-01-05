import csv
import math
import os
import re

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import calc_max_torque_angle

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
from examples.magnetics.reluctance_machine.optimisation.case_7 import calc_torque_avg_rip
from examples.magnetics.reluctance_machine.optimisation.case_7 import calc_cogging
from examples.magnetics.reluctance_machine.optimisation.case_7 import calc_max_torque_angle

#
if __name__ == "__main__":
    colors = ["#B90276", '#50237F', '#00A8B0', "#006249", '#525F6B', '#000']
    # x = calc_max_torque_angle.max_torque_angle(30, 21, 14, 1, 0.5, 3, 1, 1.5, 0, 0, 0, 0)
    # df = pd.DataFrame(x[1])
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path1 = os.path.join(folder_path, f'results/torque_sum.csv')
    file_path2 = os.path.join(folder_path, f'results/torque_rel.csv')
    file_path3 = os.path.join(folder_path, f'results/torque_sum1.csv')
    file_path4 = os.path.join(folder_path, f'results/torque_rel1.csv')
    file_path5 = os.path.join(folder_path, f'results/torque_sum2.csv')
    file_path6 = os.path.join(folder_path, f'results/torque_rel2.csv')
    file_path7 = os.path.join(folder_path, f'results/torque_sum3.csv')
    # df.to_csv(file_path7, encoding='utf-8', index=False)
    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)
    # df4 = pd.read_csv(file_path3)
    # print(df4)
    # df5 = pd.read_csv(file_path4)
    df3 = df1-df2
    df6 = pd.read_csv(file_path5)
    df7 = pd.read_csv(file_path6)
    df8 = df6 - df7
    df9 = pd.read_csv(file_path7)
    # plt.scatter(list(range(len(df1))), df1)
    # plt.scatter(list(range(len(df2))), df2)
    # plt.scatter(list(range(len(df3))), df3)
    # plt.scatter(list(range(len(df4))), df4)
    # plt.scatter(list(range(len(df5))), df5)
    # plt.plot(df6[88:453]*-1, label='SUM', color=colors[0])
    # plt.plot(df7[88:453]*-1, label='REL', color=colors[1])
    # plt.plot(df8[88:453]*-1, label='PM', color=colors[2])
    # plt.plot(df9[88:453] * -1, label='RM', color=colors[4], linestyle='--')
    plt.plot(df1[123:485] * -1, label='SUM', color=colors[0])
    plt.plot(df2[123:485] * -1, label='REL', color=colors[1])
    plt.plot(df3[123:485] * -1, label='PM', color=colors[2])
    plt.plot(df9[123:485] * -1, label='RM', color=colors[4], linestyle='--')

    plt.xlabel('Rotor position [deg]', fontsize=14)
    plt.ylabel('Torque [mNm]', fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)
    plt.legend(fontsize=14, loc='lower left')
    plt.tight_layout()
    # plt.savefig(os.getcwd() + '/figures/' + 'torquecomp_noshift.png')
    plt.savefig(os.getcwd() + '/figures/' + 'torquecomp.png')
    plt.show()

    # plt.plot([273.7056085605172, 343.96926984858277, 414.2927956145196, 483.0360976208476, 549.8906166183984, 613.2767664061369, 672.4372751199345, 726.8528950804068, 776.5217434265616, 822.0172980549409, 862.9509109470321, 898.4341099959516, 929.6265969115913, 957.412490218172, 982.250004076604, 1004.8655136657387, 1025.8546998583001, 1045.2838480243788, 1063.3752800601308, 1080.3795633113873, 1096.4327633548332, 1111.6199832554544, 1126.1639865358068, 1140.1947270947185, 1153.721081761992, 1166.7867150188683, 1179.4231186900952, 1191.6499114927713, 1203.4809089107964, 1214.9388120741685, 1226.0301986547154, 1236.755912472836, 1247.1007824206195, 1257.0577674057472, 1266.5765164874051, 1275.6079553936981, 1284.1417491100106, 1292.1705835447617, 1299.6131247852895, 1306.4157845869754, 1312.54187574912, 1317.8054159244682, 1322.0048154827912, 1324.896822718568, 1326.1614967785429, 1325.579049646882, 1322.6763572029024, 1317.483994285908, 1309.6532725340653, 1298.5846321505228, 1283.7211680519372, 1264.8393639355172, 1241.1559360840788, 1212.2885235171923, 1178.1929656126804, 1139.7192219387016, 1097.6655722384608, 1052.8728113453667, 1006.0030503600487, 957.3666321103568, 905.4360435892183, 851.1578800620244, 794.75968505968, 736.7098059613244, 678.940105698566, 622.7055154533072, 568.975754947754, 518.0783229991281, 469.9911437347068, 425.7616613438176, 385.1733474528932, 346.9408585189332, 310.8201779054801, 276.46505443862026, 243.5626009445239, 211.9924571622374, 181.18690462760176, 151.22487113622688, 122.23093084519995, 94.04403147866803, 66.51523673304824, 39.50659156558559, 12.849506613930869, -13.510859874278056, -39.61949698640379, -65.47831828123999, -91.14967528162316, -116.73150214270079, -142.1262371067786, -167.52894540115886, -192.9553974825761])
    # plt.show()

    # xl = np.array([15, 9, 1, 1, 1, 10]),
    # xu = np.array([25, 14, 4, 4, 2, 15]),

    # y = calc_torque_avg_rip.torque_avg_rip(30, 21, 14, 1, 0.5, 3, 1, 1.5, 10, 11, 16, 14)
    # z = calc_cogging.cogging(0, 21, 14, 1, 0.5, 3, 1, 1.5, 10, 11, 16, 14)
    # y = calc_torque_avg_rip.torque_avg_rip(30, 21, 14, 1, 0.5, 3, 1, 1.5, 9.85, 10.85, 15.85, 13.85)
    # z = calc_cogging.cogging(0, 21, 14, 1, 0.5, 3, 1, 1.5, 9.85, 10.85, 15.85, 13.85)

    # print(y)
    # print(z)
    # x = [25, 15, 4, 4, 1, 15]
    # g = (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5)) + x[2] + x[3]) - 8
    # if g > 0:
    #     temp_x3 = int(8 - (math.tan(math.radians(x[0] / 2)) * (22 - (x[4] * 0.5 + 1.5))) - x[2])
    #     if temp_x3 < 1:
    #         x[3] = 1
    #         x[2] = x[2] - (1 - temp_x3)
    #         if x[2] < 1:
    #             x[2] = 1
    #     else:
    #         x[3] = temp_x3
    # print(x)
    # y = calc_max_torque_angle.max_torque_angle(30, x[0], x[1], x[2], 0.5, x[3], x[4], x[5], 1.5)
