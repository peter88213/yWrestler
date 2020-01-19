"""Integration tests for the pyWriter project.

Test the collection read and write tasks.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os
import unittest

from pywriter.model.collection import Collection

from pywriter.model.mdfile import MdFile
from distutils.tests.test_text_file import TEST_DATA


TEST_PATH = os.getcwd()
EXEC_PATH = 'yw7/'
DATA_PATH = 'data/collection/'

TEST_FILE = EXEC_PATH + 'collection.pwc'


def read_file(inputFile):
    with open(inputFile, 'r', encoding='utf-8') as f:
        return(f.read())


def copy_file(inputFile, outputFile):
    with open(inputFile, 'rb') as f:
        myData = f.read()
    with open(outputFile, 'wb') as f:
        f.write(myData)
    return()


def remove_all_testfiles():
    try:
        os.remove(TEST_FILE)
    except:
        pass


class NrmOpr(unittest.TestCase):
    """Test case: Normal operation
    """

    def setUp(self):
        remove_all_testfiles()

        try:
            os.mkdir('yw7/yWriter Projects')
        except:
            pass
        try:
            os.mkdir('yw7\yWriter Projects/The Gravity Monster.yw')
        except:
            pass
        copy_file('data/yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7',
                  'yw7/yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7')
        try:
            os.mkdir('yw7\yWriter Projects/The Refugee Ship.yw')
        except:
            pass
        copy_file('data/yWriter Projects/The Refugee Ship.yw/The Refugee Ship.yw7',
                  'yw7/yWriter Projects/The Refugee Ship.yw/The Refugee Ship.yw7')

    def test_read_write_configuration(self):
        """Read and write the configuration file. """
        copy_file('data/collection/read_write.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()
        os.remove(TEST_FILE)
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/read_write.xml'))

    def test_create_collection(self):
        """Use Case: Create the collection."""
        myCollection = Collection(TEST_FILE)
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/create_collection.xml'))

    def test_add_remove_book(self):
        """Use Case: Create the collection."""

        copy_file(DATA_PATH + 'create_collection.xml', TEST_FILE)
        myCollection = Collection(TEST_FILE)
        myCollection.read()

        myCollection.add_book(
            'yw7\yWriter Projects/The Gravity Monster.yw/The Gravity Monster.yw7')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/add_first_book.xml'))

        myCollection.add_book(
            'yw7\yWriter Projects/The Refugee Ship.yw/The Refugee Ship.yw7')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/add_second_book.xml'))

        myCollection.remove_book('1')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/remove_book.xml'))

        myCollection.remove_book('2')
        myCollection.write()
        self.assertEqual(read_file(TEST_FILE),
                         read_file('data/collection/empty_series.xml'))


def main():
    unittest.main()


if __name__ == '__main__':
    main()
