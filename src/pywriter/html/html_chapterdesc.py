"""Provide a class for html invisibly tagged chapter descriptions import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

from pywriter.html.html_file import HtmlFile


class HtmlChapterDesc(HtmlFile):
    """HTML chapter summaries file representation.

    Import a brief synopsis with invisibly tagged chapter descriptions.
    """

    DESCRIPTION = 'Chapter descriptions'
    SUFFIX = '_chapters'

    def handle_endtag(self, tag):
        """Recognize the end of the chapter section and save data.
        Override HTMLparser.handle_endtag().
        """
        if self._chId is not None:

            if tag == 'div':
                self.chapters[self._chId].desc = ''.join(self._lines)
                self._lines = []
                self._chId = None

            elif tag == 'p':
                self._lines.append('\n')

            elif tag == 'h1' or tag == 'h2':

                if not self.chapters[self._chId].title:
                    self.chapters[self._chId].title = ''.join(self._lines)
                    self._lines = []

    def handle_data(self, data):
        """collect data within chapter sections.
        Override HTMLparser.handle_data().
        """
        if self._chId is not None:
            self._lines.append(data.rstrip().lstrip())
