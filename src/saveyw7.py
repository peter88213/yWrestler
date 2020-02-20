"""PyWriter v1.3 - Convert html to yw7. 

Input file format: html (with visible or invisible chapter and scene tags).

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys
import os

from pywriter.model.html_proof import HtmlProof
from pywriter.model.html_manuscript import HtmlManuscript
from pywriter.model.html_scenedesc import HtmlSceneDesc
from pywriter.model.html_chapterdesc import HtmlChapterDesc
from pywriter.model.html_partdesc import HtmlPartDesc
from pywriter.model.yw7file import Yw7File
from pywriter.converter.yw7cnv import Yw7Cnv


def run(sourcePath):
    sourcePath = sourcePath.replace('file:///', '').replace('%20', ' ')

    if sourcePath.endswith('_proof.html'):
        yw7Path = sourcePath.split('_proof.html')[0] + '.yw7'
        sourceDoc = HtmlProof(sourcePath)

    elif sourcePath.endswith('_manuscript.html'):
        yw7Path = sourcePath.split('_manuscript.html')[0] + '.yw7'
        sourceDoc = HtmlManuscript(sourcePath)

    elif sourcePath.endswith('_scenes.html'):
        yw7Path = sourcePath.split('_scenes.html')[0] + '.yw7'
        sourceDoc = HtmlSceneDesc(sourcePath)

    elif sourcePath.endswith('_chapters.html'):
        yw7Path = sourcePath.split('_chapters.html')[0] + '.yw7'
        sourceDoc = HtmlChapterDesc(sourcePath)

    elif sourcePath.endswith('_parts.html'):
        yw7Path = sourcePath.split('_parts.html')[0] + '.yw7'
        sourceDoc = HtmlPartDesc(sourcePath)

    else:
        return 'ERROR: No yWriter project content.'

    yw7File = Yw7File(yw7Path)
    converter = Yw7Cnv()

    message = converter.document_to_yw7(sourceDoc, yw7File)

    try:
        os.remove(sourcePath)
    except:
        pass

    return message


if __name__ == '__main__':
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    print(run(sourcePath))
