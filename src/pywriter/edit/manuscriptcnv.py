""" PyWriter module

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.edit.manuscript import Manuscript
from pywriter.core.yw7file import Yw7File


class ManuscriptCnv():

    def __init__(self, yw7Path, htmlPath):
        self.yw7Path = yw7Path
        self.yw7File = Yw7File(self.yw7Path)
        self.htmlPath = htmlPath
        self.htmlFile = Manuscript(self.htmlPath)

    def yw7_to_document(self):
        """ Read .yw7 file and convert sceneContents to html. """
        if not self.yw7File.filePath:
            return('ERROR: "' + self.yw7Path + '" is not an yWriter 7 project.')

        if not self.yw7File.file_is_present():
            return('ERROR: Project "' + self.yw7Path + '" not found.')

        message = self.yw7File.read()
        if message.count('ERROR'):
            return(message)

        if self.htmlFile.file_is_present():
            self.confirm_overwrite(self.htmlPath)

        self.htmlFile.title = self.yw7File.title
        self.htmlFile.scenes = self.yw7File.scenes
        self.htmlFile.chapters = self.yw7File.chapters
        return(self.htmlFile.write())

    def document_to_yw7(self):
        """ Convert html into yw7 newContents and modify .yw7 file. """
        if not self.yw7File.filePath:
            return('ERROR: "' + self.yw7Path + '" is not an yWriter 7 project.')

        if not self.yw7File.file_is_present():
            return('ERROR: Project "' + self.yw7Path + '" not found.')
        else:
            self.confirm_overwrite(self.yw7Path)

        message = self.yw7File.read()
        if message.count('ERROR'):
            return(message)

        if not self.htmlFile.filePath:
            return('ERROR: "' + self.htmlPath + '" is not a HTML file.')

        if not self.htmlFile.file_is_present():
            return('ERROR: "' + self.htmlPath + '" not found.')

        message = self.htmlFile.read()
        if message.count('ERROR'):
            return(message)

        prjStructure = self.htmlFile.get_structure()
        if prjStructure == '':
            return('ERROR: Source file contains no yWriter project structure information.')

        if prjStructure != self.yw7File.get_structure():
            return('ERROR: Structure mismatch - yWriter project not modified.')

        for scID in self.htmlFile.scenes:
            self.yw7File.scenes[scID].sceneContent = self.htmlFile.scenes[scID].sceneContent

        return(self.yw7File.write())

    def confirm_overwrite(self, fileName):
        pass