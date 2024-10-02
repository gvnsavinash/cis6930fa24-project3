import os.path
import sys

# Add the 'project0' folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'project0')))

import database
import project0


def test_databasecreation():
    """
    Test the creation of a database.

    This test ensures that the `createdb` function from the `database` module
    successfully creates a database connection. It asserts that the connection
    is not None and then closes the connection.
    """
    conn = database.createdb()
    assert conn is not None
    conn.close()

def test_databaseinsertion():
    """
    Test the insertion of data into the database.

    This test function creates a database connection, populates the database with 
    sample data, and verifies that the data has been successfully inserted by 
    checking the count of records in the 'incidents' table.

    Assertions:
        - The count of records in the 'incidents' table should be greater than 0.
    """
    conn = database.createdb()
    date_list = ['8/2/2024 0:10','8/2/2024 0:12']
    incident_number_list = ['2024-00055701','2024-00011459']
    location_list = ['2954 OAK TREE AVE','700 N BERRY RD ']
    nature_list = ['Traffic Stop','Medical Call Pd Requested']
    ori_list = ['OK0140200','14005']
    database.populatedb(conn, date_list, incident_number_list, location_list, nature_list, ori_list)
    result = conn.execute("SELECT count(*) FROM incidents").fetchone()[0]
    assert result > 0
    conn.close()

def test_download_pdf():
    """
    Test the download of a PDF file from a given URL.

    This function verifies that the `fetchincidents` method from the `project0` module
    successfully retrieves a PDF stream from the specified URL.

    Asserts:
        The PDF stream is not None.
    """
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-02_daily_incident_summary.pdf"
    byte_pdf = project0.fetchincidents(url)
    assert byte_pdf is not None

def test_extract_incidents_from_pdf():
    """
    Test the extract_incidents_from_pdf function.

    This test fetches a PDF from a given URL and extracts incident details such as 
    dates, incident numbers, locations, natures, and ORIs. It asserts that each 
    extracted list contains at least one element, ensuring that the extraction 
    process is functioning correctly.
    """
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-02_daily_incident_summary.pdf"
    byte_pdf = project0.fetchincidents(url)
    date_list, incident_number_list, location_list, nature_list, ori_list = project0.extractincidents(byte_pdf)
    assert len(date_list) > 0
    assert len(incident_number_list) > 0
    assert len(location_list) > 0
    assert len(nature_list) > 0
    assert len(ori_list) > 0

def test_column_seperator():
    """
    Test the `column_seperator` function from the `project0` module.

    This test checks if the function correctly separates a given line of text
    into its respective columns: date and time, incident number, address, 
    incident type, and police department code.

    Expected result:
        ("8/2/2024 0:10", "2024-00055701", "2954 OAK TREE AVE", "Traffic Stop", "OK0140200")
    """
    line = "8/2/2024 0:10   2024-00055701  2954 OAK TREE AVE  Traffic Stop  OK0140200"
    result = project0.column_seperator(line)
    assert result == ("8/2/2024 0:10", "2024-00055701", "2954 OAK TREE AVE", "Traffic Stop", "OK0140200")
