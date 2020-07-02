
class MoleculeParserException(Exception):
    def __init__(self, message: str, formula: str, index: int = 0):
        self.formula = formula
        self.index = index

        super(Exception, self).__init__(message + " at index {} in formula '{}'".format(self.index, self.formula))
