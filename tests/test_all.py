import os
import pytest
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import main 
from main import *
import project0
from project0 import *
import pandas as pd
import numpy as np
import re
from io import BytesIO
from unittest import mock



def test_visualization_data_processing():
    """
    Test the processing of data for visualization.

    This function tests the `visualize` function from the `main` module to ensure it processes
    the provided data correctly for visualization purposes. The test data includes lists of dates,
    incident numbers, locations, natures, and ORIs (Originating Agency Identifiers).

    The test data is structured as follows:
    - 'date_list': A list of dates in string format.
    - 'incident_number_list': A list of incident numbers in string format.
    - 'location_list': A list of locations in string format.
    - 'nature_list': A list of natures of incidents in string format.
    - 'ori_list': A list of ORIs in string format.

    The function calls `visualize` with the test data and checks if the returned results contain
    the expected visualization types: 'scatter', 'bar', and 'bubble'. These assertions ensure that
    the `visualize` function processes the data correctly and generates the required visualizations.
    """
    """Test the processing of data for visualization."""
    from main import visualize
    # Expanded test data to satisfy n_clusters requirement
    test_data = {
        'date_list': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04'],
        'incident_number_list': ['001', '002', '003', '004'],
        'location_list': ['Location1', 'Location2', 'Location3', 'Location4'],
        'nature_list': ['Nature1', 'Nature2', 'Nature3', 'Nature4'],
        'ori_list': ['ORI1', 'ORI2', 'ORI3', 'ORI4']
    }
    results = visualize(**test_data)
    assert 'scatter' in results
    assert 'bar' in results
    assert 'bubble' in results
    


    
def test_fetch_incidents_live():
    """
    Test the fetchincidents function with a live URL.
    This test function performs the following steps:
    1. Defines a test URL pointing to a PDF document.
    2. Calls the fetchincidents function with the test URL and stores the returned file path.
    3. Asserts that the fetchincidents function returns a non-None file path.
    4. Asserts that a file exists at the returned file path.
    5. Asserts that the file at the returned path is not empty.
    6. Removes the file created during the test to clean up.
    The test ensures that the fetchincidents function correctly downloads a file from the given URL,
    saves it to the local file system, and that the file is not empty.
    """
    

    test_url = "https://www.normanok.gov/sites/default/files/documents/2024-11/2024-11-02_daily_incident_summary.pdf"
    file_path = fetchincidents(test_url)

    assert file_path is not None, "fetchincidents should return a file path, got None"
    assert os.path.exists(file_path), "fetchincidents should create a file at the returned path"
    assert os.path.getsize(file_path) > 0, "File at returned path should not be empty"

   
    os.remove(file_path)



