"""PyWriter v1.2 - Import and export ywriter7 part descriptions for editing. 

Proof reading file format: html (with invisible chapter tags)

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import sys

from pywriter.model.partdesc import PartDesc
from pywriter.converter.cnv_runner import CnvRunner


def run(sourcePath: str, silentMode: bool = True) -> None:
    document = PartDesc('')
    converter = CnvRunner(sourcePath, document, 'html',
                          silentMode, '_parts')


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    run(sourcePath, False)
