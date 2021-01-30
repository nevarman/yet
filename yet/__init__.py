"""
YET
"""

from __future__ import (absolute_import, division, print_function)

import os
from sys import version_info


# Version helper
def version_helper():
    if __release__:
        version_string = 'yet {0}'.format(__version__)
    else:
        import subprocess
        version_string = 'yet-master {0}'
        try:
            git_describe = subprocess.Popen(['git', 'describe'],
                                            universal_newlines=True,
                                            cwd=YETDIR,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
            (git_description, _) = git_describe.communicate()
            version_string = version_string.format(git_description.strip('\n'))
        except (OSError, subprocess.CalledProcessError):
            version_string = version_string.format(__version__)
    return version_string


# Information
__license__ = 'GPL3'
__version__ = '0.1.6'
__release__ = False
__author__ = __maintainer__ = 'mushroomrisotto'
__email__ = 'pypi.gib@aleeas.com'

# Constants
YETDIR = os.path.dirname(__file__)
USAGE = '%prog [options] [path]'
VERSION = version_helper()
PY3 = version_info[0] >= 3

# These variables are ignored if the corresponding
# XDG environment variable is non-empty and absolute
# CACHEDIR = os.path.expanduser('~/.cache/yet')
# CONFDIR = os.path.expanduser('~/.config/yet')
# DATADIR = os.path.expanduser('~/.local/share/yet')

# args = None
