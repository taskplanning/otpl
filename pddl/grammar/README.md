To make changes to the PDDL grammar and update the Python visitor and parser, first alter the pddl22.g4 file then regenerate the Python code:
```
antlr4 -Dlanguage=Python3 pddl22.g4 -visitor
```