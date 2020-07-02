from molecule import MoleculeParser

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
