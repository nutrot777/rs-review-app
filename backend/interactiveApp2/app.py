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

# Group data by Year, Classified Column, and Country to get publication counts
publication_counts = data.groupby(['Year', 'Classified', 'Country']).size().reset_index(name='Count')

# Create the Sunburst chart with Year, Classified Column, and Country
fig = px.sunburst(
    publication_counts, 
    path=['Year', 'Classified', 'Country'], 
    values='Count', 
    title="Publications by Year, Segment, and Country",
    color='Classified',
    color_discrete_map={
        "Unique to Process": "gold",
        "Unique to People": "purple",
        "Unique to Technology": "blue",
        "AllThreeSegments": "green",
        "Process & Technology": "orange",
        "People & Process": "red",
        "People & Technology": "pink",
    },
    maxdepth=3
)

# Adjust the text display for clearer insights
fig.update_traces(
    textinfo="label+value+percent parent",
    hovertemplate=(
        '<b>%{label}</b><br>' +
        'Count: %{value}<br>' +
        'Percentage: %{percentParent:.2%}<extra></extra>'
    )
)

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container(
    [
        # Title
        html.H1(
            "Publications by Year, Segment, and Country", 
            className="text-center my-4"
        ),

                html.Div(
            [
                html.H3("How to Use This Chart:", className="my-3"),
                html.Ul(
                    [
                        html.Li("Hover over a fractions to see publication details like counts and percentages."),
                        html.Li("Click on a year to view the segments/dimensions within that year."),
                        html.Li("Click on a segment to view the countries within that segment."),
                        html.Li("Click on a country to open a table of articles published from that country based on year and segment."),
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


        # Sunburst Chart
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='sunburst-chart',
                    figure=fig,
                    config={"displayModeBar": False},
                    style={'height': '800px', 'width': '100%', 'margin': '0 auto'}
                ),
                width=12
            )
        ),

        # Modal
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
                    dbc.Button(
                        "Close",
                        id="close-modal",
                        className="ms-auto",
                        n_clicks=0
                    )
                ),
            ],
            id="modal",
            size="lg",
            is_open=False,  # Initial state is hidden
        ),
    ],
    fluid=True  # Makes the container responsive
)

@app.callback(
    [Output("modal", "is_open"),
     Output("modal-title", "children"),
     Output("details-table", "data")],
    [Input("sunburst-chart", "clickData"),
     Input("close-modal", "n_clicks")],
    [State("modal", "is_open")]
)
def display_modal(click_data, close_clicks, is_open):
    # Use callback_context from Dash
    ctx = callback_context
    if ctx.triggered:
        triggered_input = ctx.triggered[0]["prop_id"].split(".")[0]

        if triggered_input == "sunburst-chart" and click_data:
            # Extract label (current level) and parent
            label = click_data['points'][0]['label']
            parent = click_data['points'][0].get('parent', None)

            if label in data['Country'].unique() and parent in data['Classified'].unique():
                try:
                    # Get Year from data
                    year = data.loc[
                        (data['Classified'] == parent) & (data['Country'] == label),
                        'Year'
                    ].iloc[0]

                    # Filter data for the modal
                    filtered_data = data[
                        (data['Year'] == year) &
                        (data['Classified'] == parent) &
                        (data['Country'] == label)
                    ]

                    # Prepare table data
# Prepare table data
                    table_data = [
                        {
                            "Reference_no": f"[{row['Reference_no']}]({row['URL']})" if pd.notna(row['URL']) else row['Reference_no'],
                            "Title": row["Title"]
                        }
                        for _, row in filtered_data.iterrows()
                    ]


                    return True, f"Details for {label} ({parent})", table_data

                except IndexError:
                    return is_open, None, []
                except Exception as e:
                    return is_open, None, []

        elif triggered_input == "close-modal" and close_clicks:
            # Close the modal
            return False, None, []

    return is_open, None, []

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    # Only debug in local development (not in production)
    debug_mode = not (os.environ.get("RENDER") or os.environ.get("AWS_DEPLOYMENT"))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
