import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("RAPIDAPI_KEY not found in .env file. Please add it.")

API_URL = "https://appstore-scrapper-api.p.rapidapi.com/v1/app-store-api/search"

# --- MAIN FUNCTION ---
def fetch_and_combine_data():
    """
    Loads cleaned Google Play data, fetches corresponding Apple App Store data via API,
    and combines them into a single dataset.
    """
    print("--- Starting Phase 2: API Integration & Data Unification ---")

    google_data_path = os.path.join('data', 'processed', 'google_play_cleaned.csv')
    try:
        google_df = pd.read_csv(google_data_path)
    except FileNotFoundError:
        print(f"Error: Cleaned data file not found at {google_data_path}")
        print("Please run '01_data_cleaning.py' first.")
        return

    top_100_google_apps = google_df.sort_values(by='Installs', ascending=False).head(100)
    print(f"Selected {len(top_100_google_apps)} top Google Play apps to fetch from App Store.")

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
        
        # EXACT parameters that work (from successful test)
        params = {
            "num": "10",
            "lang": "en", 
            "query": app_name,
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
                    
            elif response.status_code == 429:
                print(f"  -> Rate limited. Waiting 5 seconds...")
                time.sleep(5)
                continue  # Retry this request
                
            else:
                print(f"  -> ERROR {response.status_code}: {response.text[:100]}")
                failed_requests += 1

        except Exception as e:
            print(f"  -> Exception: {e}")
            failed_requests += 1

        # Small delay to be nice to the API
        time.sleep(1)
        
        # Progress update every 25 apps
        if (successful_requests + failed_requests) % 25 == 0:
            print(f"\n--- Progress: {successful_requests} successful, {failed_requests} failed ---\n")

    print(f"\n=== FINAL RESULTS ===")
    print(f"Successful requests: {successful_requests}")
    print(f"Failed requests: {failed_requests}")
    print(f"Success rate: {successful_requests/(successful_requests+failed_requests)*100:.1f}%")

    if not app_store_data:
        print("Could not fetch any data from the App Store API.")
        return

    # Create iOS DataFrame
    ios_df = pd.DataFrame(app_store_data)
    print(f"\nSuccessfully fetched data for {len(ios_df)} iOS apps")

    # Create combined dataset
    google_subset_df = top_100_google_apps[['App', 'Category', 'Rating', 'Reviews', 'Price', 'Installs']].copy()
    google_subset_df['Platform'] = 'Android'
    
    # Add missing columns to match iOS data
    google_subset_df['App_ID'] = None
    google_subset_df['URL'] = None
    
    combined_df = pd.concat([google_subset_df, ios_df], ignore_index=True)

    # Save both datasets
    ios_output_path = os.path.join('data', 'processed', 'ios_apps_data.csv')
    ios_df.to_csv(ios_output_path, index=False)
    
    combined_output_path = os.path.join('data', 'processed', 'combined_market_data.csv')
    combined_df.to_csv(combined_output_path, index=False)
    
    print("\n--- Phase 2 Complete ---")
    print(f"iOS data saved to: {ios_output_path}")
    print(f"Combined dataset saved to: {combined_output_path}")
    print(f"Final dataset contains {len(combined_df)} entries ({len(google_subset_df)} Android + {len(ios_df)} iOS)")
    
    # Show sample results
    print("\nSample of fetched iOS apps:")
    print(ios_df[['App', 'Category', 'Rating', 'Reviews', 'Price']].head())


if __name__ == '__main__':
    fetch_and_combine_data()


def test_single_request():
    """Test function to debug API issues"""
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": API_HOST
    }
    
    print("=== Testing API Connection ===")
    print(f"API Key: {RAPIDAPI_KEY[:10]}..." if RAPIDAPI_KEY else "No API Key")
    print(f"API URL: {API_URL}")
    print(f"API Host: {API_HOST}")
    
    # Test 1: Exact parameters from your RapidAPI screenshot for searchApp
    print("\n--- Test 1: SearchApp endpoint with screenshot params ---")
    querystring_1 = {
        "num": "10",
        "lang": "en", 
        "query": "sleep",
        "country": "us"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, params=querystring_1, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        if response.status_code != 200:
            print(f"Full Error Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Try different endpoint - reviews (from your first screenshot)
    print("\n--- Test 2: Reviews endpoint ---")
    reviews_url = "https://appstore-scrapper-api.p.rapidapi.com/v1/app-store-api/reviews"
    querystring_2 = {
        "id": "364709193",
        "sort": "mostRecent", 
        "page": "1",
        "country": "us",
        "lang": "en"
    }
    
    try:
        response = requests.get(reviews_url, headers=headers, params=querystring_2, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Try app detail endpoint (from your second screenshot)  
    print("\n--- Test 3: App Detail endpoint ---")
    detail_url = "https://appstore-scrapper-api.p.rapidapi.com/v1/app-store-api/detail"
    querystring_3 = {
        "lang": "en",
        "id": "553834731",
        "country": "us"
    }
    
    try:
        response = requests.get(detail_url, headers=headers, params=querystring_3, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Simple request with minimal params
    print("\n--- Test 4: Minimal search request ---")
    querystring_4 = {
        "query": "Instagram"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, params=querystring_4, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

def test_api_subscription():
    """Test if API subscription is active"""
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": API_HOST
    }
    
    print("=== Testing API Subscription Status ===")
    
    # Try to hit any endpoint to check subscription
    try:
        response = requests.get(
            "https://appstore-scrapper-api.p.rapidapi.com/v1/app-store-api/search",
            headers=headers,
            params={"query": "test"},
            timeout=10
        )
        
        if response.status_code == 403:
            print("❌ 403 Forbidden - Check your API subscription or key")
        elif response.status_code == 429:
            print("⚠️  429 Rate Limited - You've exceeded your quota")  
        elif response.status_code == 400:
            print("❌ 400 Bad Request - Parameter or endpoint issue")
        else:
            print(f"✅ API responding with status: {response.status_code}")
            
        print(f"Response: {response.text[:300]}")
        
    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == '__main__':
    # The API is working! Run the full data fetch
    fetch_and_combine_data()