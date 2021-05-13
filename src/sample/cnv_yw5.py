"""Convert yWriter 7 to yWriter 5 format.

This is a PyWriter sample application.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import sys

from pywriter.ui.ui_tk import UiTk
from pywriter.converter.yw_cnv_ui import YwCnvUi
from pywriter.converter.abstract_file_factory import AbstractFileFactory

from pywriter.yw.yw5_new_file import Yw5NewFile
from pywriter.yw.yw7_file import Yw7File


class MyFileFactory(AbstractFileFactory):
    EXPORT_SOURCE_CLASSES = [Yw7File]
    EXPORT_TARGET_CLASSES = [Yw5NewFile]


def run(sourcePath, suffix=None):
    ui = UiTk('yWriter import/export')
    converter = YwCnvUi()
    converter.ui = ui
    converter.fileFactory = MyFileFactory()
    converter.run(sourcePath, suffix)
    ui.start()


if __name__ == '__main__':
    run(sys.argv[1], None)
