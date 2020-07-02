from typing import Optional
from molecule.molecule_node import MoleculeNode
from molecule.molecule_parser_exception import MoleculeParserException


class MoleculeParser:
    @staticmethod
    def parse(formula: str) -> MoleculeNode:
        root = MoleculeNode()
        index = 0
        atom = ''
        quantity = 1
        molecule: Optional[MoleculeNode] = None
        while index < len(formula):
            character = formula[index]
            # When reading an upper case letter
            if character.isupper():
                if molecule is not None:
                    # In case of recently read sub-molecule, apply the quantity as molecule coefficient
                    molecule.coefficient(quantity)
                    root.add_molecule(molecule)
                elif len(atom) > 0:
                    root.add_atom(atom, quantity)
                # Reset parsing state
                quantity = 1
                molecule = None

                atom = formula[index]
                index += 1
                # Read all the following lower case letters as part of an atom
                while index < len(formula) and formula[index].islower():
                    atom += formula[index]
                    index += 1
            # When reading an upper case letter
            elif formula[index].isnumeric():
                quantity = int(formula[index])
                index += 1
                # Read all the following digits and update the global value (in 10 basis)
                while index < len(formula) and formula[index].isnumeric():
                    quantity = (quantity * 10) + int(formula[index])
                    index += 1
            # When encountering an opening bracket
            elif formula[index] in "({[":
                if molecule is not None:
                    # In case of recently read sub-molecule, apply the quantity as molecule coefficient
                    molecule.coefficient(quantity)
                    root.add_molecule(molecule)
                elif len(atom) > 0:
                    root.add_atom(atom, quantity)
                # Reset parsing state
                quantity = 1
                atom = ''

                # Look for the appropriate closing bracket
                closing_bracket = ")}]"["({[".index(formula[index])]
                try:
                    # Compute the substring to be used as sub molecule parsing
                    end_index = (index + 1) + formula[index+1:].rindex(closing_bracket)
                    try:
                        molecule = MoleculeParser.parse(formula[index + 1:end_index])
                        index = end_index + 1
                    except ValueError:
                        # If no such valid substring exists it means closing bracket is missing
                        raise MoleculeParserException("Unclosed bracket character '{}'".format(formula[index]), formula, index)
                except ValueError:
                    raise MoleculeParserException("Unclosed bracket character '{}'".format(formula[index]), formula,index)
                except MoleculeParserException as e:
                    # Bubble up exceptions coming sub parsing
                    raise MoleculeParserException("Unclosed bracket character '{}'".format(e.formula[e.index]), formula, e.index + index + 1)
            else:
                raise MoleculeParserException("Unexpected character '{}'".format(formula[index]), formula, index)

        if molecule is not None:
            molecule.coefficient(quantity)
            root.add_molecule(molecule)
        elif len(atom) > 0:
            root.add_atom(atom, quantity)

        return root