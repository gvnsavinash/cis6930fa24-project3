import urllib.request
import pypdf
from io import BytesIO
import re
import tempfile

from logger import setup_logger, log_message

# Logger  for project0.py
#logger = setup_logger("project0.log")  # This will save the log in the resources folder

# Download the PDF file
def fetchincidents(url):
    """
    Fetches a PDF document from the specified URL and saves it to a temporary file.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request) as response:
        if response.status == 200:
            # Create a temporary file
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            with open(temp_pdf.name, 'wb') as f:
                f.write(response.read())
            return temp_pdf.name
        else:
            response.raise_for_status()

# Extract incidents
def extractincidents(incident_data):
    """
    Extracts incident data from a PDF file.
    This function reads a PDF file containing incident reports and extracts relevant fields such as date, 
    incident number, location, nature, and ORI. The extracted data is returned as separate lists for each field.
    Args:
        incident_data (bytes): The binary content of the PDF file.
    Returns:
        tuple: A tuple containing five lists:
            - date_list (list of str): List of incident dates.
            - incident_number_list (list of str): List of incident numbers.
            - location_list (list of str): List of incident locations.
            - nature_list (list of str): List of incident natures.
            - ori_list (list of str): List of ORI codes.
    Raises:
        Exception: If an error occurs during PDF extraction.
    Logs:
        Logs various stages of the extraction process, including start, progress, and errors.
    """
    #log_message(logger, 'info', "Starting to extract incidents from the PDF")
    
    try:
        pdf_file = BytesIO(incident_data)
        reader = pypdf.PdfReader(pdf_file)
        date_list = []
        incident_number_list = []
        location_list = []
        nature_list = []
        ori_list = []

        for page_num, page in enumerate(reader.pages):
            #log_message(logger, 'debug', f"Extracting data from page {page_num + 1}")
            page_extract = page.extract_text(
                extraction_mode="layout", layout_mode_space_vertically=False
            ).split("\n")

            for line_num, line in enumerate(page_extract):
                fields = column_seperator(line)
                if fields and len(fields) == 5:
                    #log_message(logger, 'debug', f"Page {page_num + 1}, Line {line_num + 1}: Extracted fields: {fields}")
                    date_list.append(fields[0])
                    incident_number_list.append(fields[1])
                    location_list.append(fields[2])
                    nature_list.append(fields[3])
                    ori_list.append(fields[4])
                else:
                    #log_message(logger, 'debug', f"Page {page_num + 1}, Line {line_num + 1}: Insufficient fields: {fields}")
                    pass

        #log_message(logger, 'info', "Successfully extracted all incidents from the PDF")
        return date_list, incident_number_list, location_list, nature_list, ori_list
    except Exception as e:
        #log_message(logger, 'error', f"Failed to extract incidents from the PDF: {e}")
        raise

# Split a line based on the regular expression (multiple spaces)
def column_seperator(line):
    """
    Splits a line of text into its respective fields based on 2 or more spaces as delimiters.
    Args:
        line (str): The input line to be split.
    Returns:
        tuple: A tuple containing date_time, incident_number, location, nature, and incident_ori if the line has sufficient fields.
        None: If the line does not contain enough fields.
    """
    
    #log_message(logger, 'debug', f"Splitting line: {line}")
    
    # Split the line by 2 or more spaces
    seperate_inlist = re.split(r"\s{2,}", line)
    
    # Clean up extra spaces
    seperate_inlist = [item.strip() for item in seperate_inlist if item.strip()]
    #log_message(logger, 'debug', f"Split result: {seperate_inlist}")
    
   
    if len(seperate_inlist) >= 5:
        # Extract fields
        date_time = seperate_inlist[0]  # First field is Date/Time
        incident_number = seperate_inlist[1]  # Second field is Incident Number
        location = ' '.join(seperate_inlist[2:-2])  # Location  have multiple parts, so joining with spaces
        nature = seperate_inlist[-2]  # Second-to-last field is Nature
        incident_ori = seperate_inlist[-1]  # Last field is Incident ORI
        
        #log_message(logger, 'debug', f"Extracted fields: Date/Time: {date_time}, Incident Number: {incident_number}, Location: {location}, Nature: {nature}, Incident ORI: {incident_ori}")
        
        return date_time, incident_number, location, nature, incident_ori
    else:
        #log_message(logger, 'debug', f"Insufficient fields found in line: {line}")
        return None


