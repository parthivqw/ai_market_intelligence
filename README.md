AI-Powered Market Intelligence System
An end-to-end AI system that ingests, analyzes, and generates strategic insights from cross-platform app market data, presented in an interactive dashboard.

(Note: You will need to replace the URL above with a live link to your screenshot. You can upload your dashboard image to a service like Imgur to get a link.)

🚀 Key Features
Automated Data Pipeline: Ingests and cleans data from a raw CSV (googleplaystore.csv) and a live API (App Store Scraper).

Cross-Platform Analysis: Unifies Android and iOS app data into a single dataset for powerful market comparison.

AI-Powered Insights: Uses a Large Language Model (Groq) to generate strategic market insights from the combined data.

Interactive Dashboard: A user-friendly Streamlit application to visualize insights and explore the data.

Adaptable Pipeline (Phase 5): The system is repurposed to analyze a D2C e-commerce dataset, calculating key business KPIs.

Creative AI Generation (Phase 5): Generates marketing ad copy and SEO meta descriptions based on D2C data analysis.

🛠️ How to Run
1. Prerequisites
Python 3.9+

Git

2. Setup
Clone the Repository:

git clone [https://github.com/parthivqw/ai_market_intelligence.git](https://github.com/parthivqw/ai_market_intelligence.git)
cd ai_market_intelligence

Download Data Files:

Download the Google Play Store Apps dataset from this Kaggle link and place googleplaystore.csv inside the data/raw/ folder.

Place the D2C Synthetic Dataset (Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx) inside the phase5_extension/ folder.

Create Virtual Environment & Install Dependencies:

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

Set API Keys:

Create a file named .env in the root of the project.

Add your personal API keys to it:

RAPIDAPI_KEY="your_rapidapi_key_here"
GROQ_API_KEY="your_groq_api_key_here"

3. Running the Full Pipeline
Execute the scripts in the following order to generate all necessary outputs for the dashboard.

# Phase 1-4: App Market Analysis
python scripts/01_data_cleaning.py
python scripts/02_api_integration.py
python scripts/03_insight_generation.py

# Phase 5: D2C Extension
python phase5_extension/01_d2c_analysis.py
python phase5_extension/02_creative_generation.py

4. Launching the Dashboard
After running the pipeline scripts, launch the interactive Streamlit app.

streamlit run app.py

Your web browser will open with the dashboard. Use the sidebar to switch between the App Market Intelligence view and the D2C Marketing Extension view.

✅ Deliverables Checklist
[x] Clean Combined Dataset: Generated at data/processed/combined_market_data.csv.

[x] Insights JSON File: Generated at insights.json.

[x] Executive Report: Generated at executive_report.md by running scripts/04_report_automation.py.

[x] Streamlit Interface: The main dashboard, launched via streamlit run app.py.

[x] Phase 5 Extension:

Funnel + SEO Insights are generated and visible in the UI.

AI-Generated Creative Outputs are generated and visible in the UI.
