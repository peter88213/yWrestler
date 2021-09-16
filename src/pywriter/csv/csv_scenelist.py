"""Provide a class for csv scene list import.

Copyright (c) 2021 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import re
import os

from pywriter.csv.csv_file import CsvFile
from pywriter.model.scene import Scene


class CsvSceneList(CsvFile):
    """csv file representation of an yWriter project's scenes table. 
    """

    DESCRIPTION = 'Scene list'
    SUFFIX = '_scenelist'

    _SCENE_RATINGS = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
    # '1' is assigned N/A (empty table cell).

    rowTitles = ['Scene link', 'Scene title', 'Scene description', 'Tags', 'Scene notes', 'A/R',
                 'Goal', 'Conflict', 'Outcome', 'Scene', 'Words total',
                 '$FieldTitle1', '$FieldTitle2', '$FieldTitle3', '$FieldTitle4',
                 'Word count', 'Letter count', 'Status', 'Characters', 'Locations', 'Items']

    def read(self):
        """Parse the csv file located at filePath, 
        fetching the Scene attributes contained.
        Return a message beginning with SUCCESS or ERROR.
        """
        message = CsvFile.read(self)

        if message.startswith('ERROR'):
            return message

        for cells in self.rows:
            i = 0

            if 'ScID:' in cells[i]:
                scId = re.search('ScID\:([0-9]+)', cells[0]).group(1)
                self.scenes[scId] = Scene()
                i += 1
                self.scenes[scId].title = cells[i]
                i += 1
                self.scenes[scId].desc = self.convert_to_yw(cells[i])
                i += 1
                self.scenes[scId].tags = self.get_list(cells[i])
                i += 1
                self.scenes[scId].sceneNotes = self.convert_to_yw(cells[i])
                i += 1

                if Scene.REACTION_MARKER.lower() in cells[i].lower():
                    self.scenes[scId].isReactionScene = True

                else:
                    self.scenes[scId].isReactionScene = False

                i += 1
                self.scenes[scId].goal = cells[i]
                i += 1
                self.scenes[scId].conflict = cells[i]
                i += 1
                self.scenes[scId].outcome = cells[i]
                i += 1
                # Don't write back sceneCount
                i += 1
                # Don't write back wordCount
                i += 1

                # Transfer scene ratings; set to 1 if deleted

                if cells[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field1 = cells[i]

                else:
                    self.scenes[scId].field1 = '1'

                i += 1

                if cells[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field2 = cells[i]

                else:
                    self.scenes[scId].field2 = '1'

                i += 1

                if cells[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field3 = cells[i]

                else:
                    self.scenes[scId].field3 = '1'

                i += 1

                if cells[i] in self._SCENE_RATINGS:
                    self.scenes[scId].field4 = cells[i]

                else:
                    self.scenes[scId].field4 = '1'

                i += 1
                # Don't write back scene words total
                i += 1
                # Don't write back scene letters total
                i += 1

                try:
                    self.scenes[scId].status = Scene.STATUS.index(cells[i])

                except ValueError:
                    pass
                    # Scene status remains None and will be ignored when
                    # writing back.

                i += 1
                ''' Cannot write back character IDs, because self.characters is None
                charaNames = self.get_list(cells[i])
                self.scenes[scId].characters = []

                for charaName in charaNames:

                    for id, name in self.characters.items():

                        if name == charaName:
                            self.scenes[scId].characters.append(id)
                '''
                i += 1
                ''' Cannot write back location IDs, because self.locations is None
                locaNames = self.get_list(cells[i])
                self.scenes[scId].locations = []

                for locaName in locaNames:

                    for id, name in self.locations.items():

                        if name == locaName:
                            self.scenes[scId].locations.append(id)
                '''
                i += 1
                ''' Cannot write back item IDs, because self.items is None
                itemNames = self.get_list(cells[i])
                self.scenes[scId].items = []

                for itemName in itemNames:

                    for id, name in self.items.items():

                        if name == itemName:
                            self.scenes[scId].items.append(id)
                '''

        return 'SUCCESS: Data read from "' + os.path.normpath(self.filePath) + '".'
