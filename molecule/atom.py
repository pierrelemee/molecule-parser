from molecule.element import Element


class Atom(Element):
    def __init__(self, element: str, parent):
        super().__init__(parent)
        self.element = element

    def get_container(self):
        return self.parent

    def __repr__(self):
        return "('{}': {})".format(self.element, self.coefficient)
