module Parsing where
-- (opts, Options(..), Input(..)) where

import Machine
import Options.Applicative
import Text.Read (readMaybe)
import Data.List.Split (splitOn)
import Data.List (dropWhileEnd)
import Data.Char (isSpace)
import Machine

--- Command line parser code, using optparse-applicative package ---

-- Available options
data Options = Options
    { verbose       :: Bool
    , stepsran      :: Int
    , detectrepeats :: Bool
    , inputIntMode  :: Bool
    , inputData     :: Maybe Input}

parseoptions :: Parser Options
parseoptions = Options
    <$> switch
        ( long "verbose"
        <> short 'v'
        <> help "Print the full machine runtime; otherwise, output end state only" )
    <*> option auto
        ( long "steps"
        <> short 'n'
        <> help "Steps count to run machine for"
        <> showDefault
        <> value 100
        <> metavar "INT" )
    <*> switch
        ( long "detectrepeats"
        <> short 'r'
        <> help "Look for a repeated state after running the machine")
    <*> switch
        ( long "integerinput"
        <> short 'i'
        <> help "Input initial machine state with unsigned integer representation" )
    <*> input -- Machine input parser, see below

-- Wraps parser up with high-level help text and adds --help
opts :: ParserInfo Options
opts = info (parseoptions <**> helper)
    ( fullDesc
    <> progDesc "Simulate a cyclic tag system to a given number of steps. Halts are recognized only if the register clears. Optionally looks for repeating states after execution, which is the standard way to interpret halting in a cyclic tag system. Looking for repeats is quadratic in the number of steps run and linear in register length."
    <> header "cyts - a cyclic tag system simulator written in Haskell")

-- Parser for machine input --

data Input
  = FileInput FilePath
  | StdInput
  | CompactInput String

fileInput :: Parser Input
fileInput = FileInput <$> strOption
  (  long "file"
  <> short 'f'
  <> metavar "FILENAME"
  <> help "Read initial machine state from input file FILENAME" )

stdInput :: Parser Input
stdInput = flag' StdInput
  (  long "stdin"
  <> short 's'
  <> help "Read initial machine state interactively from stdin" )

cmdInput :: Parser Input
cmdInput = CompactInput <$> strOption
  (  long "compact"
  <> short 'c'
  <> help "Compact (scripting) mode. Reads initial machine state from command line as a comma-separated string and prints the step at which the machine halted to stdout, -1 if not halted. Overrides -v and -r." )

-- optional sets input to be optional
input :: Parser (Maybe Input)
input = optional $ fileInput <|> stdInput <|> cmdInput

--- Read machine input ---

-- Converts binary string into a Machine.Word. Ignores symbols that are not 0 or 1
readBinStr :: String -> Machine.Word
readBinStr "" = []
readBinStr (x:xs)
    | x == '0'  = Zero : readBinStr xs
    | x == '1'  = One : readBinStr xs
    | x == '-'  = []
    | otherwise = readBinStr xs
-- Reads off space-separated ints into a list of words
readBinStrs :: String -> [Machine.Word]
readBinStrs = map readBinStr . words

-- Converts integer into word
readIntAsBin :: Int -> Machine.Word
readIntAsBin x
    | x <= 1   = []
    | rem == 0 = readIntAsBin div ++ [Zero]
    | rem == 1 = readIntAsBin div ++ [One]
    | otherwise = []
    where (div, rem) = divMod x 2
-- Reads off space-separated ints into a list of words
readIntsAsBins :: String -> [Machine.Word]
readIntsAsBins = map (readIntAsBin . maybe 0 id)
                    . filter (Nothing /=)
                    . map (\x -> readMaybe x :: Maybe Int)
                    . words

-- Trim whitespace, from StackOverflow
trim = dropWhileEnd isSpace . dropWhile isSpace

-- Reads off comma-separated ints into a list of words for compact mode
readCIntsAsBins :: String -> [Machine.Word]
readCIntsAsBins = map (readIntAsBin . maybe 0 id)
                    . filter (Nothing /=)
                    . map ((\x -> readMaybe x :: Maybe Int) . trim)
                    . splitOn "," -- can change to splitOneOf

-- Reads off comma-separated binary strings into a list of words for compact mode
readCBinStrs :: String -> [Machine.Word]
readCBinStrs = map readBinStr . splitOn ","

-- Runs machine in compact mode
runMachineCompact :: [Machine.Word] -> Int -> [State]
runMachineCompact (x:xs) steps = Machine.runMachineFromInputs steps xs x
runMachineCompact [] _ = []