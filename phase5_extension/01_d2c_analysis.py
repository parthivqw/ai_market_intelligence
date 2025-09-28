import pandas as pd
import os
import json

def analyze_d2c_data():
    """
    Loads D2C data, calculates metrics, and saves key findings to a JSON file,
    ensuring all data types are JSON serializable.
    """
    print("--- Starting Phase 5: D2C Funnel & SEO Analysis ---")

    data_path = os.path.join('phase5_extension', 'Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx')
    df = pd.read_excel(data_path)
    print("Successfully loaded D2C dataset from Excel file.")

    # Calculations
    df['ROAS'] = (df['revenue_usd'] / df['spend_usd'].replace(0, 1)).round(2)
    df['CAC'] = (df['spend_usd'] / df['first_purchase'].replace(0, 1)).round(2)
    
    # Identify Key Insights
    best_roas_campaign = df.sort_values(by='ROAS', ascending=False).iloc[0]
    df_seo = df[df['avg_position'] > 3].copy()
    best_seo_opportunity = df_seo.sort_values(by='monthly_search_volume', ascending=False).iloc[0]

    print("\n--- 💡 Key Business Insights ---")
    print(f"\n🏆 Best ROAS Campaign: '{best_roas_campaign['campaign_id']}' (ROAS: {best_roas_campaign['ROAS']})")
    print(f"📈 Top SEO Opportunity: '{best_seo_opportunity['seo_category']}' (Volume: {best_seo_opportunity['monthly_search_volume']}, Position: {best_seo_opportunity['avg_position']})")

    # --- NEW: Convert NumPy types to standard Python types for JSON compatibility ---
    insights_to_save = {
        "best_roas_campaign": {
            "id": str(best_roas_campaign['campaign_id']), # Convert to string
            "roas": float(best_roas_campaign['ROAS']), # Convert to float
            "revenue": float(best_roas_campaign['revenue_usd']), # Convert to float
            "spend": float(best_roas_campaign['spend_usd']), # Convert to float
            "channel": str(best_roas_campaign['channel']) # Convert to string
        },
        "top_seo_opportunity": {
            "category": str(best_seo_opportunity['seo_category']), # Convert to string
            "search_volume": int(best_seo_opportunity['monthly_search_volume']), # Convert to int
            "avg_position": float(best_seo_opportunity['avg_position']) # Convert to float
        }
    }

    insights_output_path = os.path.join('phase5_extension', 'd2c_insights.json')
    with open(insights_output_path, 'w') as f:
        json.dump(insights_to_save, f, indent=4)
    
    print(f"\n--- Analysis complete. Key insights saved to '{insights_output_path}' ---")

if __name__ == '__main__':
    analyze_d2c_data()