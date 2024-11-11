import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ----------------------------------------------------------------
#  Plot average torque and torque ripple parameter sensitivity for

df_avg = pd.read_csv(os.getcwd() + '/results/' + 'taguchi_res_avg.csv')
df_rip = pd.read_csv(os.getcwd() + '/results/' + 'taguchi_res_rip.csv')
df_cog = pd.read_csv(os.getcwd() + '/results/' + 'taguchi_res_cog.csv')

plt.bar(df_avg.keys(), df_avg.iloc[-1], label='AVG')
plt.bar(df_rip.keys(), df_rip.iloc[-1], label='RIP')
plt.bar(df_cog.keys(), df_cog.iloc[-1], label='COG')

plt.xlabel('Parameters', fontsize=14)
plt.ylabel('\u0394S/N [db]', fontsize=14)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()
# plt.savefig('figures/' + f'sens_synrm.png', bbox_inches='tight')
plt.show()

# ----------------------------------------------------------------
#  Plot average torque and torque ripple parameter sensitivity for

df_avg = pd.read_csv(os.getcwd() + '/results/' + 'taguchi_res_avg.csv')
df_rip = pd.read_csv(os.getcwd() + '/results/' + 'taguchi_res_rip.csv')
df_cog = pd.read_csv(os.getcwd() + '/results/' + 'taguchi_res_cog.csv')

plt.bar(df_avg.keys(), df_avg.iloc[-1], label='AVG')
# plt.bar(df_rip.keys(), df_rip.iloc[-1], label='RIP')
# plt.bar(df_cog.keys(), df_cog.iloc[-1], label='COG')

plt.xlabel('Parameters', fontsize=14)
plt.ylabel('\u0394S/N [db]', fontsize=14)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()
# plt.savefig('figures/' + f'sens_synrm.png', bbox_inches='tight')
plt.show()

# plt.bar(df_avg.keys()-0.2, df_avg.iloc[-1], label='AVG')
plt.bar(df_rip.keys(), df_rip.iloc[-1], label='RIP')
# plt.bar(df_cog.keys(), df_cog.iloc[-1], label='COG')

plt.xlabel('Parameters', fontsize=14)
plt.ylabel('\u0394S/N [db]', fontsize=14)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()
# plt.savefig('figures/' + f'sens_synrm.png', bbox_inches='tight')
plt.show()

# plt.bar(df_avg.keys()-0.2, df_avg.iloc[-1], label='AVG')
# plt.bar(df_rip.keys(), df_rip.iloc[-1], label='RIP')
plt.bar(df_cog.keys(), df_cog.iloc[-1], label='COG')

plt.xlabel('Parameters', fontsize=14)
plt.ylabel('\u0394S/N [db]', fontsize=14)
plt.xticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()
# plt.savefig('figures/' + f'sens_synrm.png', bbox_inches='tight')
plt.show()

