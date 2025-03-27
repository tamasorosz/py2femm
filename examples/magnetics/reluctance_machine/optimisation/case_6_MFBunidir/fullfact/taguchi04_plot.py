import os

import pandas as pd
import matplotlib.pyplot as plt

colors = ["#B90276", '#50237F', '#00A8B0', "#006249", '#525F6B', '#000']
# ----------------------------------------------------------------
#  Plot sensitivity for all

df = pd.read_csv(os.getcwd() + '/' + 'fullfact_res_all.csv')

plt.bar(df.keys(), df.iloc[0], label='AVG', color=colors[1])
plt.bar(df.keys(), df.iloc[1], label='RIP', color=colors[2])
plt.bar(df.keys(), df.iloc[2], label='COG', color=colors[3])

plt.xlabel('Parameters', fontsize=14)
plt.ylabel('SSB [u.]', fontsize=14)
plt.xticks(ticks=range(len(df.keys())), labels=["X8", "X9", "X10", "X11"], fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig(os.getcwd() + '/' + 'fullfact_res_all_c7.png')
plt.show()

# ----------------------------------------------------------------
# Plot sensitivity for all AVG

plt.bar(df.keys(), df.iloc[0], label='AVG', color=colors[1])

plt.xlabel('Parameters', fontsize=14)
plt.ylabel('SSB [u.]', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig(os.getcwd() + '/' + 'fullfact_res_avg_c7.png')
plt.show()

# ----------------------------------------------------------------
# Plot sensitivity for all RIP

plt.bar(df.keys(), df.iloc[1], label='RIP', color=colors[2])

plt.xlabel('Parameters', fontsize=14)
plt.ylabel('SSB [u.]', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig(os.getcwd() + '/' + 'fullfact_res_rip_c7.png')
plt.show()

# ----------------------------------------------------------------
# Plot sensitivity for all COG

plt.bar(df.keys(), df.iloc[2], label='COG', color=colors[3])

plt.xlabel('Parameters', fontsize=14)
plt.ylabel('SSB [u.]', fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig(os.getcwd() + '/' + 'fullfact_res_cog_c7.png')
plt.show()

