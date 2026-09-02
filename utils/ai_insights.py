import os
import json
import pandas as pd
import numpy as np
import requests


def generate_ai_insights(df, provider="local", api_key=None):
    """
    Generates automated executive insights using:
    - OpenAI
    - Google Gemini
    - Local rule-engine fallback
    """

    # Check dataset
    if df is None or df.empty:
        return {
            "summary": "No data available.",
            "key_metrics": [],
            "insights": [],
            "recommendations": []
        }

    # Extract statistical facts
    stats_data = extract_statistical_facts(df)

    # =========================================================
    # OPENAI
    # =========================================================

    if provider == "openai" and (
        api_key or os.getenv("OPENAI_API_KEY")
    ):

        try:

            return call_openai_insights(
                df,
                stats_data,
                api_key or os.getenv("OPENAI_API_KEY")
            )

        except Exception:
            # Fallback to local engine if OpenAI fails
            pass


    # =========================================================
    # GEMINI
    # =========================================================

    elif provider == "gemini" and (
        api_key or os.getenv("GEMINI_API_KEY")
    ):

        try:

            return call_gemini_insights(
                df,
                stats_data,
                api_key or os.getenv("GEMINI_API_KEY")
            )

        except Exception:
            # Fallback to local engine if Gemini fails
            pass


    # =========================================================
    # LOCAL OFFLINE ENGINE
    # =========================================================

    return generate_local_insights(
        df,
        stats_data
    )


# =========================================================
# EXTRACT DATASET STATISTICS
# =========================================================

def extract_statistical_facts(df):
    """
    Extracts factual statistics from the dataset.
    """

    numeric_cols = df.select_dtypes(
        include=[np.number]
    ).columns

    categorical_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns


    facts = {

        "num_rows": int(len(df)),

        "num_cols": int(len(df.columns)),

        "columns": list(df.columns),

        "total_nulls": int(
            df.isnull().sum().sum()
        ),

        "numeric_summaries": {},

        "top_categories": {}
    }


    # =========================================================
    # NUMERIC STATISTICS
    # =========================================================

    for col in numeric_cols:

        facts["numeric_summaries"][col] = {

            "mean": round(
                float(df[col].mean()),
                2
            ),

            "total": round(
                float(df[col].sum()),
                2
            ),

            "max": round(
                float(df[col].max()),
                2
            ),

            "min": round(
                float(df[col].min()),
                2
            ),

            "median": round(
                float(df[col].median()),
                2
            )
        }


    # =========================================================
    # CATEGORICAL STATISTICS
    # =========================================================

    for col in categorical_cols:

        mode_val = df[col].mode()

        facts["top_categories"][col] = {

            "top_item": (
                str(mode_val.iloc[0])
                if not mode_val.empty
                else "N/A"
            ),

            "unique_count": int(
                df[col].nunique()
            )
        }


    return facts


# =========================================================
# LOCAL OFFLINE INSIGHTS ENGINE
# =========================================================

def generate_local_insights(df, facts):
    """
    Generates insights using statistical rules.
    Works completely offline.
    """

    insights = []

    recommendations = []

    key_metrics = []


    numeric_cols = df.select_dtypes(
        include=[np.number]
    ).columns

    cat_cols = df.select_dtypes(
        include=["object", "category"]
    ).columns

    date_cols = df.select_dtypes(
        include=["datetime64", "datetime"]
    ).columns


    # =========================================================
    # KEY METRICS
    # =========================================================

    for col in numeric_cols:

        if any(
            term in col.lower()
            for term in [
                "sales",
                "revenue",
                "profit",
                "amount"
            ]
        ):

            key_metrics.append({

                "label": f"Total {col}",

                "value": (
                    f"{facts['numeric_summaries'][col]['total']:,.2f}"
                ),

                "sub": (
                    f"Average: "
                    f"{facts['numeric_summaries'][col]['mean']:,.2f}"
                )
            })


    # If no business-related numeric column found
    if not key_metrics and len(numeric_cols) > 0:

        col = numeric_cols[0]

        key_metrics.append({

            "label": f"Total {col}",

            "value": (
                f"{facts['numeric_summaries'][col]['total']:,.2f}"
            ),

            "sub": (
                f"Average: "
                f"{facts['numeric_summaries'][col]['mean']:,.2f}"
            )
        })


    # Total records metric

    key_metrics.append({

        "label": "Total Records",

        "value": f"{facts['num_rows']:,}",

        "sub": (
            f"{facts['num_cols']} attributes"
        )
    })


    # =========================================================
    # CORRELATION ANALYSIS
    # =========================================================

    if len(numeric_cols) >= 2:

        corr_matrix = (
            df[numeric_cols]
            .corr()
            .abs()
        )

        corr_values = corr_matrix.to_numpy(
            copy=True
        )

        np.fill_diagonal(
            corr_values,
            0
        )

        corr_matrix_copy = pd.DataFrame(

            corr_values,

            index=corr_matrix.index,

            columns=corr_matrix.columns
        )


        max_corr_idx = (
            corr_matrix_copy
            .stack()
            .idxmax()
        )


        val = corr_matrix_copy.loc[
            max_corr_idx
        ]


        if val > 0.5:

            insights.append(

                f"Strong statistical correlation "
                f"({val:.2f}) found between "
                f"'{max_corr_idx[0]}' and "
                f"'{max_corr_idx[1]}'."

            )


    # =========================================================
    # TOP CATEGORY
    # =========================================================

    for col in cat_cols:

        top_info = (
            facts["top_categories"][col]
        )

        insights.append(

            f"The most common value in "
            f"'{col}' is "
            f"'{top_info['top_item']}', "
            f"with "
            f"{top_info['unique_count']} "
            f"unique values in this column."

        )

        break


    # =========================================================
    # SKEWNESS / OUTLIER ANALYSIS
    # =========================================================

    for col in numeric_cols:

        skew = df[col].skew()


        if abs(skew) > 1.0:

            insights.append(

                f"Field '{col}' has high "
                f"distribution skewness "
                f"({skew:.2f}), which may indicate "
                f"outliers or highly concentrated values."

            )


            recommendations.append(

                f"Review potential outliers in "
                f"'{col}' before performing "
                f"advanced statistical analysis."

            )

            break


    # =========================================================
    # TIME TREND ANALYSIS
    # =========================================================

    if len(date_cols) > 0 and len(numeric_cols) > 0:

        date_col = date_cols[0]

        num_col = numeric_cols[0]


        try:

            df_sorted = df.sort_values(
                by=date_col
            )


            first_val = (
                df_sorted[num_col].iloc[0]
            )

            last_val = (
                df_sorted[num_col].iloc[-1]
            )


            if first_val != 0:

                pct_change = (
                    (
                        last_val - first_val
                    )
                    /
                    first_val
                    *
                    100
                )

            else:

                pct_change = 0


            direction = (

                "upward"

                if pct_change >= 0

                else

                "downward"
            )


            insights.append(

                f"Across the available timeline, "
                f"'{num_col}' shows an "
                f"{direction} movement of "
                f"{abs(pct_change):.1f}%."

            )

        except Exception:

            pass


    # =========================================================
    # DEFAULT INSIGHTS
    # =========================================================

    if not insights:

        insights.append(

            "The dataset has been successfully "
            "analyzed for structure, numerical "
            "patterns and categorical distributions."

        )


    # =========================================================
    # DEFAULT RECOMMENDATIONS
    # =========================================================

    if not recommendations:

        recommendations.append(

            "Review missing values and duplicate "
            "records before performing advanced "
            "analysis or machine learning."

        )


        recommendations.append(

            "Use the visualization dashboard to "
            "explore relationships and trends "
            "between important variables."

        )


    # =========================================================
    # EXECUTIVE SUMMARY
    # =========================================================

    summary = (

        f"Analysis completed successfully across "
        f"{facts['num_rows']} rows and "
        f"{facts['num_cols']} columns. "

        f"The dataset currently contains "
        f"{facts['total_nulls']} missing values."

    )


    return {

        "summary": summary,

        "key_metrics": key_metrics[:4],

        "insights": insights,

        "recommendations": recommendations
    }


# =========================================================
# OPENAI INSIGHTS
# =========================================================

def call_openai_insights(df, facts, api_key):
    """
    Calls OpenAI API for AI-powered dataset insights.
    """

    prompt = f"""

You are an expert Data Analyst.

Analyze the following dataset statistics and generate
professional executive insights.

DATASET FACTS:

{json.dumps(facts, default=str)}

Return ONLY valid JSON in this format:

{{
    "summary": "Executive summary",
    "insights": [
        "Insight 1",
        "Insight 2",
        "Insight 3"
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ]
}}

IMPORTANT RULES:

1. Do not invent information.
2. Use only the provided dataset statistics.
3. Do not assume currency unless explicitly mentioned.
4. Provide useful and practical insights.
5. Return only valid JSON.
"""


    headers = {

        "Authorization": (
            f"Bearer {api_key}"
        ),

        "Content-Type": (
            "application/json"
        )
    }


    payload = {

        "model": "gpt-4o-mini",

        "messages": [

            {

                "role": "user",

                "content": prompt
            }

        ],

        "response_format": {

            "type": "json_object"
        }
    }


    response = requests.post(

        "https://api.openai.com/v1/chat/completions",

        headers=headers,

        json=payload,

        timeout=60
    )


    response.raise_for_status()


    result = response.json()


    content = json.loads(

        result["choices"][0]
        ["message"]
        ["content"]

    )


    # Add locally calculated KPI metrics

    content["key_metrics"] = (

        generate_local_insights(
            df,
            facts
        )["key_metrics"]

    )


    return content


# =========================================================
# GEMINI INSIGHTS
# =========================================================

def call_gemini_insights(df, facts, api_key):
    """
    Calls Google Gemini API for AI-powered insights.
    """

    # Current Gemini API endpoint

    url = (

        "https://generativelanguage.googleapis.com/"
        "v1beta/models/"
        "gemini-2.5-flash:generateContent"

    )


    prompt = f"""

You are an expert Data Analyst.

Analyze the dataset statistics below and provide
professional executive insights.

DATASET FACTS:

{json.dumps(facts, default=str)}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "summary": "Overall executive summary",

    "insights": [

        "Important insight 1",

        "Important insight 2",

        "Important insight 3"

    ],

    "recommendations": [

        "Actionable recommendation 1",

        "Actionable recommendation 2"

    ]
}}

IMPORTANT RULES:

1. Do not invent any information.
2. Base every insight only on the provided statistics.
3. Do not assume that numerical values represent money.
4. Do not add currency symbols unless explicitly present.
5. Provide meaningful business or analytical insights.
6. Return ONLY valid JSON.
7. Do not include markdown.
8. Do not include ```json or code blocks.

"""


    payload = {

        "contents": [

            {

                "parts": [

                    {

                        "text": prompt

                    }

                ]

            }

        ]

    }


    headers = {

        "Content-Type": (
            "application/json"
        ),

        "x-goog-api-key": api_key

    }


    response = requests.post(

        url,

        headers=headers,

        json=payload,

        timeout=60
    )


    # Raise error if API fails

    response.raise_for_status()


    result = response.json()


    # Extract Gemini response

    text = (

        result["candidates"][0]
        ["content"]
        ["parts"][0]
        ["text"]

    )


    # Remove markdown formatting if Gemini returns it

    text = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )


    # Convert JSON string to Python dictionary

    content = json.loads(text)


    # Generate KPI metrics locally for consistency

    content["key_metrics"] = (

        generate_local_insights(
            df,
            facts
        )["key_metrics"]

    )


    return content