"""Provide a class for html invisibly tagged scene descriptions import.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.html.html_file import HtmlFile


class HtmlSceneDesc(HtmlFile):
    """HTML scene summaries file representation.

    Import a full synopsis with invisibly tagged scene descriptions.
    """

    DESCRIPTION = 'Scene descriptions'
    SUFFIX = '_scenes'

    def handle_endtag(self, tag):
        """Recognize the end of the scene section and save data.
        Overwrites HTMLparser.handle_endtag().
        """
        if self._scId is not None:

            if tag == 'div':
                self.scenes[self._scId].desc = ''.join(self._lines)
                self._lines = []
                self._scId = None

            elif tag == 'p':
                self._lines.append('\n')

        elif self._chId is not None:

            if tag == 'div':
                self._chId = None

    def handle_data(self, data):
        """Collect data within scene sections.
        Overwrites HTMLparser.handle_data().
        """
        if self._scId is not None:
            self._lines.append(data.rstrip().lstrip())
