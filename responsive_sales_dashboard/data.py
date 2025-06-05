import pandas as pd
import requests
from config import API_URL

def fetch_data(search_text, start_date, end_date):
    print("Calling API with:", search_text, start_date, end_date)  # Debug print
    try:
        
        if start_date and end_date:
            search_text += f" from {start_date} to {end_date}"
        elif start_date:
            search_text += f" from {start_date}"
        elif end_date:
            search_text += f" up to {end_date}"        
        payload = {"query": search_text or ""}
        print("Payload for API:", payload)  # Debug print
        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=payload, headers=headers)
        print("API status code:", response.status_code)

        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)

        if not df.empty:
            df['created_date'] = pd.to_datetime(df['created_date'])
            df['full_name'] = df['first_name'] + ' ' + df['last_name']
            if start_date:
                df = df[df['created_date'] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df['created_date'] <= pd.to_datetime(end_date)]
        return df
    except Exception as e:
        print("API error:", e)
        return pd.DataFrame()