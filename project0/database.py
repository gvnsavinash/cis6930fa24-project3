import os
import sqlite3
import logger
from logger import setup_logger, log_message

# Logger  for database.py
logger = setup_logger("database.log")

# create and connect to the SQLite database
def createdb():
    """
    Creates a new SQLite database named 'normanpd.db' in the 'resources' folder.
    If the database already exists, it deletes the old one and creates a new one.
    Also sets up the 'incidents' table with fields: DateTime, IncidentNumber, Location, Nature, and IncidentORI.
    Returns:
        sqlite3.Connection: Connection object to the newly created database.
    Raises:
        Exception: If there is an error during database creation.
    """
    # path for the 'resources' folder 
    abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(abs_path, "resources", "normanpd.db")

    log_message(logger, 'info', f"Checking if '{db_path}' exists and creating a new one if needed")
    
    # Check if the database already exists, if so, remove it
    if os.path.exists(db_path):
        os.remove(db_path)
        log_message(logger, 'debug', f"Removed the existing '{db_path}' database")

    try:
       
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


#  populate the database with extracted fields
def populatedb(conn, date_list, incident_number_list, location_list, nature_list, ori_list):
    """
    Inserts incident data into the database after clearing the existing records.
    Parameters:
    conn (sqlite3.Connection): The database connection object.
    date_list (list): List of incident dates.
    incident_number_list (list): List of incident numbers.
    location_list (list): List of incident locations.
    nature_list (list): List of incident natures.
    ori_list (list): List of incident ORIs.
    Raises:
    Exception: If there is an error during the database operation.
    """
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

# print the status of incidents by nature
def status(conn):
    """
    Queries the database for the status of incidents by their nature, prints the results,
    and logs the process.
    Args:
        conn (sqlite3.Connection): The database connection object.
    Raises:
        Exception: If there is an error querying the database.
    Logs:
        - Info: When the query starts and completes successfully.
        - Debug: For each nature and its count, or if no records are found.
        - Error: If the query fails.
    """
    log_message(logger, 'info', "Querying and printing status of incidents by nature")
    
    try:
        cursor = conn.cursor()
        
        # Query to count occurrences of each 'Nature', sorting alphabetically 
        cursor.execute('''
            SELECT Nature, COUNT(*)
            FROM incidents
            GROUP BY Nature
            ORDER BY Nature ASC
        ''')
        results = cursor.fetchall()

        if not results:
            print("No data found in the Nature column.")
            log_message(logger, 'debug', "No Nature records found in the database.")
        else:
            
            for row in results:
                print(f"{row[0]}|{row[1]}")
                log_message(logger, 'debug', f"Nature: {row[0]}, Count: {row[1]}")

        log_message(logger, 'info', "Successfully printed status of incidents by nature")
    except Exception as e:
        log_message(logger, 'error', f"Failed to query the database for status: {e}")
        raise
