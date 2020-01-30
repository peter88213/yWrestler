"""A lean Pypandoc substitute

Relieves the unexperienced user from the need of 
installing the Pypandoc wrapper. 
See: https://pypi.org/project/pypandoc/

Part of the PyWriter project.
Copyright (c) 2020 Peter Triesberger.
For further information see https://github.com/peter88213/PyWriter
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""

import os


def convert_file(srcFile: str, dstFormat: str, format: str = '', outputfile: str = '', extra_args: list = []) -> str:
    """Pandoc wrapper emulating the pypandoc.convert_file functon. """

    extraArgs = ' '
    for extraArgument in extra_args:
        extraArgs = extraArgs + extraArgument + ' '

    argument1 = 'pandoc'
    argument2 = ' -w ' + dstFormat
    argument3 = ' -r ' + format
    argument4 = ' -o "' + outputfile + '"'
    argument5 = ' ' + extraArgs
    argument6 = ' "' + srcFile + '"'

    status = os.system(argument1 + argument2 + argument3 +
                       argument4 + argument5 + argument6)

    if status == 0:

        if os.path.isfile(outputfile):
            return 'SUCCESS: Pandoc created "' + outputfile + '".'

    return 'ERROR: No Pandoc result.'


if __name__ == '__main__':
    pass
