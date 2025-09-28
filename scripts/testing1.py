import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
API_URL = "https://appstore-scrapper-api.p.rapidapi.com/v1/app-store-api/search"

def fetch_and_combine_data():
    """Minimal working version based on successful test"""
    print("--- Starting Phase 2: API Integration & Data Unification ---")

    # Load Google Play data
    google_data_path = os.path.join('data', 'processed', 'google_play_cleaned.csv')
    try:
        google_df = pd.read_csv(google_data_path)
    except FileNotFoundError:
        print(f"Error: File not found at {google_data_path}")
        return

    top_100_google_apps = google_df.sort_values(by='Installs', ascending=False).head(10)  # Start with just 10 for testing
    print(f"Testing with {len(top_100_google_apps)} apps first")

    # Headers - EXACTLY like the working test
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "appstore-scrapper-api.p.rapidapi.com"
    }

    app_store_data = []
    successful_requests = 0
    failed_requests = 0

    for index, row in top_100_google_apps.iterrows():
        app_name = row['App']
        print(f"Querying API for: {app_name}...")
        
        # EXACT parameters from working test
        params = {
            "num": "10",
            "lang": "en", 
            "query": app_name,  # Use app_name directly, no cleaning
            "country": "us"
        }

        try:
            # EXACT request format from working test
            response = requests.get(API_URL, headers=headers, params=params, timeout=30)
            print(f"  -> Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  -> Found {len(data)} results")
                
                if data:  # data is a list directly
                    ios_app = data[0]  # Take first result
                    app_store_data.append({
                        'App': ios_app.get('title'),
                        'Category': ios_app.get('primaryGenreName', 'Unknown'),
                        'Rating': ios_app.get('averageUserRating', 0),
                        'Reviews': ios_app.get('userRatingCount', 0),
                        'Price': ios_app.get('price', 0.0),
                        'App_ID': ios_app.get('id'),
                        'URL': ios_app.get('url'),
                        'Installs': None,
                        'Platform': 'iOS'
                    })
                    print(f"  -> SUCCESS! Found '{ios_app.get('title')}'")
                    successful_requests += 1
                else:
                    print(f"  -> No results for {app_name}")
                    failed_requests += 1
            else:
                print(f"  -> ERROR: {response.text}")
                failed_requests += 1

        except Exception as e:
            print(f"  -> Exception: {e}")
            failed_requests += 1

        time.sleep(1)  # Short delay

    print(f"\nResults: {successful_requests} success, {failed_requests} failed")
    
    if app_store_data:
        ios_df = pd.DataFrame(app_store_data)
        print(f"Successfully fetched {len(ios_df)} iOS apps")
        
        # Save just iOS data for now
        output_path = os.path.join('data', 'processed', 'ios_apps_test.csv')
        ios_df.to_csv(output_path, index=False)
        print(f"iOS data saved to: {output_path}")
        
        # Show sample of results
        print("\nSample results:")
        print(ios_df[['App', 'Rating', 'Reviews']].head())
    else:
        print("No data fetched!")

if __name__ == '__main__':
    fetch_and_combine_data()