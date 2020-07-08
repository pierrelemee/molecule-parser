from molecule.atom import Atom
from molecule.element import Element


class Molecule(Element):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.atoms = []
        self.molecules = []

    def get_container(self):
        return self

    def add_atom(self, atom: Atom):
        self.atoms.append(atom)

    def add_molecule(self, molecule):
        self.molecules.append(molecule)

    def get_atoms(self):
        atoms = {}

        for atom in self.atoms:
            if atom.element in atoms:
                atoms[atom.element] += (self.coefficient * atom.coefficient)
            else:
                atoms[atom.element] = (self.coefficient * atom.coefficient)

        for molecule in self.molecules:
            for element, coefficient in molecule.get_atoms().items():
                if element in atoms:
                    atoms[element] += (self.coefficient * coefficient)
                else:
                    atoms[element] = (self.coefficient * coefficient)

        return atoms

    def lines(self):
        lines = ['+' + ('--' * self.get_depth()) + ' {} [{}]'.format(self.coefficient, ', '.join(
            list(map(lambda a: a.__repr__(), self.atoms))))]

        for molecule in self.molecules:
            for line in molecule.lines():
                lines.append(line)

        return lines

    def __repr__(self):
        return '\n'.join(self.lines())