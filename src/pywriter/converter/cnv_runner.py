"""Import and export yWriter 7 data. 

Standalone yWriter 7 converter with a simple GUI

Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
from tkinter import *
from tkinter import messagebox

from pywriter.model.novel import Novel
from pywriter.model.yw7file import Yw7File
from pywriter.converter.yw7cnv import Yw7Cnv


TITLE = 'PyWriter v1.5'


class CnvRunner(Yw7Cnv):
    """Standalone yWriter 7 converter with a simple GUI. 

    # Arguments

        sourcePath : str
            a full or relative path to the file to be converted.
            Either an .yw7 file or a file of any supported type. 
            The file type determines the conversion's direction.    

        document : Novel
            instance of any Novel subclass representing the 
            source or target document. 

        extension : str
            File extension determining the source or target 
            document's file type. The extension is needed because 
            there can be ambiguous Novel subclasses 
            (e.g. OfficeFile).
            Examples: 
            - md
            - docx
            - odt
            - html

        silentMode : bool
            True by default. Intended for automated tests. 
            If True, the GUI is not started and no further 
            user interaction is required. Overwriting of existing
            files is forced. 
            Calling scripts shall set silentMode = False.

        suffix : str
            Optional file name suffix used for ambiguous html files.
            Examples:
            - _manuscript for a html file containing scene contents.
            - _scenes for a html file containing scene summaries.
            - _chapters for a html file containing chapter summaries.
    """

    def __init__(self, sourcePath,
                 document,
                 extension,
                 silentMode=True,
                 suffix=''):
        """Run the converter with a GUI. """

        # Prepare the graphical user interface.

        self.root = Tk()
        self.root.geometry("800x360")
        self.root.title(TITLE)
        self.header = Label(self.root, text=__doc__)
        self.header.pack(padx=5, pady=5)
        self.appInfo = Label(self.root, text='')
        self.appInfo.pack(padx=5, pady=5)
        self.successInfo = Label(self.root)
        self.successInfo.pack(fill=X, expand=1, padx=50, pady=5)
        self.processInfo = Label(self.root, text='')
        self.processInfo.pack(padx=5, pady=5)

        self._success = False

        # Run the converter.

        self.silentMode = silentMode
        self.convert(sourcePath, document, extension, suffix)

        # Visualize the outcome.

        if not self.silentMode:

            if self._success:
                self.successInfo.config(bg='green')

            else:
                self.successInfo.config(bg='red')

            self.root.quitButton = Button(text="Quit", command=quit)
            self.root.quitButton.config(height=1, width=10)
            self.root.quitButton.pack(padx=5, pady=5)
            self.root.mainloop()

    def convert(self, sourcePath,
                document,
                extension,
                suffix):
        """Determine the direction and invoke the converter. """

        # The conversion's direction depends on the sourcePath argument.

        if not os.path.isfile(sourcePath):
            self.processInfo.config(text='ERROR: File not found.')

        elif sourcePath.endswith('.yw7'):
            yw7Path = sourcePath

            # Generate the target file path.

            document.filePath = sourcePath.split(
                '.yw7')[0] + suffix + '.' + extension
            self.appInfo.config(
                text='Export yWriter7 scenes content to ' + extension)
            self.processInfo.config(text='Project: "' + yw7Path + '"')

            # Instantiate an Yw7File object and pass it along with
            # the document to the converter class.

            yw7File = Yw7File(yw7Path)
            self.processInfo.config(
                text=self.yw7_to_document(yw7File, document))

        elif sourcePath.endswith(suffix + '.' + extension):
            document.filePath = sourcePath

            # Determine the project file path.

            yw7Path = sourcePath.split(suffix + '.' + extension)[0] + '.yw7'
            self.appInfo.config(
                text='Import yWriter7 scenes content from ' + extension)
            self.processInfo.config(
                text='Proofed scenes in "' + document.filePath + '"')

            # Instantiate an Yw7File object and pass it along with
            # the document to the converter class.

            yw7File = Yw7File(yw7Path)
            self.processInfo.config(
                text=self.document_to_yw7(document, yw7File))

        else:
            self.processInfo.config(
                text='ERROR: File type is not supported.')

        # Visualize the outcome.

        if self.processInfo.cget('text').startswith('SUCCESS'):
            self._success = True

    def confirm_overwrite(self, filePath):
        """ Invoked by the parent if a file already exists. """

        if self.silentMode:
            return True

        else:
            return messagebox.askyesno('WARNING', 'Overwrite existing file "' + filePath + '"?')

    def edit(self):
        pass
