from unittest import TestCase

from molecule import MoleculeParser


class ParserTest(TestCase):

    def test_parsing_ok(self):
        molecules = {
            'H2O': {'H': 2, 'O': 1},  # 'water':
            'Mg(OH)2': {'Mg': 1, 'O': 2, 'H': 2},  # magnesium_hydroxide
            'K4[ON(SO3)2]2': {'K': 4, 'O': 14, 'N': 2, 'S': 4}  # fremy_salt
        }

        for formula, atoms in molecules.items():
            self.assertDictEqual(atoms, MoleculeParser.parse(formula).get_atoms(), "Invalid formula {}".format(formula))

    def test_parsing_ko(self):
        formulas = {
            'notaformula': 'Unexpected character n at index 0',
            ')(': 'Unexpected character ) at index 0',
            '[ HN02)}': 'Unclosed bracket character [ at index 0'
        }

        for formula, message in formulas.items():
            with self.assertRaises(Exception) as context:
                MoleculeParser.parse(formula)

            self.assertTrue(message in str(context.exception), "Unexpected exception message '{}'".format(str(context.exception)))
