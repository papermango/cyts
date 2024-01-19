import torch
import numpy as np
import pandas as pd
from torch import nn, optim

data = pd.read_csv("./CSVs/output_250_15_3.csv", index_col=0)
data = data.sample(frac=1, random_state=0) # shuffle data

# extract input and response variables
inputs = np.asarray(data[["start", "prod1", "prod2"]])
response = np.asarray(data["halt"])

X = torch.from_numpy(inputs).float()
y = torch.from_numpy(response)
y_bc = (y >= 0).float() # binary classification version

device = "cpu"
print(f"Using device %s" % device)

# Binary classification problem
model_bc = nn.Sequential(
  nn.Linear(3, 5),
  nn.ReLU(),
  nn.Linear(5, 5),
  nn.ReLU(),
  nn.Linear(5, 1),
  nn.Sigmoid()
)
print(model_bc)

loss_fn = nn.BCELoss()  # binary cross entropy
optimizer = optim.Adam(model_bc.parameters(), lr=0.001)
batch_size = 75
epochs = 5

for epoch in range(epochs):
    for i in range(0, len(X), batch_size):
        Xbatch = X[i:i+batch_size]
        y_pred = model_bc(Xbatch)
        ybatch = y_bc[i:i+batch_size]
        loss = loss_fn(y_pred, torch.unsqueeze(ybatch, 1))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    print(f'Finished epoch {epoch}, latest loss {loss}')