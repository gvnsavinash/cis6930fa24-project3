import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
import sqlite3
import project0

import urllib.request

# Mock logger setup
@patch('project0.setup_logger')
@patch('project0.log_message')
def test_fetchincidents_success(mock_log_message, mock_setup_logger):
    url = "https://www.normanok.gov/sites/default/files/documents/2024-09/2024-09-12_daily_incident_summary.pdf"
    mock_response = MagicMock()
    mock_response.read.return_value = b"PDF data"
    
    with patch('urllib.request.urlopen', return_value=mock_response):
        data = project0.fetchincidents(url)
        assert data == b"PDF data"
        mock_log_message.assert_any_call(mock_setup_logger.return_value, 'info', f"Download PDF from URL: {url}")
        mock_log_message.assert_any_call(mock_setup_logger.return_value, 'info', f"Successfully downloaded PDF from {url}")

@patch('project0.setup_logger')
@patch('project0.log_message')
def test_fetchincidents_failure(mock_log_message, mock_setup_logger):
    url = "https://www.normanok.gov/sites/default/files/documents/2024-09/2024-09-12_daily_incident_summary.pdf"
    
    with patch('urllib.request.urlopen', side_effect=Exception("Download error")):
        with pytest.raises(Exception, match="Download error"):
            project0.fetchincidents(url)
        mock_log_message.assert_any_call(mock_setup_logger.return_value, 'error', f"Failed to download PDF from {url}: Download error")

@patch('project0.setup_logger')
@patch('project0.log_message')
def test_extractincidents_success(mock_log_message, mock_setup_logger):
    pdf_data = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"
    
    with patch('pypdf.PdfReader') as mock_pdf_reader:
        mock_pdf_reader.return_value.pages = [MagicMock()]
        mock_pdf_reader.return_value.pages[0].extract_text.return_value = "2024-09-12 12:00:00 12345 Some Location Nature ORI"
        
        date_list, incident_number_list, location_list, nature_list, ori_list = project0.extractincidents(pdf_data)
        
        assert date_list == ["2024-09-12 12:00:00"]
        assert incident_number_list == ["12345"]
        assert location_list == ["Some Location"]
        assert nature_list == ["Nature"]
        assert ori_list == ["ORI"]
        mock_log_message.assert_any_call(mock_setup_logger.return_value, 'info', "Starting to extract incidents from the PDF")
        mock_log_message.assert_any_call(mock_setup_logger.return_value, 'info', "Successfully extracted all incidents from the PDF")

@patch('project0.setup_logger')
@patch('project0.log_message')
def test_createdb(mock_log_message, mock_setup_logger):
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        conn = project0.createdb()
        
        assert conn == mock_conn
        mock_log_message.assert_any_call(mock_setup_logger.return_value, 'info', "Successfully created new 'normanpd.db' database and 'incidents' table with all fields")

@patch('project0.setup_logger')
@patch('project0.log_message')
def test_populatedb(mock_log_message, mock_setup_logger):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE incidents (
            DateTime TEXT,
            IncidentNumber TEXT,
            Location TEXT,
            Nature TEXT,
            IncidentORI TEXT
        )
    ''')
    conn.commit()
    
    date_list = ["2024-09-12 12:00:00"]
    incident_number_list = ["12345"]
    location_list = ["Some Location"]
    nature_list = ["Nature"]
    ori_list = ["ORI"]
    
    project0.populatedb(conn, date_list, incident_number_list, location_list, nature_list, ori_list)
    
    cursor.execute('SELECT * FROM incidents')
    results = cursor.fetchall()
    
    assert results == [("2024-09-12 12:00:00", "12345", "Some Location", "Nature", "ORI")]
    mock_log_message.assert_any_call(mock_setup_logger.return_value, 'info', "Successfully inserted incidents into the database")

@patch('project0.setup_logger')
@patch('project0.log_message')
def test_status(mock_log_message, mock_setup_logger):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE incidents (
            DateTime TEXT,
            IncidentNumber TEXT,
            Location TEXT,
            Nature TEXT,
            IncidentORI TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO incidents (DateTime, IncidentNumber, Location, Nature, IncidentORI)
        VALUES ('2024-09-12 12:00:00', '12345', 'Some Location', 'Nature', 'ORI')
    ''')
    conn.commit()
    
    with patch('builtins.print') as mock_print:
        project0.status(conn)
        mock_print.assert_any_call("\nFormatted results:")
        mock_print.assert_any_call("Nature|1")
        mock_log_message.assert_any_call(mock_setup_logger.return_value, 'info', "Successfully printed status of incidents by nature")