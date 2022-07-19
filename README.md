# Open Task Planning Library (OTPL)

This library consists of Python modules that can be used to support PDDL planning related projects. The code supports all features of temporal PDDL 2.2. 

Current modules include:
- PDDL2.2 parser and data structures.
- Grounding.
- Planning Graphs.
- Plan representations.
- Temporal Networks to represent temporal plans.

Use the [examples](examples) directory to see more.

### Requirements

Install the runtime requirements using:
```bash
pip install -r requirements.txt
```

OTPL has the following optional dependencies:
- [https://www.antlr.org/](ANTLR) (needed to regenerate the PDDL parser after changes to the ANTLR grammar file.)
- [https://www.doxygen.nl/index.html](Doxygen) (needed to create a local copy of the documentation.)

### Literature

- PDDL - The Planning Domain Definition Language. Ghallab, M., Knoblock, C., Wilkins, D., Barrett, A., Christianson, D., Friedman, M., Kwok, C., Golden, K., Penberthy, S., Smith, D., Sun, Y., & Weld, D. (1998). 
- PDDL2.1: An Extension to PDDL for Expressing Temporal Planning Domains. Fox, M., & Long, D. (2003). [http://arxiv.org/abs/1106.4561](PDF)
- PDDL2.2: The Language for the Classical Part of the 4th International planning Competition. Technical Report No. 195. Institut für Informatik. Edelkamp, S. & Hoffmann, J. (2003). [https://gki.informatik.uni-freiburg.de/teaching/ws0607/aip/pddl2.2.pdf](PDF)