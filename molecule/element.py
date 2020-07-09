from abc import abstractmethod


class Element:
    def __init__(self, parent=None):
        self.coefficient = 1
        self.parent = parent

    def is_root(self):
        return self.parent is None

    def get_root(self):
        return self if self.parent is None else self.parent

    def get_depth(self):
        if self.parent is None:
            return 0
        return 1 + self.parent.get_depth()

    @abstractmethod
    def get_container(self):
        pass