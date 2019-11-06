#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: build.py
#
# Copyright 2018 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

import logging
import os
import shutil
import tarfile

# this sets up everything and MUST be included before any third party module in every step
import _initialize_template

from bootstrap import bootstrap
from emoji import emojize
from configuration import LOGGING_LEVEL, PROJECT_SLUG, PACKAGE_EXCLUDING_FILES
from library import execute_command, clean_up, save_requirements, Pushd

# This is the main prefix used for logging
LOGGER_BASENAME = '''_CI.build'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def filter_file(tarfile):
     if tarfile.name in PACKAGE_EXCLUDING_FILES:
          return None
     else:
          return tarfile


def make_tarfile(output_filename, source_dir):
    try:
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir), filter=filter_file)
        return True
    except Exception:
        return False


def build():
    bootstrap()
    working_directory = 'dist'
    clean_up(working_directory)
    try:
        os.mkdir(working_directory)
    except OSError:
        LOGGER.error("Creation of the directory %s failed" % path)
        raise SystemExit(1)
    package_name = f"{PROJECT_SLUG}-{open('.VERSION').read().strip()}.tar.gz"
    success = False
    with Pushd(working_directory):
        success = make_tarfile(package_name, '../')
    if success:
        LOGGER.info('%s Successfully built artifact %s',
                    emojize(':white_heavy_check_mark:'),
                    emojize(':thumbs_up:'))
    else:
        LOGGER.error('%s Errors building artifact! %s',
                     emojize(':cross_mark:'),
                     emojize(':crying_face:'))
    return True if success else False


if __name__ == '__main__':
    raise SystemExit(0 if build() else 1)
