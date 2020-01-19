"""Book - represents the basic structure of a book in yWriter.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.model.yw7file import Yw7File


class Book():
    """yWriter scene representation.

    # Attributes

    title : str
        the scene title.

    desc : str
        scene summary.

    filePath : str
        Location of the book project folder.

    wordCount : int 
        (to be updated by the sceneContent setter).

    letterCount : int 
        (to be updated by the sceneContent setter).

    """

    def __init__(self, filePath):
        self.title = ''
        self.desc = ''
        self.wordCount = 0
        self.letterCount = 0
        self.filePath = filePath
        self.update()

    def update(self):
        book = Yw7File(self.filePath)
        book.read()
        self.title = book.title
        self.desc = book.desc

        self.wordCount = 0
        self.letterCount = 0

        for scId in book.scenes:
            self.wordCount = self.wordCount + book.scenes[scId].wordCount
            self.letterCount = self.letterCount + book.scenes[scId].letterCount

        del book
