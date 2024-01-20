import torch
import numpy as np
import pandas as pd
from torch import nn, optim
from data_processing_functions import *

data = pd.read_csv("./CSVs/output_250_15_3.csv", index_col=0)

train_X, train_Y, test_X, test_Y = train_test_split(data, ["halt"])
# binary classification versions
train_Y_bc = (train_Y >= 0).float()
test_Y_bc = (test_Y >= 0).float()

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

print(f"%s epochs, batch size %s on training set of %s datapoints" % (epochs, batch_size, len(train_X)))
train_model(model_bc, epochs, batch_size, loss_fn, optimizer, train_X, train_Y_bc)

# Testing the model

# diagnostics(model_bc, train_X, train_Y_bc, test_X, test_Y_bc)

with torch.no_grad():
    out_train = model_bc(train_X).round()
    out_test = model_bc(test_X).round()
correct_train = sum(out_train == train_Y_bc).item()
correct_test = sum(out_test == test_Y_bc).item()
acc_train = (correct_train / len(train_X)) * 100
acc_test = (correct_test / len(test_X)) * 100
print()
print(f"Accuracy on training dataset: {acc_train:.4f}%, {correct_train} correct labels out of {len(train_X)}")
print(f"Accuracy on test dataset: {acc_test:.4f}%, {correct_test} correct labels out of {len(test_X)}")
# Count types of errors
# Null hypothesis is that it did not halt (0 aka False)
# Type I (false positive): identified halt when no halt occurred
# Type II (false negative): failed to identify halt when halt occurred
false_pos_tr = sum(torch.logical_and(out_train == True, train_Y_bc == False)).item()
false_neg_tr = sum(torch.logical_and(out_train == False, train_Y_bc == True)).item()
false_pos_te = sum(torch.logical_and(out_test == True, test_Y_bc == False)).item()
false_neg_te = sum(torch.logical_and(out_test == False, test_Y_bc == True)).item()
print()
print(f"{false_pos_tr} false positives and {false_neg_tr} false negatives on training dataset")
print(f"{false_pos_te} false positives and {false_neg_te} false negatives on test dataset")
print(f"Type I error (α): {(false_pos_tr / len(train_X)) * 100:.4f}% training, {(false_pos_te / len(test_X)) * 100:.4f}% test")
print(f"Type II error (β): {(false_neg_tr / len(train_X)) * 100:.4f}% training, {(false_neg_te / len(test_X)) * 100:.4f}% test")
