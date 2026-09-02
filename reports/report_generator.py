import io
import pandas as pd

def generate_excel_report(df, health_data, insights_data):
    """
    Generates a multi-tab Excel workbook with dataset, health summary, and KPIs.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Tab 1: Clean Data
        df.to_excel(writer, sheet_name='Clean Dataset', index=False)

        # Tab 2: Health Profile
        health_df = pd.DataFrame([
            {"Metric": "Overall Health Score", "Value": f"{health_data.get('score', 0)}%"},
            {"Metric": "Quality Grade", "Value": health_data.get('grade', 'N/A')},
            {"Metric": "Completeness", "Value": f"{health_data.get('completeness', 0)}%"},
            {"Metric": "Uniqueness", "Value": f"{health_data.get('uniqueness', 0)}%"},
            {"Metric": "Consistency", "Value": f"{health_data.get('consistency', 0)}%"},
        ])
        health_df.to_excel(writer, sheet_name='Data Health', index=False)

        # Tab 3: Insights & KPIs
        if insights_data.get("key_metrics"):
            kpi_df = pd.DataFrame(insights_data.get("key_metrics"))
            kpi_df.to_excel(writer, sheet_name='KPI Summary', index=False)

    output.seek(0)
    return output

def generate_markdown_report(dataset_name, health_data, insights_data):
    """
    Generates a clean Markdown report document.
    """
    md = []
    md.append(f"# 🤖 AI Data Analyst Report - {dataset_name}\n")
    md.append("## 1. Data Quality Profile")
    md.append(f"- **Health Score**: {health_data.get('score', 0)}% ({health_data.get('grade', 'N/A')})")
    md.append(f"- **Completeness**: {health_data.get('completeness', 0)}%")
    md.append(f"- **Uniqueness**: {health_data.get('uniqueness', 0)}%\n")

    md.append("## 2. Key Insights")
    md.append(f"**Summary**: {insights_data.get('summary', '')}\n")
    for ins in insights_data.get('insights', []):
        md.append(f"- {ins}")
    md.append("\n## 3. Strategic Recommendations")
    for rec in insights_data.get('recommendations', []):
        md.append(f"- {rec}")

    return "\n".join(md)
