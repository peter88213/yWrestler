""" Build python script for the LibreOffice "open yw7" script.
        
In order to distribute single scripts without dependencies, 
this script "inlines" all modules imported from the pywriter package.

For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import inliner

SRC = '../src/'
BUILD = '../build/'


def main():
    os.chdir(SRC)
    inliner.run('openyw7.py', BUILD + 'openyw7.py', 'pywriter')
    print('Done.')


if __name__ == '__main__':
    main()