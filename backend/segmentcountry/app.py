import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table, callback_context
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

# Group data by Classified Column and Country to get publication counts
segment_country_counts = data.groupby(['Classified', 'Country']).size().reset_index(name='Count')

# Create a Treemap chart
fig = px.treemap(
    segment_country_counts, 
    path=['Classified', 'Country'], 
    values='Count', 
    title="Publications by Segment and Country",
    color='Count', 
    color_continuous_scale="Viridis"
)

# Add percentage and count to the labels (shown directly on the chart)
fig.update_traces(textinfo="label+value+percent parent", textfont_size=12)

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container(
    [
        # Title
        html.H1("Trend on Publications by Segments and Country", className="text-center my-4"),
        html.P(
           
            className="text-center text-muted"
        ),

         # Navigation Instructions
        html.Div(
            [
                html.H3("How to Navigate the Treemap:", className="my-3"),
                html.Ul(
                    [
                        html.Li("The treemap visualizes the publication trends by segment and country."),
                        html.Li("Start by exploring the classified segments (e.g., 'Unique to People')."),
                        html.Li("Drill down into specific countries by clicking on a segment."),
                        html.Li(
                            "When you click on a country, a modal will appear, displaying a table of "
                            "reference numbers and titles for publications in that country."
                        ),
                        html.Li(
                            "You can return to the previous level by clicking the breadcrumb navigation "
                            "in the top-left corner of the treemap."
                        ),
                    ],
                    className="text-muted",
                ),
            ],
            className="mb-4",
        ),

        # Treemap Chart
        dcc.Graph(
            id='treemap-chart',
            figure=fig,
            config={"displayModeBar": False},
            style={'height': '120vh', 'width': '100%'}
        ),

        # Modal for displaying country details
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                dbc.ModalBody(
                    dash_table.DataTable(
                        id="details-table",
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

# Callback to handle modal display
@app.callback(
    [Output("modal", "is_open"),
     Output("modal-title", "children"),
     Output("details-table", "data")],
    [Input("treemap-chart", "clickData"),
     Input("close-modal", "n_clicks")],
    [State("modal", "is_open")]
)
def display_modal(click_data, close_clicks, is_open):
    ctx = callback_context
    if ctx.triggered:
        triggered_input = ctx.triggered[0]["prop_id"].split(".")[0]

        if triggered_input == "treemap-chart" and click_data:
            label = click_data['points'][0]['label']  # Country
            parent = click_data['points'][0].get('parent', None)  # Classified

            if label in data['Country'].unique() and parent in data['Classified'].unique():
                # Filter data for the selected country and classified segment
                filtered_data = data[
                    (data['Classified'] == parent) &
                    (data['Country'] == label)
                ]

                # Prepare data for the modal's table
                table_data = [
                    {
                        "Reference_no": f"[{row['Reference_no']}]({row['URL']})" if pd.notna(row['URL']) else row['Reference_no'],
                        "Title": row["Title"]
                    }
                    for _, row in filtered_data.iterrows()
                ]

                return True, f"Details for {label} in {parent}", table_data

        elif triggered_input == "close-modal" and close_clicks:
            return False, None, []

    return is_open, None, []

# Run the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug_mode = os.environ.get("RENDER") is None  # Only debug in local development
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
