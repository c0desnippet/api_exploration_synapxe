"""
Provides minute-by-minute wind speed readings from different weather stations across Singapore, updated every five minutes.

This data is collected from automated weather instruments and is published as soon as it is generated. Due to technical issues, there may occasionally be gaps in the data, which is subject to subsequent correction if necessary.

Efforts have been made to locate instruments in relatively unobstructed areas to capture general weather conditions accurately. However, in certain locations, readings may be influenced by local conditions.

The wind speed observations refer to the mean wind speed measured over a 10-minute period and are available at 1-minute resolution.
"""
import http.client
import json
import datetime
import os
import urllib.parse

# API base URL and endpoint
base_url = "api-open.data.gov.sg"
endpoint = "/v2/real-time/api/wind-speed"

# Query parameters
query_params = {
    "date": "2024-11-11",  # Replace with your desired date
    "paginationtoken": "string"  # Replace with your token
}

# Encode query parameters
encoded_params = urllib.parse.urlencode(query_params)

# Create the full URL with query parameters
url_with_params = f"{endpoint}?{encoded_params}"

# Connect to the API
conn = http.client.HTTPSConnection(base_url)
conn.request("GET", url_with_params)

# Fetch the response
res = conn.getresponse()
data = res.read()

# Decode the JSON data
json_data = json.loads(data.decode("utf-8"))

# Add a timestamp for when the data was fetched
fetch_timestamp = datetime.datetime.now().isoformat()
json_data['fetchTimestamp'] = fetch_timestamp

# Format the timestamp for use in the filename
file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"wind_speed_{file_timestamp}.json"

# Get the script's directory
script_dir = os.path.dirname(__file__)

# Combine directory path with filename to save in the same directory
file_path = os.path.join(script_dir, filename)

# Write the JSON data to a file with the timestamped filename
with open(file_path, "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"Data saved to {file_path} with fetch timestamp: {fetch_timestamp}")

