""" install.py

    Author: Matthew Thomson
    Date: 2023

"""

import os
import subprocess

try:
    os.makedirs("csv")
except FileExistsError:
    pass

try:
    os.makedirs("output")
except FileExistsError:
    pass

package_name = "pandas"

try:
    subprocess.check_call(['pip', 'install', package_name])
    print(f"{package_name} installed successfully!")
except Exception as err:
    print(f"Failed to install {package_name}")