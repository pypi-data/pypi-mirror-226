# imports - standard imports
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import typing
from collections import OrderedDict
from datetime import date
from functools import lru_cache
from urllib.parse import urlparse

# imports - third party imports
import click
import git

# imports - module imports
import brik
from brik.exceptions import NotInBrikDirectoryError
from brik.utils import (
	UNSET_ARG,
	fetch_details_from_tag,
	get_available_folder_name,
	is_brik_directory,
	is_git_url,
	is_valid_criscostack_branch,
	log,
	run_criscostack_cmd,
)
from brik.utils.brik import build_assets, install_python_dev_dependencies
from brik.utils.render import step