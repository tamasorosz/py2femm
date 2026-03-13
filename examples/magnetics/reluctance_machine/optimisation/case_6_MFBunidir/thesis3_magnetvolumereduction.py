import os
import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":
    import os
    import pandas as pd
    import matplotlib.pyplot as plt

    # Define colors
    colors = ["#B90276", '#50237F', '#00A8B0', "#006249", '#525F6B', '#000']

    # Get paths
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)
    file_path1 = os.path.join(folder_path, 'results/torque_sum.csv')
    file_path2 = os.path.join(folder_path, 'results/torque_rel.csv')
    file_path5 = os.path.join(folder_path, 'results/torque_sum2.csv')
    file_path6 = os.path.join(folder_path, 'results/torque_rel2.csv')
    file_path7 = os.path.join(folder_path, 'results/torque_sum3.csv')

    # Load data
    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)
    df3 = df1 - df2
    df6 = pd.read_csv(file_path5)
    df7 = pd.read_csv(file_path6)
    df8 = df6 - df7
    df9 = pd.read_csv(file_path7)

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(df8[91:450] * -1, label=r'T$_{PM}$', linestyle='--', color=colors[0], linewidth=2.5)
    plt.plot(df7[91:450] * -1, label=r'T$_{REL}$', linestyle='--', color=colors[1], linewidth=2.5)
    plt.plot(df6[91:450] * -1, label=r'T$_{SUM}$', linestyle='-', color=colors[2], linewidth=3)

    # Labels and styling
    plt.xlabel('Load angle [deg]', fontsize=18)
    plt.ylabel('Torque [mNm]', fontsize=18)
    plt.xticks([91,141,191,241,291,341,391,441], ['0','50','100','150','200','250','300','350'], fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(True, linestyle=':', linewidth=0.8)
    plt.legend(fontsize=18, loc='lower left', framealpha=0.9)

    plt.tight_layout()

    plt.savefig(os.path.join(folder_path, 'thesis3_notreducted.png'), dpi=600, bbox_inches='tight')
    plt.show()

    import os
    import pandas as pd
    import matplotlib.pyplot as plt

    # ───────────────────────────────────────────────
    # Colors
    # ───────────────────────────────────────────────
    colors = ["#B90276", '#50237F', '#00A8B0', "#006249", '#525F6B', '#000']

    # ───────────────────────────────────────────────
    # Load data
    # ───────────────────────────────────────────────
    current_file_path = os.path.abspath(__file__)
    folder_path = os.path.dirname(current_file_path)

    file_path1 = os.path.join(folder_path, 'results/torque_sum.csv')
    file_path2 = os.path.join(folder_path, 'results/torque_rel.csv')
    file_path5 = os.path.join(folder_path, 'results/torque_sum2.csv')
    file_path6 = os.path.join(folder_path, 'results/torque_rel2.csv')
    file_path7 = os.path.join(folder_path, 'results/torque_sum3.csv')

    df1 = pd.read_csv(file_path1)
    df2 = pd.read_csv(file_path2)
    df3 = df1 - df2
    df6 = pd.read_csv(file_path5)
    df7 = pd.read_csv(file_path6)
    df8 = df6 - df7
    df9 = pd.read_csv(file_path7)

    # ───────────────────────────────────────────────
    # Create figure
    # ───────────────────────────────────────────────
    plt.figure(figsize=(8, 6))

    # ───────────────────────────────────────────────
    # Plot data
    # ───────────────────────────────────────────────
    plt.plot(pd.concat([df3[443:480], df3[123:443]]).values * -1,
             label=r'T$_{PM}$', linestyle='--', color=colors[0], linewidth=2.5)
    plt.plot(pd.concat([df2[443:480], df2[123:443]]).values * -1,
             label=r'T$_{REL}$', linestyle='--', color=colors[1], linewidth=2.5)
    plt.plot(pd.concat([df1[443:480], df1[123:443]]).values * -1,
             label=r'T$_{SUM}$', linestyle='-', color=colors[2], linewidth=3)

    # ───────────────────────────────────────────────
    # Formatting
    # ───────────────────────────────────────────────
    plt.xlabel('Load angle [deg]', fontsize=18)
    plt.ylabel('Torque [mNm]', fontsize=18)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.grid(True, linestyle=':', linewidth=0.8)
    plt.legend(fontsize=18, loc='lower left')
    plt.tight_layout()

    # ───────────────────────────────────────────────
    # Show or save
    # ───────────────────────────────────────────────
    plt.savefig(os.path.join(folder_path, 'thesis3_reducted'), dpi=650, bbox_inches='tight')
    plt.show()