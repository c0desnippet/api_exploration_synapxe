import time
import datetime
from pytrends.request import TrendReq

# Initialize pytrends
pytrend = TrendReq(retries=3)

# Build payload for the past 7 days, sg region searches, and for this specific list of medicines
pytrend.build_payload(kw_list=['paracetamol', 'aspirin', 'ibuprofen', 'antibiotics'], geo='SG', timeframe='now 7-d')

# Fetch data
time.sleep(10)
df = pytrend.interest_over_time()

# Check if the dataframe has data
if not df.empty:
    # Remove the 'isPartial' column if it exists
    if 'isPartial' in df.columns:
        df = df.drop(columns=['isPartial'])
    
    # Group by date and sum hourly data to get daily totals
    df_daily = df.resample('D').sum()
    
    # Sort by date in descending order
    df_daily = df_daily.sort_index(ascending=False)
    
    # Convert the index (dates) to string format as 'YYYY-MM-DD'
    df_daily.index = df_daily.index.strftime('%Y-%m-%d')
    
    # Output the daily data to a readable JSON file
    file_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file_path = f"google_trends_{file_timestamp}.json"
    df_daily.to_json(json_file_path, orient='index', indent=4)
    
    print(f"Data successfully saved to {json_file_path}")
else:
    print("No data returned.")