from unittest import TestCase

from molecule import MoleculeParser


class ParserTest(TestCase):

    def test_parsing_ok(self):
        molecules = {
            'H2O': {'H': 2, 'O': 1},  # 'water':
            'Mg(OH)2': {'Mg': 1, 'O': 2, 'H': 2},  # magnesium_hydroxide
            'K4[ON(SO3)2]2': {'K': 4, 'O': 14, 'N': 2, 'S': 4},  # fremy_salt
            'O((CN2)3K)4': {'O': 1, 'N': 24, 'C': 12, 'K': 4},
            '[{(Mn7)}]': {'Mn': 7},
            '(CH3)(NH4)2ON3(CO2)': {'C': 2, 'H': 11, 'N': 5, 'O': 3},
            '(K4[ON(SO3)2]2O(N(SO3)3)((K2)23NMg(O))4)': {'K': 188, 'O': 28, 'N': 7,'S': 7, 'Mg': 4},  # Complex case 1
            '[Fe(SO4)2(NH4)2][H2O]6': {'Fe': 1, 'S': 2, 'O': 14, 'N': 2, 'H': 20},  # Complex case 2
            'C169719H270466N45688O52238S911': {'C': 169719, 'H': 270466, 'N': 45688, 'O': 52238, 'S': 911},  # Complex case 3
        }

        for formula, atoms in molecules.items():
            self.assertDictEqual(atoms, MoleculeParser.parse(formula).get_atoms(), "Invalid formula {}".format(formula))

    def test_parsing_ko(self):
        formulas = {
            'notaformula': "Unexpected character 'n' at index 0 in formula 'notaformula'",
            ')(': "Unexpected closing bracket ')' at index 0 in formula ')('",
            '[HN02)}': "Unexpected closing bracket ')', expecting ']' opened at 0 at index 5 in formula '[HN02)}'",
            '[{(Mn7))}]': "Unexpected closing bracket ')', expecting '}' opened at 1 at index 7 in formula '[{(Mn7))}]'"
        }

        for formula, message in formulas.items():
            with self.assertRaises(Exception) as context:
                MoleculeParser.parse(formula)

            self.assertTrue(message in str(context.exception), "Unexpected exception message '{}', excepted '{}'".format(str(context.exception), message))
