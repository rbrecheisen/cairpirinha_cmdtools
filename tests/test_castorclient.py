#!/usr/bin/env python

import pytest

from caipirinha_cmdtools import CastorClient
from tests.constants import *


@pytest.fixture
def castor_client():

    client = CastorClient()
    client.load_excel(os.path.join(TEST_DATA_DIR, TEST_DATA_EXCEL_FILE))
    return client


def test_load_excel_file():

    client = CastorClient()
    current_dir = client.pwd()
    assert os.path.isdir(current_dir)
    client.cd(TEST_DATA_DIR)
    contents = client.ls()
    assert TEST_DATA_EXCEL_FILE in contents
    data = client.load_excel(TEST_DATA_EXCEL_FILE)
    assert data.shape[0] == 507
    assert data.shape[1] == 482


def test_convert_hospital_id_column_to_string(castor_client):
    assert TEST_DATA_HOSPITAL_ID in castor_client.data.columns


def test_convert_surgery_date_column_to_string_as_dd_mm_yyyy(castor_client):
    assert TEST_DATA_SURGERY_DATE in castor_client.data.columns
