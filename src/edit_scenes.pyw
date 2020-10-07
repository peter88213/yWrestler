"""Import and export yWriter scene descriptions for editing. 

Convert yWriter scene descriptions to odt with invisible chapter and scene tags.
Convert html with invisible chapter and scene tags to yWriter format.

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
SUFFIX = '_scenes'

import sys

from pywriter.converter.yw_cnv_tk import YwCnvTk
from pywriter.converter.universal_file_factory import UniversalFileFactory


class Converter(YwCnvTk):

    def __init__(self, silentMode=False):
        YwCnvTk.__init__(self, silentMode)
        self.fileFactory = UniversalFileFactory()


if __name__ == '__main__':
    Converter().run(sys.argv[1], SUFFIX)
