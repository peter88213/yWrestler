"""Provide a class for csv character list import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re

from pywriter.pywriter_globals import ERROR
from pywriter.csv.csv_file import CsvFile
from pywriter.model.character import Character


class CsvCharList(CsvFile):
    """csv file representation of a yWriter project's characters table. 
    
    Public methods:
        read() -- parse the file and get the instance variables.
    """
    DESCRIPTION = 'Character list'
    SUFFIX = '_charlist'

    _rowTitles = ['ID', 'Name', 'Full name', 'Aka', 'Description', 'Bio', 'Goals', 'Importance', 'Tags', 'Notes']

    def read(self):
        """Parse the file and get the instance variables.
        
        Parse the csv file located at filePath, fetching the Character attributes contained.
        Return a message beginning with the ERROR constant in case of error.
        Extends the superclass method.
        """
        message = super().read()

        if message.startswith(ERROR):
            return message

        for cells in self._rows:

            if 'CrID:' in cells[0]:
                crId = re.search('CrID\:([0-9]+)', cells[0]).group(1)
                self.srtCharacters.append(crId)
                self.characters[crId] = Character()
                self.characters[crId].title = cells[1]
                self.characters[crId].fullName = cells[2]
                self.characters[crId].aka = cells[3]
                self.characters[crId].desc = self._convert_to_yw(cells[4])
                self.characters[crId].bio = cells[5]
                self.characters[crId].goals = cells[6]

                if Character.MAJOR_MARKER in cells[7]:
                    self.characters[crId].isMajor = True

                else:
                    self.characters[crId].isMajor = False

                self.characters[crId].tags = self._get_list(cells[8])
                self.characters[crId].notes = self._convert_to_yw(cells[9])

        return 'Character data read in.'
