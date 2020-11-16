#!/usr/bin/env python

import pytest

from caipirinha_cmdtools import CastorClient
from tests.constants import *

"""
These are acceptance tests for the Castor client. Acceptance tests test the system from the outside.
i.e., from a user perspective. What will a user do with the Castor client? Why am I even building
this tool in the first place? I'm building it because I'd like to automate interaction with Castor EDC
to a certain extent. I'm always spending a lot of time extracting information from it, triggered by
questions from researchers. And I'm spending even more time to import new data into Castor. Part of
that last problem is caused by the fact that the records in Castor are not (yet) uniquely identifiable
by hospital ID and surgery date. Another part of that problem is caused by the fact that the input
data is very messy. Both issues need to be addressed in the near future. For the Castor client tool
we will assume that records in Castor can be uniquely identified by hospital ID and surgery date.

So, assuming that, how would a user use the Castor client? As I said before, importing new data is
a very important requirement since we regularly have new DICA patients that we want to save. So this
amounts to the following acceptance test:

    "As a data manager, I want to import the latest DHBA patients into Castor EDC, in order
    to keep Castor EDC up-to-date with the latest treatments performed at our hospital."
    
    "As a data manager, I want to import the latest DPCA patients into Castor EDC, in order
    to keep Castor EDC up-to-date with the latest treatments performed at our hospital."
    
This is what I, as a user, want from the tool. When I write a test for this functionality, I want it
to pass ONLY when those patients have really been imported into Castor. I don't want it to pass with
some dummy data. So, first of all, I need a real DICA export file. Also, to verify that the patient
data was successfully imported into Castor we need to be able to retrieve it again and match it with
the original DICA records.

We could even say, that we import DICA data on a record-by-record basis, i.e., load the DICA data into
the Castor client tool, and for each record, import the data, retrieve the newly created record from
Castor EDC and verify that it matches the DICA record. Then proceed with the next record. 

As you can see, we have DHBA and DPCA patients. In theory we could build the tool such that it automatically
figures out which is which based on the export file but, for now, this is not necesesary. We can always
combine them later. So we focus on only one at the time. 

Additional requirements:

- I am going to use the Castor client primarily as a command-line tool
- A secondary usage is to use as a library.

"""


def test_dhba_data_successfully_imported():

    # - Create client tool
    # - Load DICA export Excel file
    # - For each record in the export file, do the following:
    #    - Import record into Castor
    #    - Verify that record successfully imported
    pass


def test_dpca_data_successfully_imported():
    pass
