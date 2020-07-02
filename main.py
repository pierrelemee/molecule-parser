import json
from molecule import MoleculeParser
import sys

if __name__ == '__main__':
    # Whether to read data from stdin or
    read_from_stdin = False
    write_as_json = False
    formulas = []
    for arg in sys.argv[1:]:
        if arg.lower() == '--stdin' or arg.lower() == '-i':
            read_from_stdin = True
        elif arg.lower() == '--json' or arg.lower() == '-j':
            write_as_json = True
        else:
            formulas.append(arg)



    if read_from_stdin:
        formulas = list(map(lambda line: line.rstrip(), sys.stdin.readlines()))

    if write_as_json:
        print(json.dumps(list(map(lambda formula: MoleculeParser.parse(formula).get_atoms(), formulas)), sort_keys=True, indent=4))
    else:
        for formula in formulas:
            print(MoleculeParser.parse(formula).get_atoms())
