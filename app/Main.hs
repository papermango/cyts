module Main where

import Machine
import Parsing
import Options.Applicative

main :: IO ()
main = execute =<< execParser Parsing.opts

-- Main function to handle inputs
execute :: Options -> IO ()

-- No input; default execution
execute opts@(Options _ _ _ _ Nothing) = executeOnInput opts defProds defWord

-- Compact (scripting) input
-- Overrides two bucketed options, so it goes first
execute (Options _ steps _ True (Just (CompactInput input)))  = compactModeOutput . findrepeatedstate $ runMachineCompact (readCIntsAsBins input) steps
execute (Options _ steps _ False (Just (CompactInput input))) = compactModeOutput . findrepeatedstate $ runMachineCompact (readCBinStrs input) steps

-- File input
execute opts@(Options _ _ _ True (Just (FileInput fp))) = print "Unimplemented"
execute opts@(Options _ _ _ False (Just (FileInput fp))) =  print "Unimplemented"

-- Stdin input
execute opts@(Options _ _ _ True (Just StdInput)) = do
    putStrLn "Enter starting word as an integer: "
    wordstr <- getLine
    putStrLn "Enter list of productions as integers, space-separated: "
    prodstr <- getLine
    putStrLn "---"
    executeOnInput opts (readIntsAsBins prodstr) (head $ readIntsAsBins wordstr)

execute opts@(Options _ _ _ False (Just StdInput)) = do
    putStrLn "Enter starting word in binary: "
    wordstr <- getLine
    putStrLn "Enter list of productions in binary, space-separated: "
    prodstr <- getLine
    putStrLn "---"
    executeOnInput opts (readBinStrs prodstr) (head $ readBinStrs wordstr)

--- Print IO actions to stitch together program cmd output from ---

printProductions :: [Machine.Word] -> IO ()
printProductions prod = putStr "Productions: " >> print (map printer prod) >> putStrLn ""

-- Prints a found repeated state in a given machine
printFoundRepeatedState :: [State] -> IO ()
printFoundRepeatedState = (putStr "Repeated/halted state at " >>) . print . findrepeatedstate

-- Runs and prints the machine, including repeated state if asked for via True bool
printShortMachine :: Int -> [Machine.Word] -> Machine.Word -> Bool -> IO ()
printShortMachine steps productions word findrepeats = do
    printProductions productions
    print (head machineout)
    putStrLn ""
    print (findLast machineout)
    if findrepeats then printFoundRepeatedState machineout else putStr ""
        where machineout = runMachineFromInputs steps productions word

-- Runs and prints the machine verbosely, with same behavior as above
printLongMachine :: Int -> [Machine.Word] -> Machine.Word -> Bool -> IO ()
printLongMachine steps productions word findrepeats = do
    printProductions productions
    putStrLn "Output:"
    putStrLn (printoutputs machineout)
    if findrepeats then printFoundRepeatedState machineout else putStr ""
        where machineout = runMachineFromInputs steps productions word

-- Handles non-input half of execute function
executeOnInput :: Options -> [Machine.Word] -> Machine.Word -> IO ()
executeOnInput (Options True n fr _ _) productions word = printLongMachine n productions word fr
executeOnInput (Options False n fr _ _) productions word = printShortMachine n productions word fr

-- For compact mode: accepts found repeating state and prints expected 
compactModeOutput :: State -> IO ()
compactModeOutput Empty              = print (-1)
compactModeOutput (Halted step)      = print step
compactModeOutput (State _ _ step _) = print step

--- Default variables ---

defProds :: [Machine.Word]
defProds = [[Zero, One, Zero],
                [One, Zero],
                [One, One],
                []]

-- Starting word
defWord :: Machine.Word
defWord = [One, Zero, One, Zero, One]