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