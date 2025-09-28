import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file.")

client = OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

def generate_creative_content():
    """
    Uses insights from our D2C analysis to prompt an LLM for creative
    marketing content (ad headlines and an SEO meta description).
    """
    print("--- Starting Phase 5, Part 2: AI Creative Generation ---")

    insights_path = os.path.join('phase5_extension', 'd2c_insights.json')
    try:
        with open(insights_path, 'r') as f:
            insights = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{insights_path}' not found. Please run '01_d2c_analysis.py' first.")
        return

    best_campaign = insights['best_roas_campaign']
    seo_opportunity = insights['top_seo_opportunity']
    
    best_campaign_insight = (f"The best performing ad campaign ('{best_campaign['id']}' on {best_campaign['channel']}) had a massive ROAS of {best_campaign['roas']}.")
    seo_opportunity_insight = (f"The SEO category '{seo_opportunity['category']}' has a high search volume but our ranking is low.")

    # --- Generate Ad Headlines ---
    print(f"\n📝 Generating Ad Headlines...")
    ad_headline_prompt = f"You are an expert copywriter. Based on the following insight, write 3 catchy ad headlines for {best_campaign['channel']}.\n\nInsight: {best_campaign_insight}"
    
    try:
        # FIXED: Updated model name
        response = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role": "user", "content": ad_headline_prompt}], temperature=0.8, max_tokens=200)
        ad_headlines = response.choices[0].message.content
        print("--- Generated Ad Headlines ---")
        print(ad_headlines)
    except Exception as e:
        print(f"An error occurred: {e}")

    # --- Generate SEO Meta Description ---
    print(f"\n📝 Generating SEO Meta Description...")
    seo_prompt = f"You are an expert SEO copywriter. Based on this insight, write an SEO meta description for the '{seo_opportunity['category']}' category, under 160 characters.\n\nInsight: {seo_opportunity_insight}"
    
    try:
        # FIXED: Updated model name
        response = client.chat.completions.create(model="openai/gpt-oss-120b", messages=[{"role": "user", "content": seo_prompt}], temperature=0.7, max_tokens=100)
        seo_description = response.choices[0].message.content
        print("\n--- Generated SEO Meta Description ---")
        print(seo_description)
        
        # Save creative outputs to a file for the Streamlit app
        creative_outputs = {"ad_headlines": ad_headlines, "seo_description": seo_description}
        with open(os.path.join('phase5_extension', 'd2c_creative_outputs.json'), 'w') as f:
            json.dump(creative_outputs, f, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")

    print("\n\n--- Phase 5 Complete ---")

if __name__ == '__main__':
    generate_creative_content()