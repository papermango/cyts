import numpy as np
import pandas as pd
import subprocess
from datetime import datetime

STEPS = 50
FILEPATH = r"..\dist-newstyle\build\x86_64-windows\ghc-8.10.7\cyts-1.0.0.0\x\cyts\build\cyts\cyts.exe"

#r"C:\Coding\mathresearch\mathscripts\Haskell\cyts\dist-newstyle\build\x86_64-windows\ghc-8.10.7\cyts-1.0.0.0\x\cyts\opt\build\cyts\cyts.exe"

MAX_INT = 2**4 - 1 # ranges from - to 111. (2^4 - 1)
COLS = 3 # starting word and COLS - 1 columns
# turns out if you pick MAX_INT to be 2^(COLS + 1) - 1 you can draw the outputs as a square matrix
# which will be very nice for CNNs

TOTAL_MACHINES = MAX_INT**COLS

# each index will range from 1 to MAX_INT, so there will be (MAX_INT)^COLS datapoints
# each datapoint is one run of the machine for STEPS steps to halt

startTime = datetime.now()

# each tuple in machine_iterator is a machine, just add 1 to each element
machine_iterator = np.ndindex(tuple([MAX_INT for c in range(COLS)]))
# one row for each machine and COLS + 1 columns to accomodate program output at the end
data = np.full(shape=(TOTAL_MACHINES, COLS + 1), fill_value=-5)

for machine, index in zip(machine_iterator, range(TOTAL_MACHINES)):
  machineinput = ""
  for i in machine:
    # need to convert from 0- to 1-indexed
    machineinput += str(i + 1) + ","
  machineinput = machineinput[:-1] # trim last ','

  progress = (index + 1) / TOTAL_MACHINES
  print(f"Progress {progress:.1%} <|> " + "Current input " + machineinput + "       ", end='\r')
  
  cmd = FILEPATH + " -n " + str(STEPS) + " -ic " + machineinput
  returned_output = subprocess.check_output(cmd)
  for i in range(COLS):
    data[index][i] = machine[i] + 1
  
  data[index][COLS] = int(returned_output.decode("utf-8"))

columns = ["prod" + str(i) for i in range(COLS)]
columns[0] = "start"
columns.append("halt")

df = pd.DataFrame(data, columns=columns)
df.to_csv("CSVs\output_" + str(STEPS) + "_" + str(MAX_INT) + "_" + str(COLS) + ".csv")
print("Finished. Time elapsed:")
print(datetime.now() - startTime)