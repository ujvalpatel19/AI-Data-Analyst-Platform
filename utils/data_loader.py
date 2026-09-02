import pandas as pd
import io
import chardet
import streamlit as st

@st.cache_data(show_spinner=False)
def load_data(file_input):
    """
    Loads CSV or Excel data with automatic encoding and delimiter detection.
    file_input can be a Streamlit UploadedFile, file path, or BytesIO.
    """
    if file_input is None:
        return None

    try:
        # Check if it's an Excel file
        if hasattr(file_input, 'name') and (file_input.name.endswith('.xlsx') or file_input.name.endswith('.xls')):
            df = pd.read_excel(file_input)
            return clean_column_names(df)
        elif isinstance(file_input, str) and (file_input.endswith('.xlsx') or file_input.endswith('.xls')):
            df = pd.read_excel(file_input)
            return clean_column_names(df)

        # Handle CSV format
        if hasattr(file_input, 'read'):
            content = file_input.read()
            # Reset stream position
            if hasattr(file_input, 'seek'):
                file_input.seek(0)
            
            # Detect encoding
            detected = chardet.detect(content[:10000])
            encoding = detected.get('encoding') or 'utf-8'

            # Try parsing with detected encoding
            try:
                df = pd.read_csv(io.BytesIO(content), encoding=encoding)
            except Exception:
                df = pd.read_csv(io.BytesIO(content), encoding='latin1')
        else:
            # File path string
            try:
                df = pd.read_csv(file_input, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_input, encoding='latin1')

        # Clean column names
        df = clean_column_names(df)
        
        # Convert date-like string columns to datetime
        for col in df.columns:
            if df[col].dtype == 'object':
                if 'date' in col.lower() or 'time' in col.lower():
                    try:
                        df[col] = pd.to_datetime(df[col])
                    except (ValueError, TypeError):
                        pass

        return df

    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return None

def clean_column_names(df):
    """Trims whitespace and standardizes column names."""
    df.columns = [str(col).strip() for col in df.columns]
    return df
