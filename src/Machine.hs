module Machine where 
-- (Alphabet(..), Machine.Word, State(..), printer, runMachineFromInputs, findrepeatedstate) where

--- Basic type definitions ---

data Alphabet = Zero | One
    deriving (Show, Eq)

type Word = [Alphabet]

-- Helper function to print a word out, right-associative
printer :: Machine.Word -> String
printer [] = ""
printer (Zero:xs) = "0" ++ printer xs
printer (One:xs) = "1" ++ printer xs

-- Encapsulates the state of the system at a snapshot
-- First Int is step count, second is number of productions (and should be kept constant)
data State = State [Machine.Word] Machine.Word Int Int
            | Halted Int
            | Empty

-- Defines Show and Eq on states
-- Eq is a weaker equality which considers repeated states equal
-- Possible way to find true repeats that accounts for duplicate words:
    -- zip productions with indices and match on both of them
instance Show State where
    show (State p w i _) = printer w ++ " at step " ++ show i ++ ", next production " ++ printer (head p)
    show (Halted i) = "Halted at step " ++ show i
    show Empty = "N/A"
instance Eq State where
    (==) (State p1 w1 i1 ps1) (State p2 w2 i2 ps2) = (head p1 == head p2) 
        && (w1 == w2) 
        && (ps1 == ps2) -- technically always true, since program execution only ever considers one CTS
        && (rem i1 ps1 == rem i2 ps2)
    (==) State {} _ = False
    (==) _ State {}  = False
    (==) _ _ = True

--- Running the machine ---

-- Logic to update the machine at each step
update :: State -> State
update (State (p:productions) (Zero:xs) i ps) = State productions xs (i + 1) ps
update (State (p:productions) (One:xs) i ps) = State productions (xs ++ p) (i + 1) ps
update (State _ [] i _) = Halted i
update (State [] xs i _) = Empty -- invalid state; cycle throws error on an empty list, so this may not be needed
update (Halted i) = Empty
update Empty = Empty -- invalid state

-- Runs the machine off steps and an initial state, allows specifying productions and starting word instead with runMachine
runMachine :: Int -> State -> [State]
runMachine n initstate = take (n + 1) (iterate update initstate)

runMachineFromInputs :: Int -> [Machine.Word] -> Machine.Word -> [State]
runMachineFromInputs n productions word = runMachine n (State (cycle productions) word 0 (length productions))

-- Pretty-print each state in sequence
alignout :: State -> String
alignout s@(State p w i _) = replicate i ' ' ++ show s ++ "\n"
alignout s@(Halted i) = replicate (i + 1) ' ' ++ show s ++ "\n"
alignout Empty = ""

printoutputs :: [State] -> String
printoutputs = concatMap alignout

-- Searches for repeated states, and returns the first repeated state
-- Hangs forever if used on an infinite nonhalting CTS
findrepeatedstate :: [State] -> State
findrepeatedstate [] = Empty
findrepeatedstate (s:states) = if s `elem` states then s else findrepeatedstate states

-- Finds last state in a CTS
findLast :: [State] -> State
findLast [] = Empty
findLast (x:xs)
            | x == Halted 0 = x
            | null xs       = x
            | otherwise = findLast xs 