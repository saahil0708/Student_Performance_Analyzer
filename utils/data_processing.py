import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    """Load data from uploaded CSV or Excel file."""
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format.")
            return None
        return preprocess_data(df)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def preprocess_data(df):
    """Basic data cleaning and preprocessing."""
    # Ensure standard columns are present if possible
    # Drop rows with all NaNs
    df.dropna(how='all', inplace=True)
    
    # Simple fill NaNs for numeric with mean
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    # Fill categorical with mode
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])
            
    return df
    
def get_class_stats(df):
    """Calculate overall statistics."""
    if df.empty:
        return {}
    
    stats = {}
    if "Percentage" in df.columns:
        stats["avg_percentage"] = df["Percentage"].mean()
        stats["topper"] = df.loc[df["Percentage"].idxmax()]
        stats["low_performer"] = df.loc[df["Percentage"].idxmin()]
        
    if "Status" in df.columns:
        stats["pass_count"] = (df["Status"] == "Pass").sum()
        stats["fail_count"] = (df["Status"] == "Fail").sum()
        stats["total_students"] = len(df)
        stats["pass_rate"] = (stats["pass_count"] / stats["total_students"]) * 100
        
    return stats
