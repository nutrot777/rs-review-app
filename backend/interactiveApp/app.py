import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import requests
import tempfile
import certifi
import os

# Load data from Excel file
url = 'https://raw.githubusercontent.com/trial777/combined_selected_RS/main/combined_selected_v3.xlsx'

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

# Prepare the Sunburst data
sunburst_data = data[['Year', 'Country', 'Reference_no', 'Title', 'URL']].copy()
sunburst_data['Count'] = 1  # Add a count column for aggregation

# Group data by Year and Country to get publication counts
publication_counts = sunburst_data.groupby(['Year', 'Country']).size().reset_index(name='Count')

# Calculate total counts for percentages
total_count = publication_counts['Count'].sum()
publication_counts['Percentage'] = (publication_counts['Count'] / total_count * 100).round(2)

# Create the Sunburst chart
fig = px.sunburst(
    publication_counts,
    path=['Year', 'Country'],
    values='Count',
    title="Publications by Country per Year",
    color='Year',
    color_continuous_scale="Viridis"
)

# Update the trace to include percentage and count values in the labels
fig.update_traces(
    textinfo="label+percent entry",  # Show labels and percentages relative to each segment's parent
    insidetextorientation="radial",  # Place text radially for better readability
    hovertemplate=(
        '<b>%{label}</b><br>' +
        'Count: %{value}<br>' +
        'Percentage: %{percentParent:.2%}<extra></extra>'
    )  # Include count and percentage in hover details
)

# Enhance the figure layout for better readability
fig.update_layout(
    title_font=dict(size=24, family="Arial", color="black"),
    margin=dict(t=50, l=50, r=50, b=50),  # Add sufficient margins for elegance
    height=800,  # Make the chart taller
    width=1000,  # Make the chart wider
    paper_bgcolor="rgba(240, 240, 240, 0.9)",  # Light gray background for elegance
    font=dict(family="Arial, sans-serif", size=14, color="black"),  # Legible font settings
)

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container(
    [
        # Add title
        html.H1("Publications by Country per Year", className="my-4 text-center"),

        # Add user instructions
        html.Div(
            [
                html.H3("How to Use This Chart:", className="my-3"),
                html.Ul(
                    [
                        html.Li("Hover over a segment to see publication details like counts and percentages."),
                        html.Li("Click on a year to view the countries within that year."),
                        html.Li("Click on a country to open a table of articles published in that country."),
                        html.Li(
                            [
                                "In the table, click on any ",
                                html.B("Reference Number"),
                                " to open the article's page in a new tab.",
                            ]
                        ),
                    ],
                    className="text-muted",
                ),
            ],
            className="mb-4",  # Add margin below instructions
        ),

        # Add the Sunburst chart
        dcc.Graph(
            id='sunburst-chart',
            figure=fig,
            config={
                "displayModeBar": False,  # Hide the default Plotly toolbar for elegance
                "responsive": True,  # Make it responsive for screen resizing
            },
            style={"height": "800px", "width": "1000px", "margin": "0 auto"}  # Center and adjust size
        ),
        
        # Modal to display country details
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                dbc.ModalBody(
                    dash_table.DataTable(
                        id='details-table',
                        columns=[
                            {"name": "Reference_no", "id": "Reference_no", "presentation": "markdown"},
                            {"name": "Title", "id": "Title"}
                        ],
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left", "padding": "5px"},
                        style_header={"fontWeight": "bold"},
                        markdown_options={"link_target": "_blank"},
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
                ),
            ],
            id="modal",
            size="lg",
            is_open=False,
        ),
    ],
    fluid=True
)

# Callback to open the modal and update table data
@app.callback(
    [Output("modal", "is_open"),
     Output("modal-title", "children"),
     Output("details-table", "data")],
    [Input("sunburst-chart", "clickData"),
     Input("close-modal", "n_clicks")],
    [State("modal", "is_open")]
)
def display_modal(click_data, close_clicks, is_open):
    # Toggle the modal
    if close_clicks or click_data:
        if not is_open:
            if click_data:
                label = click_data['points'][0]['label']
                parent = click_data['points'][0].get('parent', None)

                # If a country is clicked, filter the data
                if parent and not label.isnumeric():
                    filtered_data = sunburst_data[
                        (sunburst_data['Year'] == int(parent)) & (sunburst_data['Country'] == label)
                    ]

                    # Prepare the data for the table
                    table_data = [
                        {"Reference_no": f"[{row['Reference_no']}]({row['URL']})", "Title": row["Title"]}
                        for _, row in filtered_data.iterrows()
                    ]

                    return True, f"Details for {label} ({parent})", table_data

        return False, None, []
    return is_open, None, []


# Run the app
if __name__ == "__main__":
    # Bind the app to the Cloud Run PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    debug_mode = os.environ.get("RENDER") is None  # Only debug in local development
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
