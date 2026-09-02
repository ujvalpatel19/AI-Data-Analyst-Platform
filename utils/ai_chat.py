import os
import re
import json
import requests
import pandas as pd
import numpy as np


# ==================================================
# MAIN CHAT FUNCTION
# ==================================================

def ask_data_chat(df, user_query, provider="local", api_key=None, chat_history=None):

    if df is None or df.empty:
        return "⚠️ Please upload a valid dataset first before asking questions."

    provider = provider.lower().strip()

    # ----------------------------------------------
    # GEMINI
    # ----------------------------------------------
    if provider == "gemini":

        key = api_key or os.getenv("GEMINI_API_KEY")

        if key:
            try:
                return query_llm_chat(
                    df=df,
                    user_query=user_query,
                    provider="gemini",
                    api_key=key
                )

            except Exception as e:
                return (
                    "⚠️ Gemini AI could not process this request.\n\n"
                    f"**Error:** {str(e)}"
                )

        return "⚠️ Gemini API key was not found. Please check your `.env` file."


    # ----------------------------------------------
    # OPENAI
    # ----------------------------------------------
    elif provider == "openai":

        key = api_key or os.getenv("OPENAI_API_KEY")

        if key:
            try:
                return query_llm_chat(
                    df=df,
                    user_query=user_query,
                    provider="openai",
                    api_key=key
                )

            except Exception as e:
                return (
                    "⚠️ OpenAI could not process this request.\n\n"
                    f"**Error:** {str(e)}"
                )

        return "⚠️ OpenAI API key was not found. Please check your `.env` file."


    # ----------------------------------------------
    # LOCAL ENGINE
    # ----------------------------------------------
    return query_local_smart_agent(df, user_query)


# ==================================================
# COLUMN MATCHING
# ==================================================

def find_matching_column(columns, query, preferred_keywords=None):

    query = query.lower()

    if preferred_keywords is None:
        preferred_keywords = []

    # Exact column name match
    for col in columns:
        if col.lower() in query:
            return col

    # Individual words match
    query_words = re.findall(r"[a-zA-Z]+", query)

    for col in columns:

        col_words = re.findall(r"[a-zA-Z]+", col.lower())

        for word in col_words:
            if word in query_words and len(word) > 2:
                return col

    # Preferred keywords
    for keyword in preferred_keywords:

        for col in columns:

            if keyword.lower() in col.lower():
                return col

    return None


# ==================================================
# DETECT IDENTIFIER COLUMNS
# ==================================================

def is_identifier_column(column):

    col = column.lower()

    identifier_terms = [
        "id",
        "sr",
        "serial",
        "sno",
        "number",
        "no.",
        "index"
    ]

    return any(term in col for term in identifier_terms)


# ==================================================
# FORMAT NUMBERS
# ==================================================

def format_number(value):

    if pd.isna(value):
        return "N/A"

    if isinstance(value, (int, np.integer)):
        return f"{value:,}"

    if isinstance(value, (float, np.floating)):

        if float(value).is_integer():
            return f"{int(value):,}"

        return f"{value:,.2f}"

    return str(value)


# ==================================================
# LOCAL SMART AGENT
# ==================================================

def query_local_smart_agent(df, query):

    q = query.lower().strip()

    numeric_cols = list(
        df.select_dtypes(include=[np.number]).columns
    )

    categorical_cols = list(
        df.select_dtypes(include=["object", "category"]).columns
    )

    # Remove ID / Serial columns for analysis
    useful_numeric_cols = [

        col for col in numeric_cols

        if not is_identifier_column(col)

    ]

    if not useful_numeric_cols:
        useful_numeric_cols = numeric_cols


    # ----------------------------------------------
    # TOTAL STUDENTS / PEOPLE / RECORDS
    # ----------------------------------------------

    people_keywords = [
        "student",
        "students",
        "people",
        "persons",
        "person",
        "customers",
        "employees",
        "names"
    ]

    if any(word in q for word in people_keywords):

        possible_name_cols = []

        for col in df.columns:

            col_lower = col.lower()

            if any(
                keyword in col_lower
                for keyword in [
                    "student",
                    "name",
                    "customer",
                    "employee",
                    "person"
                ]
            ):
                possible_name_cols.append(col)

        if possible_name_cols:

            target_col = possible_name_cols[0]

            unique_count = df[target_col].nunique()

            return (
                f"👥 The dataset contains "
                f"**{unique_count:,} unique {target_col} values**."
            )

        return (
            f"👥 The dataset contains "
            f"**{len(df):,} total records**."
        )


    # ----------------------------------------------
    # COUNT / HOW MANY
    # ----------------------------------------------

    if any(
        phrase in q
        for phrase in [
            "how many",
            "count",
            "total records",
            "number of records",
            "total rows",
            "rows"
        ]
    ):

        return (
            f"🔢 The dataset contains **{len(df):,} records** "
            f"across **{len(df.columns)} columns**."
        )


    # ----------------------------------------------
    # TOTAL / SUM
    # ----------------------------------------------

    if any(
        word in q
        for word in [
            "total",
            "sum",
            "overall"
        ]
    ):

        matched_col = find_matching_column(
            useful_numeric_cols,
            q
        )

        if matched_col:

            total_val = df[matched_col].sum()

            return (
                f"📊 The total **{matched_col}** is "
                f"**{format_number(total_val)}**."
            )

        return (
            "⚠️ I could not identify which numeric column "
            "you want to calculate the total for. "
            f"Available numeric columns: "
            f"**{', '.join(map(str, useful_numeric_cols))}**"
        )


    # ----------------------------------------------
    # AVERAGE / MEAN
    # ----------------------------------------------

    if any(
        word in q
        for word in [
            "average",
            "mean",
            "avg"
        ]
    ):

        matched_col = find_matching_column(
            useful_numeric_cols,
            q
        )

        if matched_col:

            avg_val = df[matched_col].mean()

            return (
                f"📈 The average **{matched_col}** is "
                f"**{format_number(avg_val)}**."
            )

        return (
            "⚠️ Please specify which column you want "
            "the average for."
        )


    # ----------------------------------------------
    # HIGHEST / TOP / MAX
    # ----------------------------------------------

    if any(
        word in q
        for word in [
            "highest",
            "top",
            "maximum",
            "max",
            "best"
        ]
    ):

        target_cat = find_matching_column(
            categorical_cols,
            q,
            preferred_keywords=[
                "category",
                "segment",
                "region",
                "name",
                "type"
            ]
        )

        target_num = find_matching_column(
            useful_numeric_cols,
            q,
            preferred_keywords=[
                "sales",
                "revenue",
                "profit",
                "amount"
            ]
        )

        if target_cat and target_num:

            grouped = (
                df.groupby(target_cat)[target_num]
                .sum()
                .sort_values(ascending=False)
            )

            top_name = grouped.index[0]

            top_val = grouped.iloc[0]

            return (
                f"🏆 The **{target_cat}** with the highest "
                f"total **{target_num}** is "
                f"**{top_name}**, with "
                f"**{format_number(top_val)}**."
            )

        return (
            "⚠️ I could not clearly identify the category "
            "and metric for this question."
        )


    # ----------------------------------------------
    # LOWEST / MINIMUM
    # ----------------------------------------------

    if any(
        word in q
        for word in [
            "lowest",
            "bottom",
            "minimum",
            "min",
            "worst"
        ]
    ):

        target_cat = find_matching_column(
            categorical_cols,
            q
        )

        target_num = find_matching_column(
            useful_numeric_cols,
            q
        )

        if target_cat and target_num:

            grouped = (
                df.groupby(target_cat)[target_num]
                .sum()
                .sort_values()
            )

            bottom_name = grouped.index[0]

            bottom_val = grouped.iloc[0]

            return (
                f"🔻 The lowest performing **{target_cat}** is "
                f"**{bottom_name}**, with "
                f"**{format_number(bottom_val)}** in "
                f"total **{target_num}**."
            )


    # ----------------------------------------------
    # UNIQUE VALUES
    # ----------------------------------------------

    if any(
        word in q
        for word in [
            "unique",
            "distinct",
            "categories"
        ]
    ):

        matched_col = find_matching_column(
            list(df.columns),
            q
        )

        if matched_col:

            return (
                f"🏷️ **{matched_col}** contains "
                f"**{df[matched_col].nunique():,} unique values**."
            )

        if categorical_cols:

            summary = []

            for col in categorical_cols[:5]:

                summary.append(
                    f"- **{col}**: {df[col].nunique():,} unique values"
                )

            return (
                "🏷️ **Unique values breakdown:**\n\n"
                + "\n".join(summary)
            )


    # ----------------------------------------------
    # FALLBACK
    # ----------------------------------------------

    return (
        "🤖 I can analyze your dataset, but I could not "
        "fully understand this question using the Local Engine.\n\n"
        "Try asking:\n\n"
        "- What is the total sales?\n"
        "- What is the average profit?\n"
        "- Which category has the highest sales?\n"
        "- How many students are there?\n"
        "- How many unique values are in Category?"
    )


# ==================================================
# LLM CHAT
# ==================================================

def query_llm_chat(df, user_query, provider, api_key):

    schema_info = {
        str(col): str(df[col].dtype)
        for col in df.columns
    }

    sample_data = (
        df.head(10)
        .replace({np.nan: None})
        .to_dict(orient="records")
    )

    numeric_summary = {}

    for col in df.select_dtypes(
        include=[np.number]
    ).columns:

        numeric_summary[str(col)] = {

            "sum": float(df[col].sum()),
            "mean": float(df[col].mean()),
            "min": float(df[col].min()),
            "max": float(df[col].max())

        }


    prompt = f"""
You are an expert AI Data Analyst.

Answer the user's question using ONLY the dataset information provided.

IMPORTANT RULES:
1. Do not invent columns or values.
2. Do not automatically use dollar ($) formatting.
3. Only use currency formatting if the column clearly represents currency.
4. If the user's question asks about students, people, customers, or names, identify the relevant column.
5. Give a direct and accurate answer.
6. If the available dataset information is insufficient, clearly say so.

DATASET COLUMNS AND TYPES:
{json.dumps(schema_info, indent=2)}

NUMERIC SUMMARY:
{json.dumps(numeric_summary, indent=2)}

SAMPLE DATA:
{json.dumps(sample_data, indent=2, default=str)}

USER QUESTION:
{user_query}

Provide a clear Markdown response.
"""


    # ----------------------------------------------
    # OPENAI
    # ----------------------------------------------

    if provider == "openai":

        headers = {

            "Authorization": f"Bearer {api_key}",

            "Content-Type": "application/json"

        }

        payload = {

            "model": "gpt-4o-mini",

            "messages": [

                {

                    "role": "user",

                    "content": prompt

                }

            ]

        }

        response = requests.post(

            "https://api.openai.com/v1/chat/completions",

            headers=headers,

            json=payload,

            timeout=30

        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]


    # ----------------------------------------------
    # GEMINI
    # ----------------------------------------------

    import pandas as pd
import numpy as np
import os
import requests
import json
import re


def ask_data_chat(df, user_query, provider="local", api_key=None, chat_history=None):
    """
    Processes natural language queries against the dataframe and generates
    intelligent answers using Local, OpenAI, or Gemini AI.
    """

    if df is None or df.empty:
        return "⚠️ Please upload a valid dataset first before asking questions."

    # OpenAI
    if provider == "openai" and (api_key or os.getenv("OPENAI_API_KEY")):
        try:
            return query_llm_chat(
                df=df,
                user_query=user_query,
                provider="openai",
                api_key=api_key or os.getenv("OPENAI_API_KEY")
            )
        except Exception as e:
            return f"⚠️ OpenAI could not process this request.\n\nError: {str(e)}"

    # Gemini
    elif provider == "gemini" and (api_key or os.getenv("GEMINI_API_KEY")):
        try:
            return query_llm_chat(
                df=df,
                user_query=user_query,
                provider="gemini",
                api_key=api_key or os.getenv("GEMINI_API_KEY")
            )
        except Exception as e:
            return f"⚠️ Gemini AI could not process this request.\n\nError: {str(e)}"

    # Local Offline Engine
    return query_local_smart_agent(df, user_query)


def query_local_smart_agent(df, query):
    """
    Offline natural language Pandas question-answering engine.
    """

    q = query.lower()

    numeric_cols = list(
        df.select_dtypes(include=[np.number]).columns
    )

    cat_cols = list(
        df.select_dtypes(include=["object", "category"]).columns
    )

    # ----------------------------------------
    # TOTAL / SUM
    # ----------------------------------------

    if any(word in q for word in ["total", "sum", "overall"]) and numeric_cols:

        matched_col = next(
            (
                c for c in numeric_cols
                if c.lower() in q
            ),
            numeric_cols[0]
        )

        total_val = df[matched_col].sum()

        return (
            f"📊 The total **{matched_col}** across "
            f"**{len(df):,} records** is "
            f"**{total_val:,.2f}**."
        )

    # ----------------------------------------
    # AVERAGE / MEAN
    # ----------------------------------------

    if any(word in q for word in ["average", "mean", "avg"]) and numeric_cols:

        matched_col = next(
            (
                c for c in numeric_cols
                if c.lower() in q
            ),
            numeric_cols[0]
        )

        avg_val = df[matched_col].mean()

        return (
            f"📈 The average **{matched_col}** "
            f"per record is **{avg_val:,.2f}**."
        )

    # ----------------------------------------
    # HIGHEST / TOP
    # ----------------------------------------

    if (
        any(word in q for word in ["highest", "top", "max", "best"])
        and cat_cols
        and numeric_cols
    ):

        target_cat = next(
            (
                c for c in cat_cols
                if c.lower() in q
            ),
            cat_cols[0]
        )

        target_num = next(
            (
                n for n in numeric_cols
                if n.lower() in q
            ),
            numeric_cols[0]
        )

        grouped = (
            df.groupby(target_cat)[target_num]
            .sum()
            .sort_values(ascending=False)
        )

        top_name = grouped.index[0]
        top_val = grouped.iloc[0]

        return (
            f"🏆 The highest performing **{target_cat}** "
            f"based on total **{target_num}** is "
            f"**{top_name}** with a value of "
            f"**{top_val:,.2f}**."
        )

    # ----------------------------------------
    # LOWEST / MINIMUM
    # ----------------------------------------

    if (
        any(word in q for word in ["lowest", "bottom", "min", "worst"])
        and cat_cols
        and numeric_cols
    ):

        target_cat = next(
            (
                c for c in cat_cols
                if c.lower() in q
            ),
            cat_cols[0]
        )

        target_num = next(
            (
                n for n in numeric_cols
                if n.lower() in q
            ),
            numeric_cols[0]
        )

        grouped = (
            df.groupby(target_cat)[target_num]
            .sum()
            .sort_values(ascending=True)
        )

        bottom_name = grouped.index[0]
        bottom_val = grouped.iloc[0]

        return (
            f"🔻 The lowest performing **{target_cat}** "
            f"based on total **{target_num}** is "
            f"**{bottom_name}** with a value of "
            f"**{bottom_val:,.2f}**."
        )

    # ----------------------------------------
    # COUNT / RECORDS
    # ----------------------------------------

    if any(
        word in q
        for word in [
            "how many",
            "count",
            "rows",
            "number of",
            "records"
        ]
    ):

        return (
            f"🔢 Your dataset contains "
            f"**{len(df):,} total records** "
            f"and **{len(df.columns)} columns**."
        )

    # ----------------------------------------
    # UNIQUE VALUES
    # ----------------------------------------

    if any(
        word in q
        for word in [
            "unique",
            "categories",
            "types",
            "distinct"
        ]
    ):

        if cat_cols:

            summary = [
                f"- **{c}**: {df[c].nunique()} unique values"
                for c in cat_cols[:5]
            ]

            return (
                "🏷️ **Unique values breakdown:**\n\n"
                + "\n".join(summary)
            )

    # ----------------------------------------
    # FALLBACK
    # ----------------------------------------

    cols_str = ", ".join(
        [f"`{c}`" for c in df.columns[:10]]
    )

    return (
        f"📊 I analyzed your dataset containing "
        f"**{len(df):,} rows** and "
        f"**{len(df.columns)} columns**.\n\n"

        f"Available columns include:\n"
        f"{cols_str}\n\n"

        f"💡 **Try asking:**\n"
        f"- What is the total of a column?\n"
        f"- Which category has the highest value?\n"
        f"- What is the average of a column?\n"
        f"- How many records are there?\n"
        f"- Show unique categories."
    )


def query_llm_chat(df, user_query, provider, api_key):
    """
    Sends dataset context and user question to OpenAI or Gemini.
    """

    # Dataset schema
    schema_info = {
        col: str(df[col].dtype)
        for col in df.columns
    }

    # More sample rows for AI context
    sample_data = df.head(10).to_dict(
        orient="records"
    )

    # Basic statistics
    numeric_summary = {}

    numeric_cols = df.select_dtypes(
        include=[np.number]
    ).columns

    for col in numeric_cols:

        numeric_summary[col] = {
            "total": float(df[col].sum()),
            "average": float(df[col].mean()),
            "minimum": float(df[col].min()),
            "maximum": float(df[col].max())
        }

    # Dataset context
    prompt = f"""
You are an expert AI Data Analyst.

You must answer the user's question based ONLY on the provided dataset information.

DATASET INFORMATION:

Total Rows:
{len(df)}

Total Columns:
{len(df.columns)}

Column Names and Data Types:
{json.dumps(schema_info, indent=2)}

Numeric Statistics:
{json.dumps(numeric_summary, indent=2)}

Sample Dataset Rows:
{json.dumps(sample_data, indent=2, default=str)}

USER QUESTION:
{user_query}

INSTRUCTIONS:

1. Understand the user's question carefully.
2. Answer according to the actual dataset information.
3. Do not invent columns or values.
4. Do not assume currency unless the dataset clearly represents money.
5. Use the actual column names when referring to data.
6. If the available dataset context is insufficient, clearly explain what information is available.
7. Keep the answer clear and professional.
8. Format the response using Markdown where helpful.
"""

    # ==================================================
    # OPENAI
    # ==================================================

    if provider == "openai":

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"]

    # ==================================================
    # GEMINI
    # ==================================================

    elif provider == "gemini":

        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-2.5-flash:generateContent"
        )

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }

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

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        return (
            result["candidates"][0]
            ["content"]
            ["parts"][0]
            ["text"]
        )

    # Fallback

    return query_local_smart_agent(
        df,
        user_query
    )