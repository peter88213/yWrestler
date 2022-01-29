"""Provide a factory class for a document object to read and a new yWriter project.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory

from pywriter.yw.yw7_file import Yw7File
from pywriter.html.html_import import HtmlImport
from pywriter.html.html_outline import HtmlOutline

from pywriter.html.html_fop import read_html_file


class NewProjectFactory(FileFactory):
    """A factory class that instantiates a document object to read, 
    and a new yWriter project.

    Public methods:
        make_file_objects(self, sourcePath, **kwargs) -- return conversion objects.

    Class constant:
        DO_NOT_IMPORT -- list of suffixes from file classes not meant to be imported.    
    """

    DO_NOT_IMPORT = ['_xref', '_brf_synopsis']

    def make_file_objects(self, sourcePath, **kwargs):
        """Instantiate a source and a target object for creation of a new yWriter project.

        Positional arguments:
            sourcePath -- string; path to the source file to convert.

        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a Novel subclass instance
        - targetFile: a Novel subclass instance
        """
        if not self._canImport(sourcePath):
            return 'ERROR: This document is not meant to be written back.', None, None

        fileName, fileExtension = os.path.splitext(sourcePath)
        targetFile = Yw7File(fileName + Yw7File.EXTENSION, **kwargs)

        if sourcePath.endswith('.html'):

            # The source file might be an outline or a "work in progress".

            result = read_html_file(sourcePath)

            if result[0].startswith('SUCCESS'):

                if "<h3" in result[1].lower():
                    sourceFile = HtmlOutline(sourcePath, **kwargs)

                else:
                    sourceFile = HtmlImport(sourcePath, **kwargs)

                return 'SUCCESS', sourceFile, targetFile

            else:
                return 'ERROR: Cannot read "' + os.path.normpath(sourcePath) + '".', None, None

        else:
            for fileClass in self.fileClasses:

                if fileClass.SUFFIX is not None:

                    if sourcePath.endswith(fileClass.SUFFIX + fileClass.EXTENSION):
                        sourceFile = fileClass(sourcePath, **kwargs)
                        return 'SUCCESS', sourceFile, targetFile

            return 'ERROR: File type of  "' + os.path.normpath(sourcePath) + '" not supported.', None, None

    def _canImport(self, sourcePath):
        """Return True, if the file located at sourcepath is of an importable type.
        Otherwise, return False.
        """
        fileName, fileExtension = os.path.splitext(sourcePath)

        for suffix in self.DO_NOT_IMPORT:

            if fileName.endswith(suffix):
                return False

        return True
