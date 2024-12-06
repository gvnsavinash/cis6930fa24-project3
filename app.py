from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
import project0
from project0 import *
import database
from database import *
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Configure Matplotlib to use the 'Agg' backend, suitable for non-interactive environments
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

def cluster_and_visualize(date_list, incident_number_list, location_list, nature_list, ori_list):
    # Create DataFrame
    df = pd.DataFrame({
        'Date / Time': date_list,
        'Incident Number': incident_number_list,
        'Location': location_list,
        'Nature': nature_list,
        'Incident ORI': ori_list
    })

    print("dataframe shape", df.shape)

    # Label Encoding
    nature_le = LabelEncoder()
    df['Nature_Encoded'] = nature_le.fit_transform(df['Nature'])

    #label encoding
    location_le = LabelEncoder()
    df['Location_Encoded'] = location_le.fit_transform(df['Location'])

    # dates
    df['Date_time_quarters_encoded'] = df['Date / Time'].apply(lambda x: 'Morning' if 5 <= pd.to_datetime(x).hour < 12 else 'Afternoon' if 12 <= pd.to_datetime(x).hour < 17 else 'Evening' if 17 <= pd.to_datetime(x).hour < 21 else 'Night')

    # Date Encoding
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
    

    # # Scatter Plot
    # plt.figure(figsize=(10, 6))
    # plt.scatter(df['Nature_Encoded'], df['Incident_Number_Encoded'], c=df['Cluster'], cmap='viridis')
    # plt.title('Incident Clusters')
    # plt.xlabel('Nature_Encoded')
    # plt.ylabel('Location_Encoded')
    # scatter_path = os.path.join(app.config['STATIC_FOLDER'], 'scatter_plot.png')
    # plt.savefig(scatter_path)
    # plt.close()

    # Bar Plot
    plt.figure(figsize=(10, 6))
    df['Nature'].value_counts().plot(kind='barh')
    plt.title('Nature Frequency')
    plt.xlabel('Nature')
    plt.ylabel('Frequency')
    bar_path = os.path.join(app.config['STATIC_FOLDER'], 'bar_plot.png')
    plt.savefig(bar_path)
    plt.close()

    # Pie Chart
    plt.figure(figsize=(8, 8))
    df['Cluster'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title('Cluster Distribution')
    pie_path = os.path.join(app.config['STATIC_FOLDER'], 'pie_chart.png')
    plt.savefig(pie_path)
    plt.close()

    return {
        'scatter': 'scatter_plot.png',
        'bar': 'bar_plot.png',
        'pie': 'pie_chart.png'
    }

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         url = request.form.get('url')
#         pdf_path = None

#         if url:
#             pdf_path = project0.fetchincidents(url)
#         elif 'file' in request.files:
#             file = request.files['file']
#             if file and file.filename != '':
#                 # filename = secure_filename(file.filename)
#                 # pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 # file.save(pdf_path)
#                 pdf_path =file.read()
                

#         if pdf_path:
#             date_list, incident_number_list, location_list, nature_list, ori_list = extractincidents(pdf_path)
#             print(date_list, incident_number_list, location_list, nature_list, ori_list)
#             # db_conn = database.createdb()
#             # database.populatedb(db_conn, date_list, incident_number_list, location_list, nature_list, ori_list)
#             # db_conn.close()

#             visualizations = cluster_and_visualize(date_list, incident_number_list, location_list, nature_list, ori_list)
#             return redirect(url_for('result', **visualizations))

#     return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = request.form.getlist('urls')  # Handles multiple URLs
        files = request.files.getlist('files')  # Handles multiple files

        # Initialize lists to collect all data from each PDF
        date_list = []
        incident_number_list = []
        location_list = []
        nature_list = []
        ori_list = []

        for file in files:
            if file and file.filename != '':
                pdf_data = file.read()
                dates, incidents, locations, natures, oris = extractincidents(pdf_data)
                date_list.extend(dates[1:])
                incident_number_list.extend(incidents[1:])
                location_list.extend(locations[1:])
                nature_list.extend(natures[1:])
                ori_list.extend(oris[1:])

        for url in urls:
            if url:
                pdf_data = fetchincidents(url)
                dates, incidents, locations, natures, oris = extractincidents(pdf_data)
                date_list.extend(dates[1:])
                incident_number_list.extend(incidents[1:])
                location_list.extend(locations[1:])
                nature_list.extend(natures[1:])
                ori_list.extend(oris[1:])

        if date_list:
            visualizations = cluster_and_visualize(date_list, incident_number_list, location_list, nature_list, ori_list)
            print("all data", date_list, incident_number_list, location_list, nature_list, ori_list)
            print("ength", len(date_list), len(incident_number_list), len(location_list), len(nature_list), len(ori_list))
            return redirect(url_for('result', **visualizations))

    return render_template('index.html')



@app.route('/result')
def result():
    scatter = request.args.get('scatter')
    bar = request.args.get('bar')
    pie = request.args.get('pie')
    return render_template('result.html', scatter=scatter, bar=bar, pie=pie)

if __name__ == '__main__':
    app.run(debug=True, threaded=False)  # Run with threading disabled for compatibility
