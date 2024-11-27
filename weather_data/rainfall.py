"""
Precipitation readings at weather-station level, updated every five minutes.

These data are collected from automated weather instruments, and is automatically published as soon as it is generated. There could be instances when there are gaps in the data due to technical problems. The data is subject to correction subsequently if necessary.

While every effort has been made to site the instruments in relatively unobstructed areas to provide the best possible indication of the general weather conditions, there are times when this is not possible. The readings from the instruments could thus be influenced by local conditions.
"""
import http.client
import json
import datetime
import os
import urllib.parse 

# API base URL and endpoint
base_url = "api-open.data.gov.sg"
endpoint = "/v2/real-time/api/rainfall"


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
filename = f"rainfall_{file_timestamp}.json"

# Get the script's directory
script_dir = os.path.dirname(__file__)

# Combine directory path with filename to save in the same directory
file_path = os.path.join(script_dir, filename)

# Write the JSON data to a file with the timestamped filename
with open(file_path, "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"Data saved to {file_path} with fetch timestamp: {fetch_timestamp}")

