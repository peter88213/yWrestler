"""Provide a facade class for a command line user interface.

Copyright (c) 2022 Peter Triesberger
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
from pywriter.pywriter_globals import ERROR
from pywriter.ui.ui import Ui


class UiCmd(Ui):
    """Ui subclass implementing a console interface.
    
    Public methods:
        ask_yes_no(text) -- return True or False.
        set_info_what(message) -- show what the converter is going to do.
        set_info_how(message) -- show how the converter is doing.
    """

    def __init__(self, title):
        """Print the title.
        
        Extend the Ui constructor.
        """
        super().__init__(title)
        print(title)

    def ask_yes_no(self, text):
        """Query True or False at the console.
        
        Positional argument.
            Question to be printed at the console. 
            
        Override the superclass method.       
        """
        result = input(f'WARNING: {text} (y/n)')

        if result.lower() == 'y':
            return True

        else:
            return False

    def set_info_what(self, message):
        """Show what the converter is going to do.
        
        Print the message.
        Override the superclass method.
        """
        print(message)

    def set_info_how(self, message):
        """Show how the converter is doing.

        Print the message, replacing the error marker, if any.
        Override the superclass method.
        """
        if message.startswith(ERROR):
            message = f'FAIL: {message.split(ERROR, maxsplit=1)[1].strip()}'

        self.infoHowText = message
        print(message)
