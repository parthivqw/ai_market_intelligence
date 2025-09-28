import json
import os

def generate_markdown_report():
    """
    Loads insights from insights.json and generates a clean
    Markdown report.
    """
    print("--- Starting Phase 4, Part 1: Generating Automated Report ---")
    
    insights_path = 'insights.json'
    report_path = 'executive_report.md'

    try:
        with open(insights_path, 'r',encoding='utf-8') as f:
            insights = json.load(f)
    except FileNotFoundError:
        print(f"Error: '{insights_path}' not found. Please run the Phase 3 script first.")
        return

    # Start building the Markdown report string
    report_content = "# AI-Powered Market Intelligence Report\n\n"
    report_content += "This report details key insights generated from the analysis of top mobile applications.\n\n"
    report_content += "---\n\n"

    for insight in insights:
        report_content += f"## {insight['title']}\n\n"
        report_content += f"**Insight Type:** {insight['insight_type']}\n\n"
        report_content += f"**Summary:** {insight['summary']}\n\n"
        report_content += f"**Recommendation:** {insight['recommendation']}\n\n"
        report_content += f"**Confidence:** {insight['confidence_score'] * 100:.0f}%\n\n"
        report_content += "**Supporting Data:**\n"
        report_content += "```json\n"
        report_content += f"{json.dumps(insight['supporting_data'], indent=2)}\n"
        report_content += "```\n\n"
        report_content += "---\n\n"

    # Save the report to a file
    with open(report_path, 'w',encoding='utf-8') as f:
        f.write(report_content)

    print(f"✅ Success! Report generated and saved to '{report_path}'")

if __name__ == '__main__':
    generate_markdown_report()