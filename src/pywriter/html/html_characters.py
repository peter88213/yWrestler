"""Provide a class for html invisibly tagged character descriptions import.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re

from pywriter.model.character import Character
from pywriter.html.html_file import HtmlFile


class HtmlCharacters(HtmlFile):
    """HTML character descriptions file representation.

    Import a character sheet with invisibly tagged descriptions.
    """

    DESCRIPTION = 'Character descriptions'
    SUFFIX = '_characters'

    def __init__(self, filePath, **kwargs):
        HtmlFile.__init__(self, filePath)
        self._crId = None
        self._section = None

    def handle_starttag(self, tag, attrs):
        """Identify characters with subsections.
        Overwrites HTMLparser.handle_starttag()
        """
        if tag == 'div':

            if attrs[0][0] == 'id':

                if attrs[0][1].startswith('CrID_desc'):
                    self._crId = re.search('[0-9]+', attrs[0][1]).group()
                    self.srtCharacters.append(self._crId)
                    self.characters[self._crId] = Character()
                    self._section = 'desc'

                elif attrs[0][1].startswith('CrID_bio'):
                    self._section = 'bio'

                elif attrs[0][1].startswith('CrID_goals'):
                    self._section = 'goals'

                elif attrs[0][1].startswith('CrID_notes'):
                    self._section = 'notes'

    def handle_endtag(self, tag):
        """Recognize the end of the character section and save data.
        Overwrites HTMLparser.handle_endtag().
        """
        if self._crId is not None:

            if tag == 'div':

                if self._section == 'desc':
                    self.characters[self._crId].desc = ''.join(self._lines)
                    self._lines = []
                    self._section = None

                elif self._section == 'bio':
                    self.characters[self._crId].bio = ''.join(self._lines)
                    self._lines = []
                    self._section = None

                elif self._section == 'goals':
                    self.characters[self._crId].goals = ''.join(self._lines)
                    self._lines = []
                    self._section = None

                elif self._section == 'notes':
                    self.characters[self._crId].notes = ''.join(self._lines)
                    self._lines = []
                    self._section = None

            elif tag == 'p':
                self._lines.append('\n')

    def handle_data(self, data):
        """collect data within character sections.
        Overwrites HTMLparser.handle_data().
        """
        if self._section is not None:
            self._lines.append(data.rstrip().lstrip())
