"""SceneDesc - Class for html scenes file operations and parsing.

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import re
from pywriter.core.chapter import Chapter
from pywriter.edit.manuscript import Manuscript


STYLESHEET = '<style type="text/css">\n' + \
    'h1, h2, h3, h4, p {font: 1em monospace; margin: 3em; line-height: 1.5em}\n' + \
    'h1, h2, h3, h4 {text-align: center}\n' +\
    'h1 {letter-spacing: 0.5em; font-style: italic}' + \
    'h1, h2 {font-weight: bold}\n' + \
    'h3 {font-style: italic}\n' + \
    'p.textbody {margin-top:0; margin-bottom:0}\n' + \
    'p.firstlineindent {margin-top:0; margin-bottom:0; text-indent: 1em}\n' + \
    'strong {font-weight:normal; text-transform: uppercase}\n' + \
    '</style>\n'
# Make the generated html file look good in a web browser.

HTML_HEADER = '<html>\n' + '<head>\n' + \
    '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>\n' + \
    STYLESHEET + \
    '<title>$bookTitle$</title>\n' + \
    '</head>\n' + '<body>\n'

HTML_FOOTER = '\n</body>\n</html>\n'


class ChapterDesc(Manuscript):
    """HTML file representation of an yWriter project's scene descriptions part.

    Represents a html file with linkable chapter and scene sections 
    to be read and written by Open/LibreOffice Writer.

    # Attributes

    # Methods

    """

    def handle_starttag(self, tag, attrs):
        """HTML parser: Get chapter ID at chapter start. """

        if tag == 'div':
            if attrs[0][0] == 'id':
                if attrs[0][1].startswith('ChID'):
                    self.chID = re.search('[0-9]+', attrs[0][1]).group()
                    self.chapters[self.chID] = Chapter()
                    self.collectText = True

    def handle_endtag(self, tag):
        """HTML parser: Save chapter description in dictionary at chapter end. """

        if tag == 'div':
            self.chapters[self.chID].desc = self.text
            self.text = ''
            self.collectText = False

    def handle_data(self, data):
        """HTML parser: Collect paragraphs within scene. """

        if self.collectText:
            self.text = self.text + data + '\n'

    def write(self, novel) -> str:
        """Write attributes to html project file. """

        def format_yw7(text):
            """Convert yw7 raw markup """
            try:
                text = text.replace('\n\n', '\n')
                text = text.replace('\n', '</p>\n<p class="firstlineindent">')
            except:
                pass
            return(text)

        if novel.title is not None:
            if novel.title != '':
                self.title = novel.title

        if novel.chapters is not None:
            self.chapters = novel.chapters

        text = HTML_HEADER.replace('$bookTitle$', self.title)
        text = text + '<h1>' + self.title + '</h1>'
        for chID in self.chapters:
            text = text + '<div id="ChID:' + chID + '">\n'
            text = text + '<p class="firstlineindent">'
            try:
                entry = self.chapters[chID].desc
                if entry == '':
                    entry = self.chapters[chID].title
                else:
                    entry = format_yw7(entry)
                text = text + entry
            except(KeyError):
                pass
            text = text + '</p>\n'
            text = text + '</div>\n'

        text = text + HTML_FOOTER

        try:
            with open(self._filePath, 'w', encoding='utf-8') as f:
                f.write(text)
                # get_text() is to be overwritten
                # by file format specific subclasses.
        except(PermissionError):
            return('ERROR: ' + self._filePath + '" is write protected.')

        return('SUCCESS: "' + self._filePath + '" saved.')