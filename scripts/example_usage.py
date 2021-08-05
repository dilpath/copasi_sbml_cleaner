# Input descriptions. Note: probably fine to only customise input_filename
# and output_filename
# input_filename: the location of COPASI-generated SBML file to be cleaned.
# output_filename: the location where the cleaned SBML will be saved.
# observable_IDs: identifiers of observables to be removed from the SBML file.
# custom_xpaths: describe additional elements to be removed.
# custom_namespaces: namespaces of elements described by `custom_xpaths`.

input_filename  = 'PATH/TO/INPUT/SBML.xml'
output_filename = 'PATH/TO/OUTPUT/SBML_cleaned.xml'

observable_IDs = {
}

custom_xpaths = {
    '//layout:listOfLayouts',
    #'//sbml:annotation'
}
custom_namespaces = {
    'layout': 'http://projects.eml.org/bcb/sbml/level2',
    #'sbml': 'http://www.sbml.org/sbml/level2/version4',
}

from COPASI_SBML_Cleaner import COPASI_SBML_Cleaner
cleaner = COPASI_SBML_Cleaner()
cleaner.load(input_filename)
cleaner.delete_observables(observable_IDs)
cleaner.delete_elements_by_xpath(custom_xpaths, custom_namespaces)
cleaner.save(output_filename)
