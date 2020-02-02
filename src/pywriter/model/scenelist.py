"""SceneList - Class for csv scenes table.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import re

from pywriter.model.novel import Novel
from pywriter.model.pywfile import PywFile
from pywriter.model.scene import Scene

SEPARATOR = '|'     # delimits data fields within a record.
LINEBREAK = '\t'    # substitutes embedded line breaks.

TABLE_HEADER = ('Scene link'
                + SEPARATOR
                + 'Scene title'
                + SEPARATOR
                + 'Scene description'
                + SEPARATOR
                + 'Word count'
                + SEPARATOR
                + 'Letter count'
                + SEPARATOR
                + 'Tags'
                + SEPARATOR
                + 'Scene notes'
                + '\n')


class SceneList(PywFile):
    """csv file representation of an yWriter project's scenes table. 

    Represents a csv file with a record per scene.
    * Records are separated by line breaks.
    * Data fields are delimited by the SEPARATOR character.
    """

    _FILE_EXTENSION = 'csv'
    # overwrites PywFile._FILE_EXTENSION

    def read(self) -> str:
        """Parse the csv file located at filePath, 
        fetching the Scene attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        try:
            with open(self._filePath, 'r', encoding='utf-8') as f:
                table = (f.readlines())

        except(FileNotFoundError):
            return 'ERROR: "' + self._filePath + '" not found.'

        if table[0] != TABLE_HEADER:
            return 'ERROR: Wrong table content.'

        fieldsInRecord = len(TABLE_HEADER.split(SEPARATOR))

        for record in table:
            field = record.split(SEPARATOR)

            if len(field) != fieldsInRecord:
                return 'ERROR: Wrong field structure.'

            if 'ScID:' in field[0]:
                scId = re.search('ScID\:([0-9]+)', field[0]).group(1)
                self.scenes[scId] = Scene()
                self.scenes[scId].title = field[1]
                self.scenes[scId].summary = field[2].replace(LINEBREAK, '\n')
                #self.scenes[scId].wordCount = int(field[3])
                #self.scenes[scId].letterCount = int(field[4])
                self.scenes[scId].tags = field[5].split(';')
                self.scenes[scId].sceneNotes = field[6].replace(
                    LINEBREAK, '\n')

        return 'SUCCESS: Data read from "' + self._filePath + '".'

    def write(self, novel: Novel) -> str:
        """Generate a csv file containing per scene:
        - A manuscript scene hyperlink, 
        - scene title,
        - scene summary, 
        - scene word count, 
        - scene letter count,
        - scene tags.
        Return a message beginning with SUCCESS or ERROR.
        """

        # Copy the scene's attributes to write

        if novel.srtChapters != []:
            self.srtChapters = novel.srtChapters

        if novel.scenes is not None:
            self.scenes = novel.scenes

        if novel.chapters is not None:
            self.chapters = novel.chapters

        odtPath = os.path.realpath(self.filePath).replace('\\', '/').replace(
            ' ', '%20').replace('_scenes.csv', '_manuscript.odt')

        # first record: the table's column headings

        table = [TABLE_HEADER]

        # Add a record for each used scene in a regular chapter

        for chId in self.srtChapters:

            if (not self.chapters[chId].isUnused) and self.chapters[chId].chType == 0:

                for scId in self.chapters[chId].srtScenes:

                    if not self.scenes[scId].isUnused:

                        if self.scenes[scId].summary is not None:
                            sceneSummary = self.scenes[scId].summary.rstrip(
                            ).replace('\n', LINEBREAK)

                        else:
                            sceneSummary = ''

                        sceneTags = self.scenes[scId].tags

                        if sceneTags is None:
                            sceneTags = ['']

                        if self.scenes[scId].sceneNotes is not None:
                            sceneNotes = self.scenes[scId].sceneNotes.rstrip(
                            ).replace('\n', LINEBREAK)

                        else:
                            sceneNotes = ''

                        table.append('=HYPERLINK("file:///'
                                     + odtPath + '#ScID:' + scId + '";"ScID:' + scId + '")'
                                     + SEPARATOR
                                     + self.scenes[scId].title
                                     + SEPARATOR
                                     + sceneSummary
                                     + SEPARATOR
                                     + str(self.scenes[scId].wordCount)
                                     + SEPARATOR
                                     + str(self.scenes[scId].letterCount)
                                     + SEPARATOR
                                     + ';'.join(sceneTags)
                                     + SEPARATOR
                                     + sceneNotes
                                     + '\n')

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.writelines(table)

        except(PermissionError):
            return 'ERROR: ' + self._filePath + '" is write protected.'

        return 'SUCCESS: "' + self._filePath + '" saved.'

    def get_structure(self) -> None:
        """This file format has no comparable structure."""
        return None