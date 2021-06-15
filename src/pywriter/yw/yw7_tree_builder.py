"""Provide a strategy class to build an yWriter 7 xml tree.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import xml.etree.ElementTree as ET


class Yw7TreeBuilder():
    """Build yWriter 7 project xml tree."""

    TAG = 'YWRITER7'
    VER = '7'

    def put_scene_contents(self, ywProject):
        """Modify the scene contents of an existing xml element tree.
        Return a message beginning with SUCCESS or ERROR.
        Strategy method for the yw7 file format variant.
        """

        root = ywProject.tree.getroot()

        for scn in root.iter('SCENE'):
            scId = scn.find('ID').text

            if ywProject.scenes[scId].sceneContent is not None:
                scn.find(
                    'SceneContent').text = ywProject.scenes[scId].sceneContent
                scn.find('WordCount').text = str(
                    ywProject.scenes[scId].wordCount)
                scn.find('LetterCount').text = str(
                    ywProject.scenes[scId].letterCount)

            try:
                scn.remove(scn.find('RTFFile'))

            except:
                pass

        return 'SUCCESS'

    def build_element_tree(self, ywProject):
        """Modify the yWriter project attributes of an existing xml element tree.
        Return a message beginning with SUCCESS or ERROR.
        """

        def create_scene_subtree(xmlScn, prjScn):
            ET.SubElement(xmlScn, 'ID').text = scId

            if prjScn.title is not None:
                ET.SubElement(
                    xmlScn, 'Title').text = prjScn.title

            for chId in ywProject.chapters:

                if scId in ywProject.chapters[chId].srtScenes:
                    ET.SubElement(xmlScn, 'BelongsToChID').text = chId
                    break

            if prjScn.desc is not None:
                ET.SubElement(
                    xmlScn, 'Desc').text = prjScn.desc

            if prjScn.sceneContent is not None:
                ET.SubElement(xmlScn,
                              'SceneContent').text = prjScn.sceneContent
                ET.SubElement(xmlScn, 'WordCount').text = str(
                    prjScn.wordCount)
                ET.SubElement(xmlScn, 'LetterCount').text = str(
                    prjScn.letterCount)

            if prjScn.isUnused:
                ET.SubElement(xmlScn, 'Unused').text = '-1'

            scFields = ET.SubElement(xmlScn, 'Fields')

            if prjScn.isNotesScene:
                ET.SubElement(scFields, 'Field_SceneType').text = '1'

            elif prjScn.isTodoScene:
                ET.SubElement(scFields, 'Field_SceneType').text = '2'

            if prjScn.status is not None:
                ET.SubElement(xmlScn, 'Status').text = str(
                    prjScn.status)

            if prjScn.sceneNotes is not None:
                ET.SubElement(
                    xmlScn, 'Notes').text = prjScn.sceneNotes

            if prjScn.tags is not None:
                ET.SubElement(xmlScn, 'Tags').text = ';'.join(
                    prjScn.tags)

            if prjScn.field1 is not None:
                ET.SubElement(
                    xmlScn, 'Field1').text = prjScn.field1

            if prjScn.field2 is not None:
                ET.SubElement(
                    xmlScn, 'Field2').text = prjScn.field2

            if prjScn.field3 is not None:
                ET.SubElement(
                    xmlScn, 'Field3').text = prjScn.field3

            if prjScn.field4 is not None:
                ET.SubElement(
                    xmlScn, 'Field4').text = prjScn.field4

            if prjScn.appendToPrev:
                ET.SubElement(xmlScn, 'AppendToPrev').text = '-1'

            # Date/time information

            if (prjScn.date is not None) and (prjScn.time is not None):
                dateTime = ' '.join(
                    prjScn.date, prjScn.time)
                ET.SubElement(xmlScn, 'SpecificDateTime').text = dateTime
                ET.SubElement(xmlScn, 'SpecificDateMode').text = '-1'

            elif (prjScn.day is not None) or (prjScn.hour is not None) or (prjScn.minute is not None):

                if prjScn.day is not None:
                    ET.SubElement(
                        xmlScn, 'Day').text = prjScn.day

                if prjScn.hour is not None:
                    ET.SubElement(
                        xmlScn, 'Hour').text = prjScn.hour

                if prjScn.minute is not None:
                    ET.SubElement(
                        xmlScn, 'Minute').text = prjScn.minute

            if prjScn.lastsDays is not None:
                ET.SubElement(
                    xmlScn, 'LastsDays').text = prjScn.lastsDays

            if prjScn.lastsHours is not None:
                ET.SubElement(
                    xmlScn, 'LastsHours').text = prjScn.lastsHours

            if prjScn.lastsMinutes is not None:
                ET.SubElement(
                    xmlScn, 'LastsMinutes').text = prjScn.lastsMinutes

            # Plot related information

            if prjScn.isReactionScene:
                ET.SubElement(xmlScn, 'ReactionScene').text = '-1'

            if prjScn.isSubPlot:
                ET.SubElement(xmlScn, 'SubPlot').text = '-1'

            if prjScn.goal is not None:
                ET.SubElement(
                    xmlScn, 'Goal').text = prjScn.goal

            if prjScn.conflict is not None:
                ET.SubElement(
                    xmlScn, 'Conflict').text = prjScn.conflict

            if prjScn.outcome is not None:
                ET.SubElement(
                    xmlScn, 'Outcome').text = prjScn.outcome

            if prjScn.characters is not None:
                scCharacters = ET.SubElement(xmlScn, 'Characters')

                for crId in prjScn.characters:
                    ET.SubElement(scCharacters, 'CharID').text = crId

            if prjScn.locations is not None:
                scLocations = ET.SubElement(xmlScn, 'Locations')

                for lcId in prjScn.locations:
                    ET.SubElement(scLocations, 'LocID').text = lcId

            if prjScn.items is not None:
                scItems = ET.SubElement(xmlScn, 'Items')

                for itId in prjScn.items:
                    ET.SubElement(scItems, 'ItemID').text = itId

        def modify_scene_subtree(xmlScn, prjScn):

            if prjScn.title is not None:

                if xmlScn.find('Title') is not None:
                    xmlScn.find('Title').text = prjScn.title

                else:
                    ET.SubElement(
                        xmlScn, 'Title').text = prjScn.title

            if prjScn.desc is not None:

                if xmlScn.find('Desc') is None:
                    ET.SubElement(
                        xmlScn, 'Desc').text = prjScn.desc

                else:
                    xmlScn.find('Desc').text = prjScn.desc

            # Scene content is written in subclasses.

            if prjScn.isUnused:

                if xmlScn.find('Unused') is None:
                    ET.SubElement(xmlScn, 'Unused').text = '-1'

            elif xmlScn.find('Unused') is not None:
                xmlScn.remove(xmlScn.find('Unused'))

            if prjScn.isNotesScene:

                if xmlScn.find('Fields') is None:
                    scFields = ET.SubElement(xmlScn, 'Fields')

                else:
                    scFields = xmlScn.find('Fields')

                if scFields.find('Field_SceneType') is None:
                    ET.SubElement(scFields, 'Field_SceneType').text = '1'

            elif xmlScn.find('Fields') is not None:
                scFields = xmlScn.find('Fields')

                if scFields.find('Field_SceneType') is not None:

                    if scFields.find('Field_SceneType').text == '1':
                        scFields.remove(scFields.find('Field_SceneType'))

            if prjScn.isTodoScene:

                if xmlScn.find('Fields') is None:
                    scFields = ET.SubElement(xmlScn, 'Fields')

                else:
                    scFields = xmlScn.find('Fields')

                if scFields.find('Field_SceneType') is None:
                    ET.SubElement(scFields, 'Field_SceneType').text = '2'

            elif xmlScn.find('Fields') is not None:
                scFields = xmlScn.find('Fields')

                if scFields.find('Field_SceneType') is not None:

                    if scFields.find('Field_SceneType').text == '2':
                        scFields.remove(scFields.find('Field_SceneType'))

            if prjScn.status is not None:
                xmlScn.find('Status').text = str(
                    prjScn.status)

            if prjScn.sceneNotes is not None:

                if xmlScn.find('Notes') is None:
                    ET.SubElement(
                        xmlScn, 'Notes').text = prjScn.sceneNotes

                else:
                    xmlScn.find(
                        'Notes').text = prjScn.sceneNotes

            if prjScn.tags is not None:

                if xmlScn.find('Tags') is None:
                    ET.SubElement(xmlScn, 'Tags').text = ';'.join(
                        prjScn.tags)

                else:
                    xmlScn.find('Tags').text = ';'.join(
                        prjScn.tags)

            if prjScn.field1 is not None:

                if xmlScn.find('Field1') is None:
                    ET.SubElement(
                        xmlScn, 'Field1').text = prjScn.field1

                else:
                    xmlScn.find('Field1').text = prjScn.field1

            if prjScn.field2 is not None:

                if xmlScn.find('Field2') is None:
                    ET.SubElement(
                        xmlScn, 'Field2').text = prjScn.field2

                else:
                    xmlScn.find('Field2').text = prjScn.field2

            if prjScn.field3 is not None:

                if xmlScn.find('Field3') is None:
                    ET.SubElement(
                        xmlScn, 'Field3').text = prjScn.field3

                else:
                    xmlScn.find('Field3').text = prjScn.field3

            if prjScn.field4 is not None:

                if xmlScn.find('Field4') is None:
                    ET.SubElement(
                        xmlScn, 'Field4').text = prjScn.field4

                else:
                    xmlScn.find('Field4').text = prjScn.field4

            if prjScn.appendToPrev:

                if xmlScn.find('AppendToPrev') is None:
                    ET.SubElement(xmlScn, 'AppendToPrev').text = '-1'

            elif xmlScn.find('AppendToPrev') is not None:
                xmlScn.remove(xmlScn.find('AppendToPrev'))

            # Date/time information

            if (prjScn.date is not None) and (prjScn.time is not None):
                dateTime = prjScn.date + \
                    ' ' + prjScn.time

                if xmlScn.find('SpecificDateTime') is not None:
                    xmlScn.find('SpecificDateTime').text = dateTime

                else:
                    ET.SubElement(xmlScn, 'SpecificDateTime').text = dateTime
                    ET.SubElement(xmlScn, 'SpecificDateMode').text = '-1'

                    if xmlScn.find('Day') is not None:
                        xmlScn.remove(xmlScn.find('Day'))

                    if xmlScn.find('Hour') is not None:
                        xmlScn.remove(xmlScn.find('Hour'))

                    if xmlScn.find('Minute') is not None:
                        xmlScn.remove(xmlScn.find('Minute'))

            elif (prjScn.day is not None) or (prjScn.hour is not None) or (prjScn.minute is not None):

                if xmlScn.find('SpecificDateTime') is not None:
                    xmlScn.remove(xmlScn.find('SpecificDateTime'))

                if xmlScn.find('SpecificDateMode') is not None:
                    xmlScn.remove(xmlScn.find('SpecificDateMode'))

                if prjScn.day is not None:

                    if xmlScn.find('Day') is not None:
                        xmlScn.find('Day').text = prjScn.day

                    else:
                        ET.SubElement(
                            xmlScn, 'Day').text = prjScn.day

                if prjScn.hour is not None:

                    if xmlScn.find('Hour') is not None:
                        xmlScn.find('Hour').text = prjScn.hour

                    else:
                        ET.SubElement(
                            xmlScn, 'Hour').text = prjScn.hour

                if prjScn.minute is not None:

                    if xmlScn.find('Minute') is not None:
                        xmlScn.find(
                            'Minute').text = prjScn.minute

                    else:
                        ET.SubElement(
                            xmlScn, 'Minute').text = prjScn.minute

            if prjScn.lastsDays is not None:

                if xmlScn.find('LastsDays') is not None:
                    xmlScn.find(
                        'LastsDays').text = prjScn.lastsDays

                else:
                    ET.SubElement(
                        xmlScn, 'LastsDays').text = prjScn.lastsDays

            if prjScn.lastsHours is not None:

                if xmlScn.find('LastsHours') is not None:
                    xmlScn.find(
                        'LastsHours').text = prjScn.lastsHours

                else:
                    ET.SubElement(
                        xmlScn, 'LastsHours').text = prjScn.lastsHours

            if prjScn.lastsMinutes is not None:

                if xmlScn.find('LastsMinutes') is not None:
                    xmlScn.find(
                        'LastsMinutes').text = prjScn.lastsMinutes

                else:
                    ET.SubElement(
                        xmlScn, 'LastsMinutes').text = prjScn.lastsMinutes

            # Plot related information

            if prjScn.isReactionScene:

                if xmlScn.find('ReactionScene') is None:
                    ET.SubElement(xmlScn, 'ReactionScene').text = '-1'

            elif xmlScn.find('ReactionScene') is not None:
                xmlScn.remove(xmlScn.find('ReactionScene'))

            if prjScn.isSubPlot:

                if xmlScn.find('SubPlot') is None:
                    ET.SubElement(xmlScn, 'SubPlot').text = '-1'

            elif xmlScn.find('SubPlot') is not None:
                xmlScn.remove(xmlScn.find('SubPlot'))

            if prjScn.goal is not None:

                if xmlScn.find('Goal') is None:
                    ET.SubElement(
                        xmlScn, 'Goal').text = prjScn.goal

                else:
                    xmlScn.find('Goal').text = prjScn.goal

            if prjScn.conflict is not None:

                if xmlScn.find('Conflict') is None:
                    ET.SubElement(
                        xmlScn, 'Conflict').text = prjScn.conflict

                else:
                    xmlScn.find(
                        'Conflict').text = prjScn.conflict

            if prjScn.outcome is not None:

                if xmlScn.find('Outcome') is None:
                    ET.SubElement(
                        xmlScn, 'Outcome').text = prjScn.outcome

                else:
                    xmlScn.find(
                        'Outcome').text = prjScn.outcome

            if prjScn.characters is not None:
                characters = xmlScn.find('Characters')

                for oldCrId in characters.findall('CharID'):
                    characters.remove(oldCrId)

                for crId in prjScn.characters:
                    ET.SubElement(characters, 'CharID').text = crId

            if prjScn.locations is not None:
                locations = xmlScn.find('Locations')

                for oldLcId in locations.findall('LocID'):
                    locations.remove(oldLcId)

                for lcId in prjScn.locations:
                    ET.SubElement(locations, 'LocID').text = lcId

            if prjScn.items is not None:
                items = xmlScn.find('Items')

                for oldItId in items.findall('ItemID'):
                    items.remove(oldItId)

                for itId in prjScn.items:
                    ET.SubElement(items, 'ItemID').text = itId

        def create_chapter_subtree(xmlChp, prjChp, sortOrder):
            ET.SubElement(xmlChp, 'ID').text = chId
            ET.SubElement(xmlChp, 'SortOrder').text = str(sortOrder)

            if prjChp.title is not None:
                ET.SubElement(
                    xmlChp, 'Title').text = prjChp.title

            if prjChp.desc is not None:
                ET.SubElement(
                    xmlChp, 'Desc').text = prjChp.desc

            if prjChp.chLevel == 1:
                ET.SubElement(xmlChp, 'SectionStart').text = '-1'

            if prjChp.oldType is not None:
                ET.SubElement(xmlChp, 'Type').text = str(
                    prjChp.oldType)

            if prjChp.chType is not None:
                ET.SubElement(xmlChp, 'ChapterType').text = str(
                    prjChp.chType)

            if prjChp.isUnused:
                ET.SubElement(xmlChp, 'Unused').text = '-1'

            sortSc = ET.SubElement(xmlChp, 'Scenes')

            for scId in prjChp.srtScenes:
                ET.SubElement(sortSc, 'ScID').text = scId

            chFields = ET.SubElement(xmlChp, 'Fields')

            if prjChp.title is not None:

                if prjChp.title.startswith('@'):
                    prjChp.suppressChapterTitle = True

            if prjChp.suppressChapterTitle:
                ET.SubElement(
                    chFields, 'Field_SuppressChapterTitle').text = '1'

        def modify_chapter_subtree(xmlChp, prjChp, sortOrder):

            if ywProject.chapters[chId] is not None:

                if xmlChp.find('SortOrder') is not None:
                    xmlChp.find('SortOrder').text = str(sortOrder)

                else:
                    ET.SubElement(xmlChp, 'SortOrder').text = str(sortOrder)

                if xmlChp.find('Title') is not None:
                    xmlChp.find('Title').text = prjChp.title

                else:
                    ET.SubElement(
                        xmlChp, 'Title').text = prjChp.title

            if prjChp.desc is not None:

                if xmlChp.find('Desc') is None:
                    ET.SubElement(
                        xmlChp, 'Desc').text = prjChp.desc

                else:
                    xmlChp.find('Desc').text = prjChp.desc

            levelInfo = xmlChp.find('SectionStart')

            if levelInfo is not None:

                if prjChp.chLevel == 0:
                    xmlChp.remove(levelInfo)

            xmlChp.find('Type').text = str(prjChp.oldType)

            if prjChp.chType is not None:

                if xmlChp.find('ChapterType') is not None:
                    xmlChp.find('ChapterType').text = str(
                        prjChp.chType)
                else:
                    ET.SubElement(xmlChp, 'ChapterType').text = str(
                        prjChp.chType)

            if prjChp.isUnused:

                if xmlChp.find('Unused') is None:
                    ET.SubElement(xmlChp, 'Unused').text = '-1'

            elif xmlChp.find('Unused') is not None:
                xmlChp.remove(xmlChp.find('Unused'))

        xmlScenes = {}
        xmlChapters = {}

        root = ywProject.tree.getroot()

        # Write attributes at scene level to the xml element tree.

        scenes = root.find('SCENES')

        # Save the original XML scene subtrees
        # and remove them from the project tree.

        for xmlScn in scenes.findall('SCENE'):
            scId = xmlScn.find('ID').text
            xmlScenes[scId] = xmlScn
            scenes.remove(xmlScn)

        # Add the new XML scene subtrees to the project tree.

        for scId in ywProject.scenes:

            if scId in xmlScenes:
                modify_scene_subtree(xmlScenes[scId], ywProject.scenes[scId])

            else:
                xmlScenes[scId] = ET.Element('SCENE')
                create_scene_subtree(xmlScenes[scId], ywProject.scenes[scId])

            scenes.append(xmlScenes[scId])

        # Write version-dependent scene contents to the xml element tree.

        message = self.put_scene_contents(ywProject)

        if message.startswith('ERROR'):
            return message

        # Write attributes at chapter level to the xml element tree.

        chapters = root.find('CHAPTERS')

        # Save the original XML chapter subtree
        # and remove it from the project tree.

        for xmlChp in chapters.findall('CHAPTER'):
            chId = xmlChp.find('ID').text
            xmlChapters[chId] = xmlChp
            chapters.remove(xmlChp)

        # Add the new XML chapter subtrees to the project tree.

        sortOrder = 0

        for chId in ywProject.chapters:
            sortOrder += 1

            if chId in xmlChapters:
                modify_chapter_subtree(
                    xmlChapters[chId], ywProject.chapters[chId], sortOrder)

            else:
                xmlChapters[chId] = ET.Element('CHAPTER')
                create_chapter_subtree(
                    xmlChapters[chId], ywProject.chapters[chId], sortOrder)

            chapters.append(xmlChapters[chId])

        # Write attributes at novel level to the xml element tree.

        prj = root.find('PROJECT')
        prj.find('Title').text = ywProject.title

        if ywProject.desc is not None:

            if prj.find('Desc') is None:
                ET.SubElement(prj, 'Desc').text = ywProject.desc

            else:
                prj.find('Desc').text = ywProject.desc

        if ywProject.author is not None:

            if prj.find('AuthorName') is None:
                ET.SubElement(prj, 'AuthorName').text = ywProject.author

            else:
                prj.find('AuthorName').text = ywProject.author

        prj.find('FieldTitle1').text = ywProject.fieldTitle1
        prj.find('FieldTitle2').text = ywProject.fieldTitle2
        prj.find('FieldTitle3').text = ywProject.fieldTitle3
        prj.find('FieldTitle4').text = ywProject.fieldTitle4

        locations = root.find('LOCATIONS')
        sortOrder = 0

        # Remove LOCATION entries in order to rewrite
        # the LOCATIONS section in a modified sort order.

        for loc in locations.findall('LOCATION'):
            locations.remove(loc)

        for lcId in ywProject.srtLocations:
            loc = ET.SubElement(locations, 'LOCATION')
            ET.SubElement(loc, 'ID').text = lcId

            if ywProject.locations[lcId].title is not None:
                ET.SubElement(
                    loc, 'Title').text = ywProject.locations[lcId].title

            if ywProject.locations[lcId].image is not None:
                ET.SubElement(
                    loc, 'ImageFile').text = ywProject.locations[lcId].image

            if ywProject.locations[lcId].desc is not None:
                ET.SubElement(
                    loc, 'Desc').text = ywProject.locations[lcId].desc

            if ywProject.locations[lcId].aka is not None:
                ET.SubElement(loc, 'AKA').text = ywProject.locations[lcId].aka

            if ywProject.locations[lcId].tags is not None:
                ET.SubElement(loc, 'Tags').text = ';'.join(
                    ywProject.locations[lcId].tags)

            sortOrder += 1
            ET.SubElement(loc, 'SortOrder').text = str(sortOrder)

        # Write items to the xml element tree.

        items = root.find('ITEMS')
        sortOrder = 0

        # Remove ITEM entries in order to rewrite
        # the ITEMS section in a modified sort order.

        for itm in items.findall('ITEM'):
            items.remove(itm)

        for itId in ywProject.srtItems:
            itm = ET.SubElement(items, 'ITEM')
            ET.SubElement(itm, 'ID').text = itId

            if ywProject.items[itId].title is not None:
                ET.SubElement(itm, 'Title').text = ywProject.items[itId].title

            if ywProject.items[itId].image is not None:
                ET.SubElement(
                    itm, 'ImageFile').text = ywProject.items[itId].image

            if ywProject.items[itId].desc is not None:
                ET.SubElement(itm, 'Desc').text = ywProject.items[itId].desc

            if ywProject.items[itId].aka is not None:
                ET.SubElement(itm, 'AKA').text = ywProject.items[itId].aka

            if ywProject.items[itId].tags is not None:
                ET.SubElement(itm, 'Tags').text = ';'.join(
                    ywProject.items[itId].tags)

            sortOrder += 1
            ET.SubElement(itm, 'SortOrder').text = str(sortOrder)

        # Write characters to the xml element tree.

        characters = root.find('CHARACTERS')
        sortOrder = 0

        # Remove CHARACTER entries in order to rewrite
        # the CHARACTERS section in a modified sort order.

        for crt in characters.findall('CHARACTER'):
            characters.remove(crt)

        for crId in ywProject.srtCharacters:
            crt = ET.SubElement(characters, 'CHARACTER')
            ET.SubElement(crt, 'ID').text = crId

            if ywProject.characters[crId].title is not None:
                ET.SubElement(
                    crt, 'Title').text = ywProject.characters[crId].title

            if ywProject.characters[crId].desc is not None:
                ET.SubElement(
                    crt, 'Desc').text = ywProject.characters[crId].desc

            if ywProject.characters[crId].image is not None:
                ET.SubElement(
                    crt, 'ImageFile').text = ywProject.characters[crId].image

            sortOrder += 1
            ET.SubElement(crt, 'SortOrder').text = str(sortOrder)

            if ywProject.characters[crId].notes is not None:
                ET.SubElement(
                    crt, 'Notes').text = ywProject.characters[crId].notes

            if ywProject.characters[crId].aka is not None:
                ET.SubElement(crt, 'AKA').text = ywProject.characters[crId].aka

            if ywProject.characters[crId].tags is not None:
                ET.SubElement(crt, 'Tags').text = ';'.join(
                    ywProject.characters[crId].tags)

            if ywProject.characters[crId].bio is not None:
                ET.SubElement(crt, 'Bio').text = ywProject.characters[crId].bio

            if ywProject.characters[crId].goals is not None:
                ET.SubElement(
                    crt, 'Goals').text = ywProject.characters[crId].goals

            if ywProject.characters[crId].fullName is not None:
                ET.SubElement(
                    crt, 'FullName').text = ywProject.characters[crId].fullName

            if ywProject.characters[crId].isMajor:
                ET.SubElement(crt, 'Major').text = '-1'

        self.indent_xml(root)
        ywProject.tree = ET.ElementTree(root)

        return 'SUCCESS'

    def indent_xml(self, elem, level=0):
        """xml pretty printer

        Kudos to to Fredrik Lundh. 
        Source: http://effbot.org/zone/element-lib.htm#prettyprint
        """
        i = "\n" + level * "  "

        if len(elem):

            if not elem.text or not elem.text.strip():
                elem.text = i + "  "

            if not elem.tail or not elem.tail.strip():
                elem.tail = i

            for elem in elem:
                self.indent_xml(elem, level + 1)

            if not elem.tail or not elem.tail.strip():
                elem.tail = i

        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
