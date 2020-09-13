"""yW7NewFile - Class for yWriter 7 xml file creation.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.yw.yw_file import YwFile
from pywriter.yw.yw7_tree_creator import Yw7TreeCreator
from pywriter.yw.utf8_tree_reader import Utf8TreeReader
from pywriter.yw.utf8_tree_writer import Utf8TreeWriter
from pywriter.yw.utf8_postprocessor import Utf8Postprocessor


class Yw7NewFile(YwFile):
    """yWriter 7 xml project file representation."""

    EXTENSION = '.yw7'

    def __init__(self, filePath):
        YwFile.__init__(self, filePath)
        self.ywTreeReader = Utf8TreeReader()
        self.ywTreeBuilder = Yw7TreeCreator()
        self.ywTreeWriter = Utf8TreeWriter()
        self.ywPostprocessor = Utf8Postprocessor()
