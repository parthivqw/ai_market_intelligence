import pandas as pd
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file. Please add it.")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

# --- MAIN FUNCTION ---
def generate_insights():
    """
    Loads the combined dataset, prepares summaries, sends them to the Groq LLM
    with a clear JSON schema example, and saves the insights.
    """
    print("--- Starting Phase 3: AI-Powered Insight Generation (with JSON Schema) ---")

    # 1. Load the combined dataset
    combined_data_path = os.path.join('data', 'processed', 'combined_market_data.csv')
    try:
        df = pd.read_csv(combined_data_path)
    except FileNotFoundError:
        print(f"Error: Combined data file not found at {combined_data_path}")
        return

    # 2. Prepare the data for the LLM
    app_counts = df['App'].value_counts()
    apps_on_both_platforms = app_counts[app_counts == 2].index.tolist()
    df_filtered = df[df['App'].isin(apps_on_both_platforms)]
    df_filtered = df_filtered[df_filtered['Reviews'] > 0]

    if df_filtered.empty:
        print("Could not find enough comparable data after filtering. Exiting.")
        return

    data_summary = df_filtered.to_json(orient='records')
    print(f"Prepared a summary of {len(df_filtered)} data points for the LLM.")

    # 3. Define the prompt WITH a clear JSON schema example
    # This is the key improvement!
    json_schema_example = """
    [
      {
        "insight_id": "CP-001",
        "insight_type": "Cross-Platform Comparison",
        "title": "Example Title: App Performance on Android vs. iOS",
        "summary": "A detailed explanation of the finding, referencing data.",
        "supporting_data": { "app": "Example App", "android_rating": 4.5, "ios_rating": 4.7 },
        "recommendation": "An actionable business suggestion based on the insight.",
        "confidence_score": 0.9
      }
    ]
    """

    user_prompt = f"""
    You are an expert market analyst for the mobile app industry. Analyze the provided JSON data about mobile apps.
    Your task is to generate 3-5 key market intelligence insights from the data.

    You MUST respond with ONLY a single, valid JSON array that follows the exact schema and structure shown in the example below.
    Do not include any introductory text, markdown formatting, or any other content outside of the JSON array.

    JSON Schema Example:
    {json_schema_example}

    Now, analyze the following data and provide your response:
    {data_summary}
    """

    # 4. Call the Groq LLM API
    print("Sending data to the Groq LLM for analysis...")
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.5, # Lower temp for better schema adherence
            max_tokens=4096,
        )
        
        insights_json_string = response.choices[0].message.content
        insights = json.loads(insights_json_string)

    except json.JSONDecodeError as e:
        print(f"\n--- ERROR: Failed to decode JSON from the LLM response. ---")
        print("The LLM did not return a perfectly formatted JSON object despite the instructions.")
        print("\n--- Raw LLM Response: ---")
        print(insights_json_string)
        print("-----------------------")
        return
    except Exception as e:
        print(f"An error occurred while calling the LLM API: {e}")
        return

    # 5. Save the insights
    output_path = 'insights.json'
    with open(output_path, 'w') as f:
        json.dump(insights, f, indent=4)
    
    print("\n--- Phase 3 Complete ---")
    print(f"Successfully generated {len(insights)} insights.")
    print(f"Insights saved to: {output_path}")

if __name__ == '__main__':
    generate_insights()