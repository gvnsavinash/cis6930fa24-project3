# cis6930fa24 -- Assignment0

Name: Venkata Naga Satya Avinash, Gudipudi

---

## Project Description

This project is about working with the FBI’s Most Wanted API. We need to fetch data from the API and format it into a CSV-like structure with a special thorn character (`þ`) separating the values. The data includes information about people wanted by the FBI, such as the title, subjects, and field offices related to each case. 

The program can either fetch live data from the API or read it from a local JSON file. Once retrieved, the data is formatted for output.

---

## Implementation Steps

1. Data Retrieval: 
   - You can either fetch data from the FBI’s Most Wanted API or load it from a local JSON file.
   
2. Data Processing: 
   - The program extracts key fields such as the title, subjects, and field offices from each data record.
   
3. Data Formatting: 
   - The extracted data is formatted into thorn-separated (þ) records, creating a structured and human-readable output.

4. Output: 
   - The formatted data is printed to the console (standard output).

---

## Expected Output

The output is a list of records where each line follows this structure:

{title}þ{subjects}þ{field_offices}


For example, a sample output :

Extreme lossþsebastian,Pit BullþMiami
Dissapointing teamþDJþTallahassee,Dublin
Florida ManþSeeking InformationþGainesville
Data Engineerþþall over


---

## Environment Setup

To set up the environment, use `pipenv` to install the required packages. Run the following command in your project directory:


pipenv install 


This will create a virtual environment and install the dependencies needed to run the project.

---

## How to Run the Program

You can run the program in two ways:

1. Fetch data from the FBI API:

   Run the following command to retrieve data from a specific page of the FBI Most Wanted API:

   
   pipenv run python main.py --page <page_number>
   

   Replace `<page_number>` with a number like `1` or `2` etc , to get the respective page from the API.

2. Load data from a local JSON file:

   If you want to load data from a local JSON file instead of the API, run the following command:

   
   pipenv run python main.py --file-location <path_to_json_file>
   

   Replace `<path_to_json_file>` with the actual path to your JSON file.
   In this Project FileName is "jsonfile.json"

---

## Functions

### `main.py` Functions

- `fetch_data(page)`: 

  - Fetches data from the FBI API for a specified page.
  - Raises exceptions in case of errors and exits the program.
  
- `load_json(file_location)`: 

  - Loads data from a specified JSON file on your local machine.
  - Exits the program if there's an error while reading the file.

- `get_item_title(item)`: 

  - Extracts the title from a record (e.g., the name of the wanted person or event).

- `get_item_subjects(item)`: 

  - Extracts and formats the subjects from a record as a list or a string. Handles empty or missing subjects.

- `get_item_field_offices(item)`:

  - Extracts and formats the field offices from a record as a list or a string with a comma-separated.

- `format_fbi_wanted_data(data)`:

  - Formats the retrieved or loaded data into a thorn-separated format.
  - Returns a list where each entry is formatted as {title}þ{subjects}þ{field_offices}.

- `main(page=None, file_location=None)`: 

  - The main function that coordinates retrieving data (either from the API or a file), formatting it, and printing the output.


---

## Test Cases

There are two test files included in this project to ensure the functionality works as expected.

### `test_download.py`

This file includes the following tests and it will retrieving from API Page:

1. test_extract_fields():
   - Tests the extraction of fields like title, subjects, and field offices from the data, ensuring correct handling of None and string types.

2. test_successful_data_download():
   - Verifies successful data downloading from the FBI API.

3. test_load_json():
  - Tests loading data from a local JSON file.

4. test_format_fbi_wanted_data():
  - Validates the proper formatting of FBI data into thorn-separated format and ensures it contains the necessary keys.
   


### `test_randompage.py`

This file includes a test for retrieving data from a random page:

1. test_fetch_random_page():
  - Tests fetching data from a random page of the FBI API and validates its correctness.

2. test_invalid_page():
  - Verifies that fetching from an invalid page returns an empty result set.

3. test_get_item_title():
  - Tests extracting the title field from an API response.

4. test_format_fbi_wanted_data():
  - Tests that the formatted output contains thorn-separated values for the title, subjects, and field offices.
  
---

## How to Run the Tests

To run the tests and verify that the program works as expected, use `pytest`:


pipenv run python -m pytest -v


The tests will automatically validate the main functionalities, such as downloading data and formatting it correctly.

---

## Future Enhancements
1. Database Integration: The program does not use a database but relies on fetching data in real-time from the FBI's API. The API data is then processed and formatted as required. Future versions may consider storing the fetched data into a database for better retrieval and management.
2. Extended Field Extraction: Future versions could extract more fields from the API, such as images or detailed descriptions.

## Bugs and Assumptions

1. API Structure Changes: If the API structure changes, the program may fail to process the data correctly.
2. Local JSON Format: The program expects the local JSON file to have the same structure as the API response.
3. Network Issues: No graceful handling of network timeouts or connection failures.
4. Command-Line Arguments: Either `--page` or `--file-location` must be provided. If neither or both are given, the program will exit with an error.
5. Special Characters: The program assumes the thorn (`þ`) character does not appear in the data fields.
6. Empty Fields: Empty or null fields are handled, but fully empty records might still appear in the output.
7. File Access: Assumes that the user has read permissions for the file in the `--file-location` option.
8. Data Consistency: The program expects the data to be consistently formatted. Inconsistent entries may cause issues.

---
