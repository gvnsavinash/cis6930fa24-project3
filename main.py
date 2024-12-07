from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
import project0
from project0 import *
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import numpy as np
from matplotlib.patches import Circle
from sklearn.preprocessing import MinMaxScaler


import matplotlib
from sklearn.decomposition import PCA
matplotlib.use('Agg')

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


def convert_to_time(x):
    """
    Converts a given datetime string to a time of day category.

    This function takes a datetime string as input and converts it to a 
    specific time of day category: 'Morning', 'Afternoon', 'Evening', or 'Night'.
    If the input string cannot be converted to a datetime object, it returns 'Unknown'.

    Parameters:
    x (str): A string representing a datetime.

    Returns:
    str: A string representing the time of day category:
         - 'Morning' for hours between 5 AM and 12 PM (exclusive)
         - 'Afternoon' for hours between 12 PM and 5 PM (exclusive)
         - 'Evening' for hours between 5 PM and 9 PM (exclusive)
         - 'Night' for hours between 9 PM and 5 AM (inclusive)
         - 'Unknown' if the input string cannot be parsed as a datetime
    """
    try:
        dt = pd.to_datetime(x)
        if 5 <= dt.hour < 12:
            return 'Morning'
        elif 12 <= dt.hour < 17:
            return 'Afternoon'
        elif 17 <= dt.hour < 21:
            return 'Evening'
        else:
            return 'Night'
    except ValueError:
        return 'Unknown'  




def visualize(date_list, incident_number_list, location_list, nature_list, ori_list):
    """
    Visualizes incident data using various plots and encodings.
    Parameters:
    date_list (list): List of dates and times of incidents.
    incident_number_list (list): List of incident numbers.
    location_list (list): List of locations where incidents occurred.
    nature_list (list): List of the nature or type of incidents.
    ori_list (list): List of ORI (Originating Agency Identifier) codes for incidents.
    Returns:
    dict: A dictionary containing paths to the generated plots and HTML tables:
        - 'scatter': Path to the PCA scatter plot image.
        - 'bar': Path to the bar plot image showing Incident ORI frequency.
        - 'bubble': Path to the packed bubble chart image showing nature frequencies.
        - 'Incident_ORI_html': HTML table of Incident ORI frequencies.
        - 'nature_counts_html': HTML table of nature frequencies.
    The function performs the following steps:
    1. Creates a DataFrame from the input lists.
    2. Encodes categorical data (Nature, Location, Date/Time, Incident Number) using Label Encoding.
    3. Applies K-Means clustering to the encoded data.
    4. Uses PCA for dimensionality reduction and creates a scatter plot of the clusters.
    5. Generates a bar plot showing the frequency of Incident ORI codes.
    6. Creates a packed bubble chart to visualize the frequency of different natures of incidents.
    7. Converts frequency data to HTML tables for display in a web template.
    """
    # Create DataFrame
    df = pd.DataFrame({
        'Date / Time': date_list,
        'Incident Number': incident_number_list,
        'Location': location_list,
        'Nature': nature_list,
        'Incident ORI': ori_list
    })

    #print("dataframe shape", df.shape)
    #print("Set of Incident ORI", set(df['Incident ORI']))

    # Label Encoding
    nature_le = LabelEncoder()
    df['Nature_Encoded'] = nature_le.fit_transform(df['Nature'])

    # Location Encoding
    location_le = LabelEncoder()
    df['Location_Encoded'] = location_le.fit_transform(df['Location'])

    # df['Date_time_quarters_encoded'] = df['Date / Time'].apply(lambda x: 'Morning' if 5 <= pd.to_datetime(x).hour < 12 else 'Afternoon' if 12 <= pd.to_datetime(x).hour < 17 else 'Evening' if 17 <= pd.to_datetime(x).hour < 21 else 'Night')
    # Date Encoding
    df['Date_time_quarters_encoded'] = df['Date / Time'].apply(convert_to_time)
    date_le = LabelEncoder()
    df['Date_time_quarters_encoded'] = date_le.fit_transform(df['Date_time_quarters_encoded'])

    # Incident Number Encoding
    incident_le = LabelEncoder()
    df['Incident_Number_Encoded'] = incident_le.fit_transform(df['Incident Number'])

    # K-Means Clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    df['Cluster'] = kmeans.fit_predict(df[['Nature_Encoded', 'Location_Encoded', 'Date_time_quarters_encoded', 'Incident_Number_Encoded']])

    # PCA for dimensionality reduction

    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(df[['Nature_Encoded', 'Location_Encoded', 'Date_time_quarters_encoded', 'Incident_Number_Encoded']])
    df['PCA1'] = pca_components[:, 0]
    df['PCA2'] = pca_components[:, 1]

    # Scatter Plot with PCA components
    plt.figure(figsize=(10, 6))
    plt.scatter(df['PCA1'], df['PCA2'], c=df['Cluster'], cmap='viridis')
    plt.title('Incident Clusters (PCA)')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    pca_scatter_path = os.path.join(app.config['STATIC_FOLDER'], 'pca_scatter_plot.png')
    plt.savefig(pca_scatter_path)
    plt.close()
    
    # Bar Plot

    Incident_ORI = df['Incident ORI'].value_counts().sort_values(ascending=True)
    plt.figure(figsize=(12, 8))  # Increased size for readability
    Incident_ORI.plot(kind='barh', color='skyblue')
    plt.title('Incident ORI Frequency')
    plt.xlabel('Frequency')
    plt.ylabel('Incident ORI')
    plt.tight_layout()  # Adjust layout to make sure labels/axes are not cut off
    bar_path = os.path.join(app.config['STATIC_FOLDER'], 'bar_plot.png')
    plt.savefig(bar_path)
    plt.close()

    Incident_ORI = df['Incident ORI'].value_counts().reset_index()
    Incident_ORI.columns = ['Incident ORI', 'Count']  # Renaming columns immediately after resetting index

    # Convert to HTML for display in the template
    Incident_ORI_html = Incident_ORI.to_html(classes="table table-striped", border=0, index=False)

    # Packed Bubble Chart
    df = df.head(100)
    nature_counts = df['Nature'].value_counts().reset_index()
    nature_counts.columns = ['Nature', 'Frequency']

    scaler = MinMaxScaler(feature_range=(100, 1000))  # Scale between 100 and 1000 for visualization purposes
    nature_counts['Scaled Frequency'] = scaler.fit_transform(nature_counts[['Frequency']])

    nature_counts_html = nature_counts.to_html(classes="table table-striped", border=0, index=False)

    # Initialize plot
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')  

    np.random.seed(0)
    points = np.random.rand(len(nature_counts), 2) * 100

    def check_overlap(circles, new_circle):
        for circle in circles:
            distance = np.sqrt((circle[0] - new_circle[0])**2 + (circle[1] - new_circle[1])**2)
            if distance < (circle[2] + new_circle[2]):
                return True
        return False

    circles = []
    for _, row in nature_counts.iterrows():
        x, y = np.random.rand(2) * 100
        size = np.sqrt(row['Scaled Frequency'])
        new_circle = [x, y, size / 2]  # x, y, radius
        while check_overlap(circles, new_circle):
            x, y = np.random.rand(2) * 100
            new_circle = [x, y, size / 2]
        circles.append(new_circle)
        circle = Circle((x, y), size / 2, alpha=0.5, color=np.random.rand(3,), edgecolor='black')
        ax.add_artist(circle)
        plt.text(x, y, row['Nature'], horizontalalignment='center', verticalalignment='center', fontsize=9)

    plt.title('Packed Bubble Chart of Nature Frequencies')
    plt.show()


    bubble_chart_path = os.path.join('static', 'bubble_chart.png')
    plt.savefig(bubble_chart_path)
    plt.close()

    return {
        'scatter': 'pca_scatter_plot.png',
        'bar': 'bar_plot.png',
        'bubble': 'bubble_chart.png',
        'Incident_ORI_html': Incident_ORI_html ,
        'nature_counts_html': nature_counts_html
    }






@app.route('/', methods=['GET', 'POST'])
def index():
    """
Handle the index route for the web application. This function processes both GET and POST requests.
For GET requests:
    - Renders the 'home.html' template.
For POST requests:
    - Retrieves lists of URLs and files from the form data.
    - Initializes lists to collect data for dates, incident numbers, locations, natures, and ORIs.
    - Processes each uploaded file:
        - Reads the file content.
        - Extracts incident data from the PDF content.
        - Extends the respective lists with the extracted data.
    - Processes each URL:
        - Fetches the PDF content from the URL.
        - Reads the PDF content.
        - Extracts incident data from the PDF content.
        - Extends the respective lists with the extracted data.
        - Removes the temporary file used to store the PDF content.
    - If any data was extracted:
        - Generates visualizations based on the collected data.
        - Redirects to the 'result' route with the visualizations as query parameters.
    - If no data was extracted, proceeds to render the 'home.html' template.
Returns:
    - For GET requests: Renders the 'home.html' template.
    - For POST requests: Redirects to the 'result' route if data was extracted, otherwise renders the 'home.html' template.
"""
    if request.method == 'POST':
        urls = request.form.getlist('urls')
        files = request.files.getlist('files')

        # Lists to collect data
        date_list = []
        incident_number_list = []
        location_list = []
        nature_list = []
        ori_list = []

        # Process uploaded files
        for file in files:
            if file and file.filename != '':
                pdf_data = file.read()
                extracted_data = extractincidents(pdf_data)
                date_list.extend(extracted_data[0])
                incident_number_list.extend(extracted_data[1])
                location_list.extend(extracted_data[2])
                nature_list.extend(extracted_data[3])
                ori_list.extend(extracted_data[4])

        # Process URLs
        for url in urls:
            if url:
                temp_pdf_path = fetchincidents(url)
                with open(temp_pdf_path, 'rb') as pdf_file:
                    pdf_data = pdf_file.read()
                extracted_data = extractincidents(pdf_data)
                date_list.extend(extracted_data[0])
                incident_number_list.extend(extracted_data[1])
                location_list.extend(extracted_data[2])
                nature_list.extend(extracted_data[3])
                ori_list.extend(extracted_data[4])
                # Clean up the temporary file
                os.remove(temp_pdf_path)

        print("info extracted")

        if date_list:
            visualizations = visualize(date_list, incident_number_list, location_list, nature_list, ori_list)
            print("visulization done")
            return redirect(url_for('result', **visualizations))
        
        print("going to render")

    return render_template('home.html')



@app.route('/result')
def result():
    """
    Handles the result view for the web application.

    This function retrieves various parameters from the request arguments,
    including 'scatter', 'bar', 'bubble', 'Incident_ORI_html', and 'nature_counts_html'.
    It then renders the 'charts.html' template with these parameters.

    Parameters:
    - scatter (str): The scatter plot data passed as a query parameter.
    - bar (str): The bar chart data passed as a query parameter.
    - bubble (str): The bubble chart data passed as a query parameter.
    - Incident_ORI_html (str): HTML content related to Incident ORI, passed as a query parameter. Defaults to an empty string if not provided.
    - nature_counts_html (str): HTML content related to nature counts, passed as a query parameter. Defaults to an empty string if not provided.

    Returns:
    - A rendered HTML template 'charts.html' with the provided parameters.
    """
    scatter = request.args.get('scatter')
    bar = request.args.get('bar')
    bubble = request.args.get('bubble')
    Incident_ORI_html = request.args.get('Incident_ORI_html', '')  
    nature_counts_html = request.args.get('nature_counts_html', '')
    return render_template('charts.html', scatter=scatter, bar=bar, bubble=bubble, Incident_ORI_html=Incident_ORI_html, nature_counts_html=nature_counts_html)

if __name__ == '__main__':
    app.run(debug=True, threaded=False)  