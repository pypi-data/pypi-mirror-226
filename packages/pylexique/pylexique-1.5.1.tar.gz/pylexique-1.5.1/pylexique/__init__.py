# -*- coding: utf-8 -*-

"""Top-level package for pylexique."""

__author__ = """SekouDiaoNlp"""
__email__ = 'diao.sekou.nlp@gmail.com'
__version__ = '1.5.1'
__copyright__ = "Copyright (c) 2021, SekouDiaoNlp"
__credits__ = ("Lexique383",)
__license__ = "MIT"
__maintainer__ = "SekouDiaoNlp"
__status__ = "Production"

__all__ = ['Lexique383', 'LexItem', 'LexEntryTypes']

import pkg_resources

from .pylexique import Lexique383, LexItem, LexEntryTypes

_RESOURCE_PACKAGE = 'pylexique'
_RESOURCE_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'Lexique383/Lexique383.txt')
