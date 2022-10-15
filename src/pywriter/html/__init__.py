"""Package for reading html files.

The html format is mainly used to read text documents exported by Office 
applications like OpenOffice and LibreOffice. This is because the html format 
is much easier to parse than the odt format.

Modules:

html_chapterdesc -- Provide a class for html invisibly tagged chapter descriptions import.
html_characters -- Provide a class for html invisibly tagged character descriptions import.
html_file -- Provide a generic class for html file import.
html_fop -- Helper module for HTML file operations.
html_formatted -- Provide a base class for HTML documents containing text that is formatted in yWriter.
html_import -- Provide a class for html 'work in progress' import.
html_items -- Provide a class for html item invisibly tagged descriptions import.
html_locations -- Provide a class for html invisibly tagged location descriptions import.
html_manuscript -- Provide a class for html invisibly tagged chapters and scenes import.
html_notes -- Provide a class for html invisibly tagged "Notes" chapters import.
html_outline -- Provide a class for html outline import.
html_partdesc -- Provide a class for html invisibly tagged part descriptions import.
html_proof -- Provide a class for html visibly tagged chapters and scenes import.
html_scenedesc -- Provide a class for html invisibly tagged scene descriptions import.
html_todo -- Provide a class for html invisibly tagged "Todo" chapters import.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
