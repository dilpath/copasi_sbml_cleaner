from lxml import etree
import tempfile
from typing import Dict, List, Optional, Set

namespace_observables = {'sbml': 'http://www.sbml.org/sbml/level2/version4'}

class COPASI_SBML_Cleaner:
    def __init__(self):
        pass


    def load(self, sbml_filename: str):
        '''
        Load a COPASI-generated SBML file.

        Parameters
        ----------
        sbml_filename:
            The name of the SBML file to be cleaned.
        '''
        self.sbml = etree.parse(sbml_filename)


    def delete_observables(self, observable_IDs: Set[str]):
        '''
        Converts a set of observable IDs into the XPaths that describe their
        parameter and assignment rule elements in SBML generated by COPASI.

        Here, observables are assumed to be implemented as global quantities in
        COPASI, with an assigned formula.

        Parameters
        ----------
        observable_IDs:
            The SBML identifiers of the observables to be deleted.
        '''
        xpaths = set()
        for observable_ID in observable_IDs:
            xpaths |= {f'//sbml:parameter[@id="{observable_ID}"]'}
            xpaths |= {f'//sbml:assignmentRule[@variable="{observable_ID}"]'}
        self.delete_elements_by_xpath(xpaths, namespace_observables)


    def delete_annotations(
            self,
    ):
        '''
        Removes annotations from an SBML file.
        '''
        xpath = '//sbml:annotation'
        namespaces = {
            'sbml': 'http://www.sbml.org/sbml/level2/version4',
        }
        for element in self.sbml.xpath(xpath, namespaces=namespaces):
            element.getparent().remove(element)


    def delete_elements_by_xpath(
            self,
            xpaths: Set[str],
            namespaces: Dict[str, str],
    ):
        '''
        Removes unwanted elements from an SBML file.

        Parameters
        ----------
        xpaths:
            The XPaths of elements to be deleted.

        namespaces:
            The namespaces used in the XPaths.
        '''
        for xpath in xpaths:
            for element in self.sbml.xpath(xpath, namespaces=namespaces):
                element.getparent().remove(element)


    def save(self, output_filename: Optional[str] = None) -> str:
        '''
        Save the current state of the SBML to a file.

        Parameters
        ----------
        output_filename:
            The name of the file to write the SBML to.
        '''
        if output_filename is None:
            sbml_file = tempfile.NamedTemporaryFile(mode='r+', delete=False)
            output_filename = sbml_file.name
        self.sbml.write(
            output_filename,
            encoding='UTF-8',
            pretty_print=True,
            xml_declaration=True,
        )
        return output_filename

