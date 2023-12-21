# Cyts: a cyclic tag system simulator in Haskell

[Cyclic tag systems](https://esolangs.org/wiki/Cyclic_tag_system) can be thought of as very abstract computers. They're simplified [tag systems](https://en.wikipedia.org/wiki/Tag_system) that can simulate any tag system and hence are Turing-complete. cyts can simulate any cyclic tag system, making it a **Turing-complete interpreter.**

Cyts offers a few additional features to improve its usability with simulating cyclic tag systems as a proper interpreter:

* Detects if a halt has happened, both when states repeat and when the register clears
* Pretty-printed machine output
* CLI with interactive (stdinput) and scripting (compact) user input modes
* Binary string and unsigned integer input modes for starting word and productions

## Data analysis
The data-analysis/ folder contains a short script that collects Cyts output on all possible programs of a certain complexity, and some CSVs collected with it. My project is to apply machine learning to the collected data to study program halting in a novel manner. Check out the repository website for more information!