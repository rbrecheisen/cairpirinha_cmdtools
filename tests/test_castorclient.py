#!/usr/bin/env python

import pytest

from caipirinha_cmdtools import CastorClient
from tests.constants import *


def test_castorclient_can_be_instantiated():
    client = CastorClient()
    client.print_current_dir()


def test_dhba_data_successfully_imported():

    # - Create client tool
    # - Load DICA export Excel file
    # - For each record in the export file, do the following:
    #    - Import record into Castor
    #    - Verify that record successfully imported
    pass


def test_dpca_data_successfully_imported():
    pass
