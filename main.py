from typing import Optional


class MoleculeNode:

    def __init__(self, parent=None):
        self.parent = parent
        self.atoms = {}
        self.molecules = []

    def is_root(self):
        return self.parent is None

    def get_depth(self):
        if self.parent is None:
            return 0
        return 1 + self.parent.get_depth()

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def add_atom(self, atom: str, quantity: int = 1):
        if atom in self.atoms:
            self.atoms[atom] += quantity
        else:
            self.atoms[atom] = quantity

    def coefficient(self, coefficient):
        for atom in self.atoms.keys():
            self.atoms[atom] = self.atoms[atom] * coefficient
        for molecule in self.molecules:
            molecule.coefficient(coefficient)

    def add_molecule(self, molecule):
        molecule.parent = self
        self.molecules.append(molecule)

    def get_atoms(self, atoms=None):
        if atoms is None:
            atoms = self.atoms.copy()
        else:
            for atom,quantity in self.atoms.items():
                if atom in atoms:
                    atoms[atom] += quantity
                else:
                    atoms[atom] = quantity

        for molecule in self.molecules:
            molecule.get_atoms(atoms)
        return atoms

    def lines(self):
        lines = []
        lines.append(('+-' if self.is_root() else '|-') + ('---' * self.get_depth()) + ' ' + str(self.atoms))
        for molecule in self.molecules:
            lines += molecule.lines()

        return lines

    def __repr__(self):
        return '\n'.join(self.lines())


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


if __name__ == '__main__':
    water = 'H2O'
    print(MoleculeParser.parse(water).get_atoms())
    magnesium_hydroxide = "Mg(OH)2"
    print(MoleculeParser.parse(magnesium_hydroxide).get_atoms())
    fremy_salt = 'K4[ON(SO3)2]2'
    print(MoleculeParser.parse(fremy_salt).get_atoms())
    propanal = "CH3CH2CHO"
    print(MoleculeParser.parse(propanal).get_atoms())
    dihydroxyacetone = "CO(CH2OH)2"
    print(MoleculeParser.parse(dihydroxyacetone).get_atoms())
