#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: upload.py
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
import sys
import hashlib
import requests
from requests.auth import HTTPBasicAuth

# this sets up everything and MUST be included before any third party module in every step
import _initialize_template

from emoji import emojize
from build import build
from library import execute_command, validate_environment_variable_prerequisites, Pushd
from configuration import PREREQUISITES, PROJECT_SLUG, ROLE_REPOSITORY, ANSIBLE_UPLOAD_USER

# This is the main prefix used for logging
LOGGER_BASENAME = '''_CI.upload'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def get_file_hashes(filename):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(filename, 'rb') as infile:
        while True:
            data = infile.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
            sha1.update(data)
    return {'X-Checksum-Sha1': sha1.hexdigest(),
            'X-Checksum-Sha256': sha256.hexdigest()}


def upload_package(package_name):
    with Pushd('dist'), open(package_name, 'rb') as ofile:
        headers = get_file_hashes(package_name)
        url = f'{ROLE_REPOSITORY}/{package_name}'
        response = requests.put(url,
                                data=ofile,
                                headers=headers,
                                auth=HTTPBasicAuth(ANSIBLE_UPLOAD_USER,
                                                   os.environ.get('ANSIBLE_UPLOAD_TOKEN')))
    return response.ok


def upload():
    success = build()
    if not success:
        LOGGER.error('Errors caught on building the artifact, bailing out...')
        raise SystemExit(1)
    if not validate_environment_variable_prerequisites(PREREQUISITES.get('upload_environment_variables', [])):
        LOGGER.error('Prerequisite environment variable for upload missing, cannot continue.')
        raise SystemExit(1)
    LOGGER.info('Trying to upload built artifact...')
    package_name = f"{PROJECT_SLUG}-{open('.VERSION').read().strip()}.tar.gz"
    success = upload_package(package_name)
    if success:
        LOGGER.info('%s Successfully uploaded artifact! %s',
                    emojize(':white_heavy_check_mark:'),
                    emojize(':thumbs_up:'))
    else:
        LOGGER.error('%s Errors found in uploading artifact! %s',
                     emojize(':cross_mark:'),
                     emojize(':crying_face:'))
    raise SystemExit(0 if success else 1)


if __name__ == '__main__':
    upload()
