from typing import Optional
from molecule.molecule_node import MoleculeNode


class MoleculeParser:
    @staticmethod
    def parse(formula: str) -> MoleculeNode:
        root = MoleculeNode()
        index = 0
        atom = ''
        quantity = 1
        molecule: Optional[MoleculeNode] = None
        while index < len(formula):
            if formula[index].isupper():
                if molecule is not None:
                    molecule.coefficient(quantity)
                    root.add_molecule(molecule)
                elif len(atom) > 0:
                    root.add_atom(atom, quantity)
                quantity = 1
                atom = ''
                molecule = None

                atom = formula[index]
                index += 1
                while index < len(formula) and formula[index].islower():
                    atom += formula[index]
                    index += 1
            elif formula[index].isnumeric():
                quantity = int(formula[index])
                index += 1
                while index < len(formula) and formula[index].isnumeric():
                    quantity = (quantity * 10) + int(formula[index])
                    index += 1
            elif formula[index] in "({[":
                if molecule is not None:
                    molecule.coefficient(quantity)
                    root.add_molecule(molecule)
                elif len(atom) > 0:
                    root.add_atom(atom, quantity)
                quantity = 1
                atom = ''
                molecule = None

                closing_bracket = ")}]"["({[".index(formula[index])]
                try:
                    end_index = (index + 1) + formula[index+1:-1].index(closing_bracket)
                    molecule = MoleculeParser.parse(formula[index + 1:end_index])
                    index = end_index + 1
                except ValueError:
                    raise Exception("Unclosed bracket character " + formula[index] + " at index " + str(index))
            else:
                raise Exception("Unexpected character " + formula[index] + " at index " + str(index))

        if molecule is not None:
            molecule.coefficient(quantity)
            root.add_molecule(molecule)
        elif len(atom) > 0:
            root.add_atom(atom, quantity)

        return root