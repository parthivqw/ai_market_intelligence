AI-Powered Market Intelligence System - Project Report
Author: Parthiv S

1. Project Overview
This project implements an end-to-end AI-powered market intelligence system as per the assignment brief. The system ingests and cleans data from multiple sources (a static CSV and a live API), unifies it, uses a Large Language Model (Groq) to derive strategic insights, and presents the findings through an automated report and an interactive Streamlit dashboard.

The project also includes the Phase 5 extension, demonstrating the pipeline's adaptability by repurposing it for a D2C e-commerce dataset to generate both business insights and AI-powered creative content (ad headlines and an SEO description).

Technologies Used: Python, Pandas, Streamlit, Requests, python-dotenv, and the Groq LLM API.

2. File Structure
The project is organized into a modular structure for clarity and reproducibility:

ai_project_intelligence/
├── data/
│   ├── raw/
│   │   └── googleplaystore.csv
│   └── processed/
├── phase5_extension/
│   ├── Kasparro_Phase5_D2C_Synthetic_Dataset.xlsx
│   ├── 01_d2c_analysis.py
│   └── 02_creative_generation.py
├── scripts/
│   ├── 01_data_cleaning.py
│   ├── 02_api_integration.py
│   ├── 03_insight_generation.py
│   └── 04_report_automation.py
├── .env.example
├── app.py
├── executive_report.md
└── requirements.txt

3. How to Run
Follow these steps to set up and run the entire project.

Step 1: Setup
Unzip the File: Unzip ai_project_intelligence.zip.

Navigate to Directory: Open a terminal and cd into the ai_project_intelligence folder.

Create Virtual Environment:

python -m venv venv

Activate Environment:

On Windows: venv\Scripts\activate

On macOS/Linux: source venv/bin/activate

Install Dependencies:

pip install -r requirements.txt

Set API Keys:

Rename the .env.example file to .env.

Open the .env file and add your personal API keys:

RAPIDAPI_KEY="your_rapidapi_key_here"
GROQ_API_KEY="your_groq_api_key_here"

Step 2: Running the Pipeline (In Order)
Run the following scripts sequentially from your terminal to generate all the necessary data and insight files.

Clean Google Play Data:

python scripts/01_data_cleaning.py

Fetch API Data & Combine:

python scripts/02_api_integration.py

Generate AI Insights for App Market:

python scripts/03_insight_generation.py

Generate Markdown Report:

python scripts/04_report_automation.py

Step 3: Running the Phase 5 Extension
Analyze D2C Data:

python phase5_extension/01_d2c_analysis.py

Generate Creative Content:

python phase5_extension/02_creative_generation.py

Step 4: Launching the Interactive UI
After running all the scripts, launch the Streamlit dashboard:

streamlit run app.py

Your web browser will open with the dashboard. You can use the sidebar to switch between the "App Market Intelligence" view (Phases 1-4) and the "D2C Marketing Extension" view (Phase 5).

4. Deliverables Checklist
Clean Combined Dataset: Located at data/processed/combined_market_data.csv.

Insights JSON File: Located at insights.json.

Executive Report: Located at executive_report.md.

CLI/Streamlit Interface: The main dashboard, run via streamlit run app.py.

Phase 5 Extension:

Funnel + SEO Insights: Printed to the console by 01_d2c_analysis.py.

AI-Generated Creative Outputs: Printed to the console by 02_creative_generation.py. The results are also visible in the Streamlit UI.
