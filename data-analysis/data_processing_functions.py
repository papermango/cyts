import numpy as np
import pandas as pd
import torch

def train_test_split(data, responses, frac=0.8, shuffle=True, rs=0):
    if isinstance(responses, list) == False:
        raise Exception("responses must be a list of column names")

    df = data.sample(frac=1, random_state=rs) if shuffle else data

    split_point = int(frac*len(df.index))
    train = df[:split_point]
    test = df[split_point:]

    # extract response columns
    train_X = train[train.columns[~train.columns.isin(responses)]]
    train_Y = train[responses]
    test_X = test[test.columns[~test.columns.isin(responses)]]
    test_Y = test[responses]

    # convert to float-valued tensors
    train_X = torch.from_numpy(np.asarray(train_X)).float()
    train_Y = torch.from_numpy(np.asarray(train_Y)).float()
    test_X  = torch.from_numpy(np.asarray(test_X )).float()
    test_Y  = torch.from_numpy(np.asarray(test_Y )).float()

    return (train_X, train_Y, test_X, test_Y)

def batch(data, batches, responses, shuffle=True, rs=0):
    if isinstance(responses, list) == False:
        raise Exception("responses must be a list of column names")

    df = data.sample(frac=1, random_state=rs) if shuffle else data
    batch_size = int(len(df.index) / batches)
    split_points = [i * batch_size for i in range(batches)]
    split_points.append(len(df.index))

    groups = [df[split_points[i]:split_points[i+1]] for i in range(batches)]
    # extract response columns
    x_sets = [g[g.columns[~g.columns.isin(responses)]] for g in groups]
    y_sets = [g[responses] for g in groups]
    # convert to float-valued tensors
    x_tensors = [torch.from_numpy(np.asarray(elem)).float() for elem in x_sets]
    y_tensors = [torch.from_numpy(np.asarray(elem)).float() for elem in y_sets]

    return (x_tensors, y_tensors)

def train_model(model, epochs, batch_size, loss_fn, optimizer, X, y):
    for epoch in range(epochs):
        for i in range(0, len(X), batch_size):
            Xbatch = X[i:i+batch_size]
            y_pred = model(Xbatch)
            ybatch = y[i:i+batch_size]
            loss = loss_fn(y_pred, ybatch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f'Finished epoch {epoch}, latest loss {loss}')

def diagnostics(model, train_X, train_Y, test_X, test_Y):
    with torch.no_grad():
        out_train = model(train_X).round()
        out_test = model(test_X).round()

    correct_train = sum(out_train == train_Y).item()
    correct_test = sum(out_test == test_Y).item()
    acc_train = (correct_train / len(train_X)) * 100
    acc_test = (correct_test / len(test_X)) * 100
    print()
    print(f"Accuracy on training dataset: {acc_train:.4f}%, {correct_train} correct labels out of {len(train_X)}")
    print(f"Accuracy on test dataset: {acc_test:.4f}%, {correct_test} correct labels out of {len(test_X)}")

    # Count types of errors
    # Null hypothesis is that it did not halt (0 aka False)
    # Type I (false positive): identified halt when no halt occurred
    # Type II (false negative): failed to identify halt when halt occurred
    false_pos_tr = sum(torch.logical_and(out_train == True, train_Y == False)).item()
    false_neg_tr = sum(torch.logical_and(out_train == False, train_Y == True)).item()
    false_pos_te = sum(torch.logical_and(out_test == True, test_Y == False)).item()
    false_neg_te = sum(torch.logical_and(out_test == False, test_Y == True)).item()
    print()
    print(f"{false_pos_tr} false positives and {false_neg_tr} false negatives on training dataset")
    print(f"{false_pos_te} false positives and {false_neg_te} false negatives on test dataset")
    print(f"Type I error (α): {(false_pos_tr / len(train_X)) * 100:.4f}% training, {(false_pos_te / len(test_X)) * 100:.4f}% test")
    print(f"Type II error (β): {(false_neg_tr / len(train_X)) * 100:.4f}% training, {(false_neg_te / len(test_X)) * 100:.4f}% test")

    return (out_train, out_test)
