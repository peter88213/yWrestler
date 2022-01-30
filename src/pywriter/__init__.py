"""The pywriter library - Convert yWriter projects

The system is based on the meta-model of a novel, which is also the basis of the yWriter novel writing 
application: 

There is a project tree that branches into chapters and scenes, plus other branches for documenting 
world-building elements such as characters, locations, and items. 

The root of this tree is represented by the Novel class in the 'model' package. This base class also 
contains some elementary methods for file operations. File format-specific subclasses are derived from 
this Novel superclass. For each file format there is a separate package in the pywriter library.

Modules:

pywriter_globals -- Provide global variables to be imported.

Packages:

converter -- Modules for conversion of Novel subclasses.
csv -- Modules for reading and writing csv spreadsheet documents.
file -- Shared modules for template-based document generation.
html -- Modules for reading html files.
model -- Modules for representation of yWriter's meta model.
odf -- Shared modules for writing Open Document files.
ods -- Modules for writing Open Document spreadsheet documents.
odt -- Modules for writing Open Document text documents.
ui -- Modules for user interfaces.
yw -- Modules for reading and writing yWriter project files.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
