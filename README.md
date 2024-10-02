cis6930fa24 -- Project 0 -- Incident Report Processing
Name: [Your Name]

Project Description
This project automates the downloading, parsing, and analysis of incident reports provided by the Norman Police Department in PDF format. It processes data such as incident time, number, location, nature, and ORI (Originating Agency Identifier), stores it in an SQLite database, and generates a summary report on the nature of incidents.

How to Install
Install the necessary dependencies using a virtual environment like pipenv.
After setting up the virtual environment, install dependencies with the appropriate commands.
How to Run
Run the main Python script, passing in the URL of the incident report PDF as an argument. The script will download, parse, and store the incident data into the database, and a summary report will be generated.

Example: Provide the URL of the incident report PDF to the script, which will handle the rest, including data extraction and generating the summary report.

Functions
main.py
main():
Description: The main driver function that coordinates the entire process, from downloading the PDF to storing the data in the database and generating a summary report. It calls other functions from the project for different tasks such as data extraction and database population.
project0.py
fetchincidents(url):

Description: Downloads the PDF file from the provided URL.
Parameters: url (string): The URL of the PDF.
Returns: The byte stream of the downloaded PDF.
extractincidents(byte_pdf):

Description: Extracts the details (incident time, number, location, nature, and ORI) from the byte stream of the PDF.
Parameters: byte_pdf: Byte stream of the PDF file.
Returns: Five lists containing the respective fields for all incidents extracted from the PDF.
column_seperator(line):

Description: Splits a line of text from the PDF into its respective fields: Date/Time, Incident Number, Location, Nature, ORI.
Parameters: line: The string to be split.
Returns: A tuple containing the extracted fields.
status(conn):

Description: Generates a summary report based on the incident data stored in the database. It retrieves the number of occurrences of each incident nature, sorts them alphabetically, and prints them in a formatted string with each row separated by a pipe character (|).
Parameters: conn: The database connection object.
Returns: A string formatted summary of incidents and their occurrences.
database.py
createdb():

Description: Creates an SQLite database named normanpd.db and a table called incidents to store the parsed data from the incident reports.
Returns: A connection object to the SQLite database.
populatedb(conn, date_list, incident_number_list, location_list, nature_list, ori_list):

Description: Populates the incidents table in the SQLite database with the extracted data from the incident report.
Parameters:
conn: Database connection object.
date_list, incident_number_list, location_list, nature_list, ori_list: Lists containing the data to insert.
logger.py
setup_logger(log_file):

Description: Sets up a logger for logging messages to a specified log file.
Parameters: log_file: The path to the log file.
Returns: A logger object that can be used to log messages.
log_message(logger, level, message):

Description: Logs a message with a specified severity level (e.g., info, debug, error) using the provided logger object.
Parameters:
logger: The logger object.
level: The severity level of the log.
message: The message to be logged.
test_file.py
This file contains the unit tests for various components of the project.

test_databasecreation():

Description: Tests the database creation functionality by ensuring that a database connection is successfully established.
Assertions: The connection object is not None.
test_databaseinsertion():

Description: Tests the insertion of data into the database. It verifies that data is correctly inserted into the incidents table by checking that the number of records is greater than zero.
Assertions: The count of records in the incidents table is greater than 0.
test_download_pdf():

Description: Tests the downloading of the PDF from a specified URL to ensure the PDF byte stream is successfully retrieved.
Assertions: The PDF stream is not None.
test_extract_incidents_from_pdf():

Description: Tests the extraction of incidents from the PDF by checking that the lists returned (dates, incident numbers, locations, natures, and ORIs) contain at least one element each.
Assertions: All extracted lists contain at least one element.
test_column_seperator():

Description: Tests the column separator functionality, ensuring that the function splits a line of text into the correct components.
Assertions: The split result matches the expected tuple.
Database Development
An SQLite database is used to store the incident report data. The database contains a single table called incidents with the following fields:

incident_time (TEXT)
incident_number (TEXT)
incident_location (TEXT)
nature (TEXT)
incident_ori (TEXT)
Data is inserted into the table using the pandas.DataFrame.to_sql() function for efficient insertion.

SQL Query for Summary Report
The summary report of incidents by their nature is generated using this SQL query:

sql
Copy code
SELECT nature, count(*) as num_incidents 
FROM incidents 
GROUP BY nature 
ORDER BY num_incidents ASC, nature;
Bugs and Assumptions
PDF Structure: The project assumes that the structure of the incident report PDF remains the same. Any changes to the structure may lead to issues in data extraction.
Missing Fields: A record must have at least three fields. Records missing more than two fields will be discarded.
Junk Data: The first two rows and the last row of the PDF are assumed to be junk data and are ignored.
Write Access: The project assumes that the system has write access to the resources directory where logs and the database are stored.
Field Order: The project assumes that the fields in the incident report PDF are in the following order: incident_time, incident_number, incident_location, nature, and incident_ori.