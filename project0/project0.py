import urllib.request
import pypdf
from io import BytesIO
import sqlite3
import re
import os
import project0
from logger import setup_logger, log_message

# Use the centralized logger specifically for project0.py
logger = setup_logger("project0.log")  # This will save the log in the resources folder

# Function to download the PDF file
def fetchincidents(url):
    log_message(logger, 'info', f"Download PDF from URL: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
        }
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        data = response.read()
        log_message(logger, 'info', f"Successfully downloaded PDF from {url}")
        return data
    except Exception as e:
        log_message(logger, 'error', f"Failed to download PDF from {url}: {e}")
        raise

# Function to extract incidents
def extractincidents(incident_data):
    log_message(logger, 'info', "Starting to extract incidents from the PDF")
    
    try:
        pdf_file = BytesIO(incident_data)
        reader = pypdf.PdfReader(pdf_file)
        date_list = []
        incident_number_list = []
        location_list = []
        nature_list = []
        ori_list = []

        for page_num, page in enumerate(reader.pages):
            log_message(logger, 'debug', f"Extracting data from page {page_num + 1}")
            page_extract = page.extract_text(
                extraction_mode="layout", layout_mode_space_vertically=False
            ).split("\n")

            for line_num, line in enumerate(page_extract):
                fields = project0.column_seperator(line)
                if fields and len(fields) == 5:
                    log_message(logger, 'debug', f"Page {page_num + 1}, Line {line_num + 1}: Extracted fields: {fields}")
                    date_list.append(fields[0])
                    incident_number_list.append(fields[1])
                    location_list.append(fields[2])
                    nature_list.append(fields[3])
                    ori_list.append(fields[4])
                else:
                    log_message(logger, 'debug', f"Page {page_num + 1}, Line {line_num + 1}: Insufficient fields: {fields}")

        log_message(logger, 'info', "Successfully extracted all incidents from the PDF")
        return date_list, incident_number_list, location_list, nature_list, ori_list
    except Exception as e:
        log_message(logger, 'error', f"Failed to extract incidents from the PDF: {e}")
        raise

# Function to split a line based on the regular expression (multiple spaces)
def column_seperator(line):
    log_message(logger, 'debug', f"Splitting line: {line}")
    
    # Split the line by 2 or more spaces
    seperate_inlist = re.split(r"\s{2,}", line)
    
    # Clean up extra spaces
    seperate_inlist = [item.strip() for item in seperate_inlist if item.strip()]
    log_message(logger, 'debug', f"Split result: {seperate_inlist}")
    
    # Ensure there are enough fields in the line before attempting extraction
    if len(seperate_inlist) >= 5:
        # Extract fields based on the split result
        date_time = seperate_inlist[0]  # First field is Date/Time
        incident_number = seperate_inlist[1]  # Second field is Incident Number
        location = ' '.join(seperate_inlist[2:-2])  # Location may have multiple parts, so join with spaces
        nature = seperate_inlist[-2]  # Second-to-last field is Nature
        incident_ori = seperate_inlist[-1]  # Last field is Incident ORI
        
        log_message(logger, 'debug', f"Extracted fields: Date/Time: {date_time}, Incident Number: {incident_number}, Location: {location}, Nature: {nature}, Incident ORI: {incident_ori}")
        
        return date_time, incident_number, location, nature, incident_ori
    else:
        log_message(logger, 'debug', f"Insufficient fields found in line: {line}")
        return None

# Function to extract incidents from the PDF


# Function to create and connect to the SQLite database
def createdb():
    """
    Creates a SQLite database and returns a connection object.
    If 'normanpd.db' exists in the 'resources' folder, it deletes the old database and creates a new one.
    Also creates the 'incidents' table with all necessary fields.
    """
    # Define the path for the 'resources' folder relative to the current script
    abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(abs_path, "resources", "normanpd.db")

    log_message(logger, 'info', f"Checking if '{db_path}' exists and creating a new one if needed")
    
    # Check if the database already exists, if so, remove it
    if os.path.exists(db_path):
        os.remove(db_path)
        log_message(logger, 'debug', f"Removed the existing '{db_path}' database")

    try:
        # Create a new SQLite database inside the 'resources' folder
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create the 'incidents' table with all fields
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                DateTime TEXT,
                IncidentNumber TEXT,
                Location TEXT,
                Nature TEXT,
                IncidentORI TEXT
            )
        ''')
        conn.commit()
        log_message(logger, 'info', f"Successfully created new '{db_path}' database and 'incidents' table with all fields")
        return conn
    except Exception as e:
        log_message(logger, 'error', f"Failed to create database: {e}")
        raise

    log_message(logger, 'info', "Creating SQLite database 'normanpd.db'")
    
    try:
        conn = sqlite3.connect('normanpd.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                DateTime TEXT,
                IncidentNumber TEXT,
                Location TEXT,
                Nature TEXT,
                IncidentORI TEXT
            )
        ''')
        conn.commit()
        log_message(logger, 'info', "Successfully created database and table")
        return conn
    except Exception as e:
        log_message(logger, 'error', f"Failed to create database: {e}")
        raise

# Function to populate the database with extracted fields
def populatedb(conn, date_list, incident_number_list, location_list, nature_list, ori_list):
    log_message(logger, 'info', "Inserting extracted incidents into the database")
    
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM incidents')  # Clear the table before inserting new data
        conn.commit()
        log_message(logger, 'debug', "Successfully cleared the incidents table")

        incidents_data = list(zip(date_list, incident_number_list, location_list, nature_list, ori_list))

        cursor.executemany('''
            INSERT INTO incidents (DateTime, IncidentNumber, Location, Nature, IncidentORI)
            VALUES (?, ?, ?, ?, ?)
        ''', incidents_data)
        conn.commit()
        log_message(logger, 'info', "Successfully inserted incidents into the database")
    except Exception as e:
        log_message(logger, 'error', f"Failed to insert data into database: {e}")
        raise

# Function to print the status of incidents by nature
def status(conn):
    log_message(logger, 'info', "Querying and printing status of incidents by nature")
    
    try:
        cursor = conn.cursor()
        
        # Query to count occurrences of each 'Nature', sorting alphabetically (case-sensitive)
        cursor.execute('''
            SELECT Nature, COUNT(*)
            FROM incidents
            GROUP BY Nature
            ORDER BY Nature 
        ''')
        results = cursor.fetchall()

        if not results:
            print("No data found in the Nature column.")
            log_message(logger, 'debug', "No Nature records found in the database.")
        else:
            print("\nFormatted results:")
            for row in results:
                print(f"{row[0]}|{row[1]}")
                log_message(logger, 'debug', f"Nature: {row[0]}, Count: {row[1]}")

        log_message(logger, 'info', "Successfully printed status of incidents by nature")
    except Exception as e:
        log_message(logger, 'error', f"Failed to query the database for status: {e}")
        raise
