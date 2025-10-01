from flask import Flask, render_template, jsonify, send_file
import pandas as pd
import certifi
import requests
import tempfile
import io
from urllib.parse import quote, unquote
import os

app = Flask(__name__)

# Load the Excel file
url = 'https://raw.githubusercontent.com/trial777/combined_selected_RS/main/combined_selected_v3.xlsx'

try:
    response = requests.get(url, verify=certifi.where())
    response.raise_for_status()

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file.seek(0)
        data = pd.read_excel(temp_file.name)

    print("Data loaded successfully!")
except Exception as e:
    print(f"Error: {e}")
    raise

# Map classified values to URL-safe identifiers
classified_url_map = {
    "Unique to Process": "unique-process",
    "Unique to People": "unique-people",
    "Unique to Technology": "unique-technology",
    "AllThreeSegments": "all-three",
    "People & Process": "people-process",
    "People & Technology": "people-technology",
    "Process & Technology": "process-technology"
}
url_to_classified = {v: k for k, v in classified_url_map.items()}

# Group data by 'Classified'
grouped_data = data.groupby("Classified")

@app.route('/<classified_url>')
def modal(classified_url):
    classified_value = url_to_classified.get(unquote(classified_url))
    if not classified_value or classified_value not in grouped_data.groups:
        return jsonify({"error": "Invalid classified value."}), 404

    filtered_data = grouped_data.get_group(classified_value)
    modal_data = filtered_data[["Reference_no", "Title", "URL"]].to_dict(orient="records")

    # Count and percentage calculations
    classified_count = len(filtered_data)
    percentage = round((classified_count / len(data)) * 100, 2)

    print(f"DEBUG: classified_url = {classified_url}")  # Add debug print

    return render_template(
        'modal.html',
        classified_url=classified_url,  # Pass this variable
        classified_value=classified_value,
        modal_data=modal_data,
        classified_count=classified_count,
        total_count=len(data),
        percentage=percentage
    )


@app.route('/download/<classified_url>')
def download_excel(classified_url):
    """
    Route to download an Excel file for a specific 'Classified' value.
    """
    # Decode the classified_url and map it to the original Classified value
    classified_value = url_to_classified.get(unquote(classified_url))
    print(f"Received classified_url: {classified_url}")  # Debug log
    print(f"Mapped classified_value: {classified_value}")  # Debug log
    
    if not classified_value or classified_value not in grouped_data.groups:
        return jsonify({"error": "Invalid classified value."}), 404

    # Get filtered data for the classified value
    filtered_data = grouped_data.get_group(classified_value)

    # Save the filtered data to an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        filtered_data.to_excel(writer, index=False, sheet_name="Data")
    output.seek(0)

    # Generate a safe filename
    safe_filename = f"{classified_url}.xlsx"

    return send_file(
        output,
        as_attachment=True,
        download_name=safe_filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# Run the app
if __name__ == "__main__":
    # Bind the app to the Cloud Run PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)