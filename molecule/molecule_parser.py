from molecule.molecule import Molecule, Atom
from molecule.molecule_parser_exception import MoleculeParserException


class MoleculeParser:
    opening_brackets = '({['
    closing_brackets = ')}]'

    @staticmethod
    def parse(formula: str) -> Molecule:
        molecule = Molecule()
        element = molecule
        index = 0
        brackets = []
        while index < len(formula):
            character = formula[index]
            # When reading an upper case letter
            if character.isupper():
                index += 1
                buffer = character
                # Read all the following lower case letters as part of an atom
                while index < len(formula) and formula[index].islower():
                    buffer += formula[index]
                    index += 1
                atom = Atom(buffer, molecule)
                molecule.add_atom(atom)
                element = atom
            # When reading an upper case letter
            elif character.isnumeric():
                coefficient = int(character)
                index += 1
                # Read all the following digits and update the global value (in 10 basis)
                while index < len(formula) and formula[index].isnumeric():
                    coefficient = (coefficient * 10) + int(formula[index])
                    index += 1
                element.coefficient = coefficient
            # When encountering an opening bracket
            elif character in MoleculeParser.opening_brackets:
                brackets.append((character, index))
                submolecule = Molecule(molecule)
                molecule.add_molecule(submolecule)
                molecule = submolecule
                element = molecule
                index += 1
            # When encountering a closing bracket
            elif character in MoleculeParser.closing_brackets:
                if len(brackets) == 0:
                    raise MoleculeParserException("Unexpected closing bracket '{}'".format(character), formula, index)
                if MoleculeParser.closing_brackets.index(character) != MoleculeParser.opening_brackets.index(brackets[-1][0]):
                    raise MoleculeParserException("Unexpected closing bracket '{}', expecting '{}' opened at {}".format(character, MoleculeParser.closing_brackets[MoleculeParser.opening_brackets.index(brackets[-1][0])], brackets[-1][1]), formula, index)
                brackets.pop(-1)
                element = molecule
                molecule = molecule.parent
                index += 1
            else:
                raise MoleculeParserException("Unexpected character '{}'".format(formula[index]), formula, index)

        return molecule.get_root()
