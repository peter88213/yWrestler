"""HtmlImport - Class for html import file parsing.

Part of the PyWriter project.
Copyright (c) 2020, peter88213
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
from html import unescape

from pywriter.html.html_manuscript import HtmlManuscript
from pywriter.html.html_form import *


class HtmlImport(HtmlManuscript):
    """HTML file representation of an yWriter project's OfficeFile part.

    Represents a html file without chapter and scene tags 
    to be written by Open/LibreOffice Writer.
    """

    def read(self):
        """Parse a HTML file and insert chapter and scene sections.
        Read scene contents.
        Return a message beginning with SUCCESS or ERROR. 
        """
        _TEXT_END_TAGS = ['<div type=footer>', '/body']
        _SCENE_DIVIDER = '* * *'
        _LOW_WORDCOUNT = 10

        _SC_DESC_OPEN = '{_'
        _SC_DESC_CLOSE = '_}'
        _CH_DESC_OPEN = '{#'
        _CH_DESC_CLOSE = '#}'

        result = read_html_file(self._filePath)

        if result[0].startswith('ERROR'):
            return (result[0])

        # Insert chapter and scene markers in html text.

        lines = result[1].split('\n')
        newlines = []
        chCount = 0     # overall chapter count
        scCount = 0     # overall scene count
        inBody = False
        contentFinished = False
        inSceneSection = False
        inSceneDescription = False
        inChapterDescription = False

        chapterTitles = {}
        sceneTitles = {}
        chapterDescs = {}
        sceneDescs = {}
        chapterLevels = {}

        tagRegEx = re.compile(r'(<!--.*?-->|<[^>]*>)')
        desc = ''

        for line in lines:

            if contentFinished:
                break

            line = line.rstrip().lstrip()
            scan = line.lower()

            if '<h1' in scan or '<h2' in scan:

                if inSceneDescription or inChapterDescription:
                    return 'ERROR: Wrong description tags in Chapter #' + str(chCount)

                inBody = True
                chCount += 1

                if '<h1' in scan:
                    # line contains the start of a part heading
                    chapterLevels[str(chCount)] = 1

                else:
                    # line contains the start of a chapter heading
                    chapterLevels[str(chCount)] = 0

                if inSceneSection:
                    newlines.append('</DIV>')
                    # close the leading scene section
                    inSceneSection = False

                if chCount > 0:
                    newlines.append('</DIV>')
                    # close the leading chapter section

                m = re.match('.+?>(.+?)</[h,H][1,2]>', line)

                if m is not None:
                    chapterTitles[str(chCount)] = m.group(1)

                else:
                    chapterTitles[str(chCount)] = 'Chapter' + str(chCount)

                newlines.append('<DIV ID="ChID:' + str(chCount) + '">')
                # open the next chapter section

            elif _SCENE_DIVIDER in scan or '<h3' in scan:

                if inSceneDescription or inChapterDescription:
                    return 'ERROR: Wrong description tags in Chapter #' + str(chCount)

                if inSceneSection:
                    newlines.append('</DIV>')
                    # close the leading scene section

                scCount += 1
                m = re.match('.+?>(.+?)</[h,H]3>', line)

                if m is not None:
                    sceneTitles[str(scCount)] = m.group(1)

                else:
                    sceneTitles[str(scCount)] = 'Scene ' + str(scCount)

                newlines.append('<DIV ID="ScID:' + str(scCount) + '">')
                # open the next scene section
                inSceneSection = True

            elif inBody and '<p' in scan:

                if inChapterDescription or _CH_DESC_OPEN in scan:

                    if desc != '':
                        desc += '\n'

                    desc += unescape(tagRegEx.sub('', line).replace(
                        _CH_DESC_OPEN, '').replace(_CH_DESC_CLOSE, ''))

                    if _CH_DESC_CLOSE in scan:
                        chapterDescs[str(chCount)] = desc
                        desc = ''
                        inChapterDescription = False

                    else:
                        inChapterDescription = True

                elif chCount > 0 and not inSceneSection:
                    scCount += 1
                    sceneTitles[str(scCount)] = 'Scene ' + str(scCount)
                    newlines.append('<DIV ID="ScID:' + str(scCount) + '">')
                    # open the chapter's first scene section
                    inSceneSection = True

                    if _SC_DESC_OPEN in scan:

                        desc += unescape(tagRegEx.sub('', line).replace(
                            _SC_DESC_OPEN, '').replace(_SC_DESC_CLOSE, ''))

                        if _SC_DESC_CLOSE in scan:
                            sceneDescs[str(scCount)] = desc
                            desc = ''

                        else:
                            inSceneDescription = True

                    else:
                        newlines.append(line)

                elif inSceneDescription or _SC_DESC_OPEN in scan:

                    if desc != '':
                        desc += '\n'

                    desc += unescape(tagRegEx.sub('', line).replace(
                        _SC_DESC_OPEN, '').replace(_SC_DESC_CLOSE, ''))

                    if _SC_DESC_CLOSE in scan:
                        sceneDescs[str(scCount)] = desc
                        desc = ''
                        inSceneDescription = False

                    else:
                        inSceneDescription = True

                else:
                    newlines.append(line)

            elif inChapterDescription:
                desc += '\n' + unescape(tagRegEx.sub('', line).replace(
                        _CH_DESC_OPEN, '').replace(_CH_DESC_CLOSE, ''))

                if _CH_DESC_CLOSE in scan:
                    chapterDescs[str(chCount)] = desc
                    desc = ''
                    inChapterDescription = False

            elif inSceneDescription:
                desc += '\n' + unescape(tagRegEx.sub('', line).replace(
                        _SC_DESC_OPEN, '').replace(_SC_DESC_CLOSE, ''))

                if _SC_DESC_CLOSE in scan:
                    sceneDescs[str(scCount)] = desc
                    desc = ''
                    inSceneDescription = False

            else:
                for marker in _TEXT_END_TAGS:

                    if marker in scan:
                        # line contains the content closing marker

                        if inSceneSection:
                            newlines.append('</DIV>')
                            # close the last scene section
                            inSceneSection = False

                        if chCount > 0:
                            newlines.append('</DIV>')
                            # close the last chapter section

                        contentFinished = True
                        break

                if not contentFinished:
                    newlines.append(line)

        text = '\n'.join(newlines)
        text = to_yw7(text)

        # Invoke HTML parser.

        self.feed(text)

        for scId in self.scenes:
            self.scenes[scId].title = sceneTitles[scId]

            if scId in sceneDescs:
                self.scenes[scId].desc = sceneDescs[scId]

            if self.scenes[scId].wordCount < _LOW_WORDCOUNT:
                self.scenes[scId].status = 1

            else:
                self.scenes[scId].status = 2

        for chId in self.chapters:
            self.chapters[chId].title = chapterTitles[chId]
            self.chapters[chId].chLevel = chapterLevels[chId]
            self.chapters[chId].type = 0
            self.chapters[chId].suppressChapterTitle = True

            if chId in chapterDescs:
                self.chapters[chId].desc = chapterDescs[chId]

        return 'SUCCESS: ' + str(len(self.scenes)) + ' Scenes read from "' + self._filePath + '".'
