import pandas as pd

csv_file_path = "refined_data_for_ml.csv"

# Open the file using open() and read it with pandas
with open(csv_file_path, 'r') as file:
    df = pd.read_csv(file)

print(df.head())

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the data
csv_file_path = "refined_data_for_ml.csv"
df = pd.read_csv(csv_file_path)

# Prepare the data
X = df.iloc[:, :11].values
y = df.iloc[:, 11:].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Convert to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train_scaled)
y_train_tensor = torch.FloatTensor(y_train)
X_test_tensor = torch.FloatTensor(X_test_scaled)
y_test_tensor = torch.FloatTensor(y_test)


# Define the neural network
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(11, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 3)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x


# Initialize the network and optimizer
model = Net()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the model
num_epochs = 1000
batch_size = 32

for epoch in range(num_epochs):
    for i in range(0, len(X_train_tensor), batch_size):
        batch_X = X_train_tensor[i:i + batch_size]
        batch_y = y_train_tensor[i:i + batch_size]

        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# Evaluate the model
model.eval()
with torch.no_grad():
    y_pred = model(X_test_tensor)
    mse = nn.MSELoss()(y_pred, y_test_tensor)
    r2 = 1 - mse / torch.var(y_test_tensor)
    print(f'Mean Squared Error: {mse.item():.4f}')
    print(f'R-squared Score: {r2.item():.4f}')

# Predict for the new input
new_input = np.array([[20, 150, 3, 0.5, 1, 2.0, 1.5, 10, 10, 15, 15]])
new_input_scaled = scaler.transform(new_input)
new_input_tensor = torch.FloatTensor(new_input_scaled)

model.eval()
with torch.no_grad():
    predicted_output = model(new_input_tensor)

print("Input:")
print(new_input)
print("\nPredicted Output (AVG, RIP, COG):")
print(predicted_output.numpy()[0])