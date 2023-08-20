from .exception import ScreenShotError
from .factory import pygrabshot

__version__ = "1.0.2"
__author__ = "kittyplot"
__copyright__ = """
Copyright (c) 2013-2023, kittyplot

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee or royalty is hereby
granted, provided that the above copyright notice appear in all copies
and that both that copyright notice and this permission notice appear
in supporting documentation or portions thereof, including
modifications, that you make.
"""
__all__ = ("ScreenShotError", "pygrabshot")
