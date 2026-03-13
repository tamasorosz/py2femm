import pandas as pd

# Specify the path to your CSV file
csv_file_path_0 = "all_res_avg_case6_20241227.csv"
csv_file_path_1 = "all_res_cog_case6_20241227.csv"

# Open the file using open() and read it with pandas
with open(csv_file_path_0, 'r') as file:
    df_avg = pd.read_csv(file)
with open(csv_file_path_1, 'r') as file:
    df_cog = pd.read_csv(file)

df_avg['COG'] = df_cog['COG']
df_avg['ANG'] = df_avg['ANG'] * -1
df_avg['AVG'] = df_avg['AVG'] * -1

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # No fixed width; adjust to content

print(df:=df_avg[df_avg.iloc[:, -2] < 15])
print(len(df))

# output_file = "refined_data_for_ml.csv"
# df_avg.to_csv(output_file, index=False)
#
# print(f"Data saved to {output_file}")