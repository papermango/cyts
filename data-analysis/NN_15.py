import torch
import numpy as np
import pandas as pd
from torch import nn

data = pd.read_csv("CSVs/output_250_15_3.csv", index_col=0)

# extract input and response variables
inputs = np.asarray(data[["start", "prod1", "prod2"]])
response = np.asarray(data["halt"])

X = torch.from_numpy(inputs)
y = torch.from_numpy(response)
y_bc = y >= 0 # binary classification version

device = "cpu"

class NN_Classify(nn.Module):
   def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
