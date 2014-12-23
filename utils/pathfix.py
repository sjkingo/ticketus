"""Fixes the paths and initialises Django.
Import this from other scripts."""

import os.path, sys
sys.path.append(os.path.realpath('..'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticketus.settings")
import django
django.setup()
