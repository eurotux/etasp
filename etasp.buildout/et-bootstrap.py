#!/usr/bin/python2.6
"""Early bootstrap script to run virtualenv before the regular buildout bootstrap.
"""

import subprocess

# FIXME: we should check the python versions available and have some option to wich version to use.

# run virtualenv
subprocess.call(["virtualenv", "--no-site-packages", "python"])


# run regular bootstrap
subprocess.call(["python/bin/python", "bootstrap.py"])

