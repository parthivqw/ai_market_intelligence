import pandas as pd
import numpy as np
import os

print("--- Python script '01_data_cleaning.py' is starting ---")

def clean_google_play_data():
    """
    Loads the raw Google Play Store dataset, cleans it, and saves the processed version.
    """
    # Define file paths
    raw_data_path = os.path.join('data', 'raw', 'googleplaystore.csv')
    processed_data_path = os.path.join('data', 'processed', 'google_play_cleaned.csv')

    print("--- Function 'clean_google_play_data' has been called ---")
    print(f"Attempting to load data from: {raw_data_path}")

    # Load the dataset
    try:
        df = pd.read_csv(raw_data_path)
        print("Successfully loaded the raw CSV file.")
    except FileNotFoundError:
        print(f"Error: The file was not found at {raw_data_path}")
        print("Please make sure 'googleplaystore.csv' is in the 'data/raw/' directory.")
        return

    # This dataset has a known misaligned row. Let's drop it explicitly.
    df.drop(df[df['Category'] == '1.9'].index, inplace=True)

    # 1. Drop duplicates
    df.drop_duplicates(subset=['App'], keep='first', inplace=True)

    # 2. Clean 'Reviews' and convert to numeric
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    df.dropna(subset=['Reviews'], inplace=True)
    df['Reviews'] = df['Reviews'].astype(int)

    # 3. Clean 'Installs' - remove '+' and ',' and convert to numeric
    df['Installs'] = df['Installs'].str.replace('[,+]', '', regex=True)
    df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')
    df.dropna(subset=['Installs'], inplace=True)
    df['Installs'] = df['Installs'].astype(int)

    # 4. Clean 'Price' - remove '$' and convert to numeric
    df['Price'] = df['Price'].str.replace('$', '', regex=False)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Price'].fillna(0, inplace=True)
    df['Price'] = df['Price'].astype(float)

    # 5. Handle 'Rating' - Convert to numeric and fill missing values
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Rating'] = df['Rating'].fillna(df.groupby('Category')['Rating'].transform('mean'))
    df['Rating'].fillna(df['Rating'].mean(), inplace=True)
    df['Rating'] = df['Rating'].round(2)

    # 6. Convert 'Last Updated' to datetime objects
    df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')

    # Drop rows where critical data might still be missing after cleaning
    df.dropna(subset=['Last Updated', 'Category', 'Content Rating'], inplace=True)

    # Create the processed directory if it doesn't exist
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    
    # Save the cleaned dataframe
    df.to_csv(processed_data_path, index=False)
    print("--- Cleaning complete ---")
    print(f"Cleaned data saved to: {processed_data_path}")
    print(f"Original shape was approx (10841, 13). Cleaned shape is now: {df.shape}")

# This is the entry point of the script. It tells Python to run our function.
if __name__ == '__main__':
    print("--- Inside the '__main__' block, preparing to run the function ---")
    clean_google_play_data()

print("--- Python script '01_data_cleaning.py' has finished ---")