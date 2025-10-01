import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table, callback_context
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import os
import certifi
import requests, tempfile

# Load data from Excel file
url = 'https://raw.githubusercontent.com/trial777/combined_selected_RS/main/countries_continent_main.xlsx'

# Load the Excel file and ensure necessary columns are present
try:
    # Fetch the Excel file using requests with certifi for SSL verification
    response = requests.get(url, verify=certifi.where())
    response.raise_for_status()  # Raise an error for bad status codes

    # Save the content to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".xlsx") as temp_file:
        temp_file.write(response.content)
        temp_file.seek(0)  # Go back to the beginning of the file

        # Load the file into pandas DataFrame
        data = pd.read_excel(temp_file.name)

    print("Data loaded successfully!")
except requests.exceptions.RequestException as e:
    print(f"Error fetching the Excel file: {e}")

if not {"Continent", "Country", "Reference_no", "Title", "URL"}.issubset(data.columns):
    raise ValueError("The Excel file must contain 'Continent', 'Country', 'Reference_no', 'Title', and 'URL' columns.")

# Group data by Continent and Country for the Sunburst chart
sunburst_data = data.groupby(["Continent", "Country"]).size().reset_index(name="Count")

# Create the Sunburst chart
fig = px.sunburst(
    sunburst_data,
    path=["Continent", "Country"],
    values="Count",
    title="Interactive Distribution of Countries by Continent",
    color="Continent",
    color_discrete_sequence=px.colors.qualitative.Set3,
)

# Add percentage and count to the labels
fig.update_traces(
    textinfo="label+percent entry",
    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percentParent:.2%}",
    insidetextorientation="radial",
    textfont=dict(size=12),
)

# Enhance chart layout
fig.update_layout(
    title_font=dict(size=26, family="Arial, sans-serif", color="#333"),
    margin=dict(t=70, l=50, r=50, b=50),  # Enhanced margins
    height=850,
    width=1100,
    paper_bgcolor="#f8f9fa",  # Light gray background
    font=dict(family="Arial, sans-serif", size=14, color="#333"),
)

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container(
    [
        # Title
        html.H1(
            "Publications by Continent and Countries", 
            className="text-center my-4"
        ),
        
        # Add user instructions
        html.Div(
            [
                html.H3("How to Use This Chart:", className="my-3"),
                html.Ul(
                    [
                        html.Li("Hover over a segment to see publication details like counts and percentages."),
                        html.Li("Click on a continent to view the countries within it."),
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
            className="mb-4 text-left",  # Centered instructions
        ),

        # Sunburst Chart
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id="sunburst-chart",
                    figure=fig,
                    config={"displayModeBar": False},  # Hide the default Plotly toolbar
                    style={"height": "850px", "width": "100%"},
                ),
                width={"size": 10, "offset": 1},  # Center the chart using Bootstrap grid offsets
            )
        ),

        # Modal for displaying country details
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.ModalTitle(id="modal-title", style={"fontWeight": "bold"})
                ),
                dbc.ModalBody(
                    dash_table.DataTable(
                        id="details-table",
                        columns=[
                            {"name": "Reference_no", "id": "Reference_no", "presentation": "markdown"},
                            {"name": "Title", "id": "Title"}
                        ],
                        style_table={"overflowX": "auto", "width": "100%"},
                        style_cell={
                            "textAlign": "left",
                            "padding": "10px",
                            "fontFamily": "Arial, sans-serif",
                            "fontSize": "14px",
                        },
                        style_header={
                            "fontWeight": "bold",
                            "backgroundColor": "#e9ecef",
                            "border": "1px solid #dee2e6",
                        },
                        markdown_options={"link_target": "_blank"},
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close-modal", className="btn btn-danger", n_clicks=0
                    )
                ),
            ],
            id="modal",
            size="lg",
            is_open=False,
        ),
    ],
    fluid=True,
    style={"padding": "20px", "backgroundColor": "#f8f9fa"},
)

# Callback to open the modal and populate the table
@app.callback(
    [Output("modal", "is_open"),
     Output("modal-title", "children"),
     Output("details-table", "data")],
    [Input("sunburst-chart", "clickData"),
     Input("close-modal", "n_clicks")],
    [State("modal", "is_open")]
)
def display_modal(click_data, close_clicks, is_open):
    ctx = callback_context
    if ctx.triggered:
        triggered_input = ctx.triggered[0]["prop_id"].split(".")[0]

        if triggered_input == "sunburst-chart" and click_data:
            label = click_data['points'][0]['label']  # Country
            parent = click_data['points'][0].get('parent', None)  # Continent

            # Ensure clicked segment is a country
            if label in data['Country'].unique() and parent in data['Continent'].unique():
                # Filter data for the selected country
                filtered_data = data[data['Country'] == label]

                # Prepare data for the modal's table
                table_data = [
                    {
                        "Reference_no": f"[{row['Reference_no']}]({row['URL']})" if pd.notna(row['URL']) else row['Reference_no'],
                        "Title": row["Title"]
                    }
                    for _, row in filtered_data.iterrows()
                ]

                return True, f"Details for {label}", table_data

        elif triggered_input == "close-modal" and close_clicks:
            return False, None, []

    return is_open, None, []

# Run the app
if __name__ == "__main__":
    # Bind the app to the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    # Only debug in local development (not in production)
    debug_mode = not (os.environ.get("RENDER") or os.environ.get("AWS_DEPLOYMENT"))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)