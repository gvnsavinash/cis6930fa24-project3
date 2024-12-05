import argparse
from logger import setup_logger, log_message
import project0  
import database

# logger for main.py
logger = setup_logger("main.log")  # This will save the log in the resources folder

def main(url):
    #log_message(logger, 'info', "Starting main function")
    
    try:
        # Download data
        #log_message(logger, 'info', f"Fetching incidents from URL: {url}")
        incident_data = project0.fetchincidents(url)
        if incident_data is None:
            #log_message(logger, 'error', "Failed to fetch incidents. Exiting.")
            return

        # Extract data
        #log_message(logger, 'info', "Extracting incidents from PDF")
        date_list, incident_number_list, location_list, nature_list, ori_list = project0.extractincidents(incident_data)
        if not date_list or not incident_number_list or not location_list or not nature_list or not ori_list:
            #log_message(logger, 'error', "No incidents extracted from the PDF. Exiting.")
            return

        # Create new database
        #log_message(logger, 'info', "Creating new SQLite database")
        db = database.createdb()

        # Insert data into the database
        #log_message(logger, 'info', f"Inserting {len(date_list)} incidents into the database")
        database.populatedb(db, date_list, incident_number_list, location_list, nature_list, ori_list)

        # Print incident counts
        #log_message(logger, 'info', "Printing incident counts by nature")
        database.status(db)

        #log_message(logger, 'info', "Main function completed successfully")
    except Exception as e:
        #log_message(logger, 'error', f"Error in main function: {e}")
        pass

if __name__ == '__main__':
    #log_message(logger, 'info', "Starting the script")

    # Set up argument parser to accept the --incidents URL argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                        help="Incident summary URL for the PDF to be processed.")
     
    args = parser.parse_args()

    if args.incidents:
        #log_message(logger, 'info', f"Received incidents URL: {args.incidents}")
        main(args.incidents)
    else:
        #log_message(logger, 'error', "No incidents URL provided. Exiting.")
        pass
