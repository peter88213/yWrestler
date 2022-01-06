"""Provide a strategy class to write ANSI encoded yWriter project files.

DEPRECATED -- This module is no longer provided for v4.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
from pywriter.yw.utf8_tree_writer import Utf8TreeWriter


class AnsiTreeWriter(Utf8TreeWriter):
    """Write ANSI encoded yWriter project file."""

    def write_element_tree(self, ywProject):
        """Write back the xml element tree to a yWriter xml file located at filePath.
        Return a message beginning with SUCCESS or ERROR.
        Override the superclass method.
        """

        try:
            ywProject.tree.write(
                ywProject.filePath, xml_declaration=False, encoding='iso-8859-1')

        except(PermissionError):
            return 'ERROR: "' + os.path.normpath(ywProject.filePath) + '" is write protected.'

        return 'SUCCESS'
