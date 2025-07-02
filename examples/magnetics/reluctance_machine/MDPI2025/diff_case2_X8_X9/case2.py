import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from sklearn.preprocessing import MinMaxScaler

with open('D:\Respositories\py2femm\examples\magnetics/reluctance_machine\MDPI2025/refined\case2_all.csv', 'r') as f:
    df2 = pd.read_csv(f)

# Broadcasted difference: shape (len(df1), len(df2))
diff = (df2['X9'] - df2['X8']) / 2
diff = np.round(diff,3)

# Optionally, make it a DataFrame with matching indices
diff_df = pd.DataFrame({'diff': diff})

print(diff_df)

diff_df.to_parquet("diff_X9X8.parquet", index=False)