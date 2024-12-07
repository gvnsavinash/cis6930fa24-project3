# cis6930fa24 -- Project3

Name: Venkata Naga Satya Avinash Gudipudi

# Project Descripition 

Develop an interactive web interface to visualize data from Norman Police Department incident PDFs. The interface should allow users to upload files via URL or direct upload and display three visualizations: clustering of records, a bar graph comparison, and a custom visualization.

# Key Features

1. PDF Upload and URL Submission: Allows for direct PDF uploads or URL submissions to access online PDFs.
2. Automated Data Extraction: Extracts critical details like dates, incident numbers, locations, and more from PDFs.
3. Advanced Data Visualization: Features dynamic visualizations including cluster scatter plots, bar graphs, and bubble charts to provide clear insights into the incident data.
4. Real-Time and Responsive: Offers real-time content updates and a responsive design for effective use across different devices.
5. This tool utilizes Flask for backend operations, integrating Python for data processing, while the frontend combines HTML, CSS,  for a seamless user experience.

# Assignment Objective 

1. Data Extraction:

Allow users to upload one or more NormanPD-style incident PDFs via a web interface (URL or file upload).

Extract key details from the PDFs, including:
Date/Time
Incident Number
Location
Nature of the Incident
Incident ORI

2. Data Analysis and Visualizations:

Create three different visualizations to help understand and summarize the data:

1. Scatter Chart: For clustering data
2. Bar Graph: For categorical data analysis
3. Bubble Chart (Chossen by own as per project descripition): For showing patterns and trends

3. Interactive Web Interface:

Display the visualizations on a web page with clear explanations.
Include a status table showing the data results related to the bar graph and bubble chart.

# Requirements
To run the project, you will need to install the following packages. The versions listed are known to be compatible, but newer versions may also work if they maintain backward compatibility. It is recommended to use a virtual environment to avoid conflicts with other Python projects you may have.

# Required Python Packages
1. Python: Ensure Python 3.12 is installed as specified in your Pipfile.
2. Flask: A micro web framework for Python, crucial for handling backend logic, routing, and serving web pages.
3. matplotlib: A comprehensive library for creating static, animated, and interactive visualizations in Python.
4. pandas: Provides high-performance, easy-to-use data structures, and data analysis tools.
5. scikit-learn: Useful for implementing machine learning algorithms including k-means clustering and PCA used in your data visualizations.
6. pypdf2: A Pure-Python library built as a PDF toolkit. It is capable of splitting, merging together, cropping, and transforming the pages of PDF files.
7. plotly: An interactive graphing library for making interactive, publication-quality graphs online.
8. numpy: Essential for scientific computing with Python, supports large, multi-dimensional arrays and matrices.
9. seaborn: A Python data visualization library based on matplotlib that provides a high-level interface for drawing attractive and informative statistical graphics.
10. python-multipart: A streaming multipart parser for Python. Used in handling form data, especially for file uploads in web forms.
11. jinja2: A modern and designer-friendly templating language for Python, modeled after Django’s templates. It is used in Flask for rendering the templates.
12. werkzeug: A comprehensive WSGI web application library, it is a dependency of Flask and also directly used for utilities like secure file handling.
13. requests: Allows you to send HTTP/1.1 requests extremely easily, used perhaps for fetching PDFs from URLs.
14. pytest: A framework that makes it easy to write simple tests, can also be used to develop complex functional testing for applications.

## How to Install 
To install these packages, use the following command in your terminal after activating your Python virtual environment:

- bash
pipenv  install Flask matplotlib pandas scikit-learn pypdf2 plotly numpy seaborn python-multipart jinja2 

## How to run
To execute the project, navigate to the project directory and run the following commands:

1. To output a page use command:

        pipenv run python main.py  

2. For Test Cases 

        pipenv run python -m pytest tests/test.py


## Video 

## Code Workflow
Step 1: Starting the Application
To run the project, navigate to the project directory in your terminal and execute the main.py script. This initializes the Flask server, typically accessible via localhost on a specific port, commonly 5000. You can start the server using:

bash
pipenv run python main.py

Once the server is running, you can access the application by opening a web browser and navigating to http://localhost:5000.

Step 2: Home Page Interaction
Upon accessing the application, you land on the home.html page. This page serves as the main interface where you can:

1. Upload PDF files: You can select single or multiple PDF files for upload. To select multiple files, hold the Ctrl key and click on each file you wish to upload.
2. Enter URLs: You can also input URLs pointing to PDFs. To add multiple URLs, click the "Add More URLs" button, which dynamically adds additional text fields for inputting more URLs.

Step 3: Submitting Data
After you have selected your files or entered URLs, click the "Upload and Analyze" button. This action triggers the backend Flask routes in main.py to process the PDFs—either fetched from the URLs or uploaded from your local machine. The application extracts incident data using functions defined in project0.py, specifically:

fetchincidents to retrieve PDFs from URLs.
extractincidents to parse the PDFs and extract relevant data such as dates, incident numbers, locations, and other details.

Step 4: Data Processing and Visualization
Post data extraction, the application performs several analyses:

Clustering Analysis: Using K-means clustering to categorize the data.
Dimensionality Reduction: Applying PCA to transform the data into principal components for visualization.
Data Visualization: Generating three types of visual charts:
Cluster Scatter Plot: Shows clusters of data points.
Bar Graph: Displays the frequency of incidents by ORI.
Bubble Chart: Represents the nature of incidents with varying bubble sizes.

Step 5: Displaying Results
After processing, you are redirected to the charts.html page, where the results are presented. This page displays:

Visualizations: The scatter plot, bar graph, and bubble chart are shown, providing insights into the different dimensions of the incident data.
Data Tables: Accompanying the visualizations, tables display detailed results such as incident ORI frequencies and nature counts.

Step 6: Further Actions
From the results page, you have the option to:

Upload Another File: A button at the bottom of the charts.html page allows you to return to the home.html page to start a new session of data uploads and analysis.

# Functions 

## main.py 

1. convert_to_time(x)
Purpose: Converts a datetime string into a categorized time of day. Parameters:

x (str): A string representing a datetime. Returns:
(str): A string representing one of the time categories ('Morning', 'Afternoon', 'Evening', 'Night', 'Unknown'). Description: This function parses a datetime string to determine the time of day it represents. It categorizes times into morning, afternoon, evening, or night based on the hour. If the datetime string cannot be parsed, it returns 'Unknown'.

2. visualize(date_list, incident_number_list, location_list, nature_list, ori_list)
Purpose: Processes incident data and generates visualizations and HTML tables. Parameters:

date_list (list): Dates of incidents.
incident_number_list (list): Incident numbers.
location_list (list): Locations of incidents.
nature_list (list): Natures of incidents.
ori_list (list): ORI codes. Returns:
(dict): Paths to visualization images and HTML table content. Description: This function creates a DataFrame from provided lists, performs label encoding on categorical data, applies K-means clustering, and uses PCA for dimensionality reduction. It then generates a cluster scatter plot, a bar graph of incident ORI frequencies, and a bubble chart showing nature frequencies. It also converts data into HTML tables for display.

3. index()
Purpose: Serves the home page and handles data upload and URL submission. HTTP Methods: GET, POST Returns:

On GET: Renders home.html.
On POST: Processes uploaded files and URLs, extracts data, generates visualizations, and redirects to result with visualization data. Description: This route handles the landing page where users can upload PDF files or submit URLs. On POST, it processes the input, calls the data extraction and visualization functions, and then redirects to the results page with data.

4. result()
Purpose: Displays the results of the data analysis. Returns:

Renders charts.html with parameters for visualizations and data tables. Description: This route retrieves visualization paths and HTML table content from query parameters and renders the charts.html template. It presents visualizations and detailed data analysis results to the user.

5. main block
Purpose: Configures and runs the Flask application. Description: This block checks if the script is executed as the main program and runs the Flask app with debugging enabled and threading disabled. This setup is typical for development but should be modified for production environments for better security and performance.

## project0.py

1. fetchincidents(url):

Downloads the PDF file from the specified URL.
Parameters: url (string): URL of the PDF file.
Returns: Byte stream of the downloaded PDF.

2. extractincidents(byte_pdf):

Extracts the relevant incident details (Date/Time, Incident Number, Location, Nature, and ORI) from the PDF byte stream.
Parameters: byte_pdf: Byte stream of the PDF.
Returns: Five lists containing the respective fields.

3. column_seperator(line):

Splits a line of text from the PDF into its components: Date/Time, Incident Number, Location, Nature, and ORI.
Parameters: line: The string line from the PDF.
Returns: A tuple containing the extracted fields.

## Templates 

## home.html

# Purpose
home.html serves as the initial user interface for the web application. It provides the functionality for users to upload PDF files directly or input URLs pointing to online PDFs containing incident data. The page is designed to be intuitive and user-friendly, facilitating easy navigation and interaction for a diverse audience.

Structure and Interaction
Header: Displays the title of the application, setting the context for the user.
PDF File Upload: Users can select single or multiple PDF files to upload. Multiple selections are enabled by holding the Ctrl key while selecting files. This allows for batch processing of incident data.
URL Input Field: Accommodates the input of URLs for online PDFs. Users can add multiple URL fields dynamically by clicking the "Add More URLs" button, enhancing the form's flexibility and user interaction.
Submission Button: After files or URLs are selected/inputted, users click the "Upload and Analyze" button to submit their data for processing. The application then handles file retrieval, data extraction, and subsequent analysis.
Styling: The page uses a forest-themed background image and maintains a clean and modern aesthetic with responsive design elements to ensure usability across devices.


## charts.html
# Purpose
charts.html is designed to display the results of the data analysis performed on the uploaded or fetched PDFs. This page visualizes the processed data through various graphical representations and tables, providing users with insights into the incident data in an easily digestible format.

Structure and Interaction
Header: Features a title and a dynamic flash card displaying the last updated time and view count, adding a real-time dynamic component to the page.
Visualization Section:
Cluster Scatter Plot: Visualizes clusters of incident data, allowing users to discern patterns based on the clustering analysis.
Bar Graph: Displays the frequency of incidents by ORI, highlighting which agencies report the most incidents.
Bubble Chart: Shows the frequency of different incident natures with bubble sizes proportional to their frequency, offering an engaging visual representation of the data.
Data Tables: Two HTML tables display detailed tabular data about incident ORI frequencies and the nature of incidents, complementing the visual data representation.
Footer: Contains a button that allows users to return to the home.html page to upload new files or enter new URLs, facilitating continuous interaction and analysis.
Styling: Similar to home.html, the page uses a clean and modern design with responsive elements to ensure it functions well on various devices.

## Technologies Used in both files 
HTML: Structures the result display.
CSS: Styles the visualizations and tables for clarity and aesthetic appeal.
JavaScript: Used to update the time dynamically on the page, adding a live aspect to the static data display.


## Explanation of Visuilizations charts

## Visualization 1: Cluster Scatter Plot
Type of Diagram: Scatter Plot
Purpose: To visualize the clustering of incident data based on multiple attributes to identify patterns and relationships.

Data Columns Used:

Nature_Encoded: Numeric representation of the nature of incidents, encoded from categorical descriptions.
Location_Encoded: Numeric representation of incident locations, encoded from categorical descriptions.
Date_time_quarters_encoded: Time of day encoded into categories like Morning, Afternoon, Evening, and Night based on incident times.
Incident_Number_Encoded: Numeric representation of unique incident numbers.
Description: This scatter plot uses PCA (Principal Component Analysis) for dimensionality reduction, plotting the first two principal components derived from the encoded attributes. Each point in the scatter plot represents an incident, colored based on the cluster it belongs to, determined by K-Means clustering. This visualization helps in understanding how incidents are grouped based on time, location, nature, and specific incident details.

Path : static\pca_scatter_plot.png

## Visualization 2: Bar Graph of Incident ORI Frequency
Type of Diagram: Bar Graph
Purpose: To show the frequency of incidents associated with different ORI (Originating Agency Identifier) codes.
Data Column Used:

Incident ORI: Categorical data indicating the Originating Agency Identifier, which specifies the agency responsible for reporting the incident.
Description: This bar graph displays the frequency of incidents for each ORI code, sorted by the number of occurrences. It provides a clear representation of which agencies are reporting the most incidents, allowing for a straightforward assessment of data distribution across different agencies.

Path : static\bar_plot.png

## Visualization 3: Bubble Chart of Nature Frequency
Type of Diagram: Bubble Chart
Purpose: To visualize the frequency and relative importance of different types of incident natures.
Data Columns Used:

Nature: The categorical description of the nature of the incidents.
Description: The bubble chart plots the frequency of each incident type, with the size of each bubble proportional to the frequency of occurrences. This chart not only shows which types of incidents are most common but also visually emphasizes the relative frequency through bubble size, making it easier to identify major concerns or common incident types.

Path : static\bubble_chart.png

These visualizations collectively provide a comprehensive view of the incident data, helping stakeholders quickly grasp complex datasets and uncover insights that can drive more informed decision-making. Each diagram utilizes specific attributes of the data to highlight different aspects of the incident reports.



## Test Cases 
1. test_visualization_data_processing()
Purpose: This test verifies that the visualize function can accurately process data and generate required visualizations such as scatter plots, bar graphs, and bubble charts.

Functionality:

Ensures that provided data (dates, incident numbers, etc.) is properly transformed into visual formats.
Checks for the creation of specific visualization outputs, confirming the function’s capability to render the necessary graphical representations from the data.

2. test_fetch_incidents_live()
Purpose: Tests the fetchincidents function to confirm it can successfully download and store PDF files from a live URL, ensuring the file is retrieved, stored correctly, and contains data.

Functionality:

Validates successful retrieval of a PDF from an external source, ensuring the file exists and is not empty post-download.
Ensures proper cleanup by removing the downloaded file after the test, maintaining a clean test environment.


## Bugs and Assumptions
1. Data Quantity Assumption:

- Assumes sufficient data points are available for clustering, which can fail if data is inadequate.
- Address by dynamically adjusting cluster numbers based on available data or improving user guidance.

2. External Dependency Assumption:
- Assumes uninterrupted access to external URLs for fetching PDFs, risking failures if URLs are down or unreliable.
- Implement error handling and fallback mechanisms to manage external service interruptions.

3. File Integrity Assumption:
- Assumes downloaded PDFs are not corrupt and are readable, which could disrupt processing if incorrect.
- Incorporate file integrity checks before processing to catch and handle corrupt files.

4. Responsive Design:

- The UI may not display properly on various devices, leading to inconsistent user experiences.
- Implement comprehensive CSS and layout strategies that adapt fluidly to different screen sizes.

5. File Handling Bug:
- Issues in managing temporary files could lead to incorrect file paths or missing files during operations.
- Ensure systematic file management including proper cleanup post-use to prevent residue or path errors.

6. Error Handling Insufficiency:
- Current error handling for network and file operations is inadequate, potentially leading to crashes.
- Strengthen error handling to ensure the application remains stable and responsive under various error conditions.