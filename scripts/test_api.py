import requests
import os
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

headers = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "appstore-scrapper-api.p.rapidapi.com"
}

API_URL = "https://appstore-scrapper-api.p.rapidapi.com/v1/app-store-api/search"

# Test the exact apps that are failing
failing_apps = ["Google News", "Google+", "Subway Surfers", "Google Play Books", "YouTube"]

print("=== Testing Failing Apps with Different Strategies ===")

for app_name in failing_apps:
    print(f"\n--- Testing: {app_name} ---")
    
    # Strategy 1: Exact working parameters from Test 3
    params1 = {
        "num": "10",
        "lang": "en", 
        "query": app_name,
        "country": "us"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, params=params1, timeout=30)
        print(f"Strategy 1 - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  SUCCESS! Found {len(data)} results")
            if data:
                print(f"  First result: {data[0].get('title')}")
        else:
            # Strategy 2: Try simplified app name
            simplified_name = app_name.replace("Google ", "").replace("Play ", "")
            params2 = {
                "num": "10",
                "lang": "en", 
                "query": simplified_name,
                "country": "us"
            }
            
            response2 = requests.get(API_URL, headers=headers, params=params2, timeout=30)
            print(f"Strategy 2 ({simplified_name}) - Status: {response2.status_code}")
            
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"  SUCCESS with simplified name! Found {len(data2)} results")
                if data2:
                    print(f"  First result: {data2[0].get('title')}")
            else:
                # Strategy 3: Try single word
                single_word = app_name.split()[-1]  # Take last word
                params3 = {
                    "num": "10",
                    "lang": "en", 
                    "query": single_word,
                    "country": "us"
                }
                
                response3 = requests.get(API_URL, headers=headers, params=params3, timeout=30)
                print(f"Strategy 3 ({single_word}) - Status: {response3.status_code}")
                
                if response3.status_code == 200:
                    data3 = response3.json()
                    print(f"  SUCCESS with single word! Found {len(data3)} results")
                    if data3:
                        print(f"  First result: {data3[0].get('title')}")
                else:
                    print(f"  All strategies failed for {app_name}")
                    
    except Exception as e:
        print(f"  Exception: {e}")

# Also test some apps that should work
print("\n\n=== Testing Apps That Should Work ===")
working_apps = ["Instagram", "Facebook", "Twitter", "WhatsApp", "Netflix"]

for app_name in working_apps:
    params = {
        "num": "10",
        "lang": "en", 
        "query": app_name,
        "country": "us"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=30)
        print(f"{app_name}: Status {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  SUCCESS! Found {len(data)} results")
    except Exception as e:
        print(f"{app_name}: Exception {e}")