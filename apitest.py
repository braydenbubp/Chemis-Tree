from chemspipy import ChemSpider

# cs = ChemSpider('rxSH6fXVGTFYU8GrTyJ6l6STu8MqXUh8')

# c = cs.get_compound(2157)

# print(c.molecular_formula)
# print(c.molecular_weight)
# print(c.smiles)
# print(c.common_name)

# for result in cs.search('C44H30N4Zn'):
#     print(result)


# creating a compound
# compound = cs.get_compound(2157)

# this instantiates the compound directly
# compound = Compound(cs, 2157)

# refs = cs.get_external_references(2157, datasources=['PubChem'])
# print(refs)

# info = cs.get_details(2157)
# print(info.keys())
# print(info['smiles'])

# print(cs.get_datasources())

# print(cs.convert('c1ccccc1', 'SMILES', 'InChI'))
# allowed conversions
# From InChI to InChIKey
# From InChI to Mol
# From InChI to SMILES
# From InChIKey to InChI
# From InChIKey to Mol
# From Mol to InChI
# From Mol to InChIKey
# From SMILES to InChI


# FE calls BE with request, BE querys 3rd party api, serializes, then sends to FE. 
# SQlite can still be used 
# below is how this might look

