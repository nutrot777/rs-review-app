import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import os
import certifi
import ssl
import requests
import tempfile

# Load data from Excel file
url ='https://raw.githubusercontent.com/trial777/combined_selected_RS/main/combined_selected_v3.xlsx'

# Download the file, specifying the CA bundle path directly
response = requests.get(url, verify=certifi.where())

# Check if the request was successful
if response.status_code == 200:
    # Save the content to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".xlsx") as temp_file:
        temp_file.write(response.content)
        temp_file.seek(0)  # Go back to the beginning of the file

        # Load the file into a DataFrame
        data = pd.read_excel(temp_file.name)
else:
    print("Failed to download the file.")

# Convert "Publication Date" to datetime and extract the year
data['Publication Date'] = pd.to_datetime(data['Publication Date'], errors='coerce')
data = data.dropna(subset=['Publication Date'])
data['Year'] = data['Publication Date'].dt.year

# Group data by Year and Classified Column to get publication counts
year_segment_counts = data.groupby(['Year', 'Classified']).size().reset_index(name='Count')

# Create a Stacked Area chart
fig = px.area(year_segment_counts, 
              x='Year', 
              y='Count', 
              color='Classified', 
              title="Trends in Publication Segments over Time",
              line_group='Classified')

# Add text labels for count and percentage
fig.update_traces(text=year_segment_counts['Count'], 
                  texttemplate='%{text} (%{percent:.1f}%)', 
                  hoverinfo="text")

app = dash.Dash(__name__)

#Display in the Dash app
app.layout = html.Div([
    html.H1("Trend on Publications by Segments Over Time", style={'text-align': 'center'}),
    html.P("Hover, Click, Double Click on the legends for more instructions and inlook",
           style={'text-align': 'center', 'font-size': '18px', 'color': 'gray'}),
    dcc.Graph(
        figure=fig,
        style={'height': '90vh', 'width': '85vw'}
    )
])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)