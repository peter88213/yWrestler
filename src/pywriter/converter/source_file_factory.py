"""Provide a factory class for any import source object.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os

from pywriter.converter.file_factory import FileFactory


class SourceFileFactory(FileFactory):
    """A factory class that instantiates an import source file object."""

    def __init__(self):
        self.sourceClasses = []
        # List of FileExport subclasses. To be set by the caller.

    def make_file_objects(self, sourcePath, suffix=None):
        """Instantiate a source object for conversion to a yWriter format.

        Return a tuple with three elements:
        - A message string starting with 'SUCCESS' or 'ERROR'
        - sourceFile: a YwFile subclass instance, or None in case of error
        - targetFile: None
        """

        for sourceClass in self.sourceClasses:

            if sourceClass.SUFFIX is None:
                suffix = ''

            else:
                suffix = sourceClass.SUFFIX

            if sourcePath.endswith(suffix + sourceClass.EXTENSION):
                sourceFile = sourceClass(sourcePath)
                return 'SUCCESS', sourceFile, None

        return 'ERROR: File type of "' + os.path.normpath(sourcePath) + '" not supported.', None, None
