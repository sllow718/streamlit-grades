import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.helpers import extract_section_code

def main():
    st.title("Histogram of Scores by Section Code")
    
    if st.session_state.df is None:
        st.error("No data available. Please upload a CSV file on the Upload page.")
        if st.button("Go to Upload Page"):
            st.session_state.page = 'Upload'
            st.experimental_rerun()
        return
    
    df = st.session_state.df.copy()
    
    # Extract Section_Code if not present
    if 'Section_Code' not in df.columns:
        df['Section_Code'] = df['Sections'].apply(extract_section_code)
    
    # Identify numeric columns with at least one non-null value
    numeric_cols = [
        col for col in df.select_dtypes(include='number').columns
        if df[col].notnull().sum() > 0
    ]

    if not numeric_cols:
        st.error("No numeric columns with non-null values available in the dataset for histogram plotting.")
        return

    
    # Section codes available
    unique_sections = sorted(df['Section_Code'].unique())
    # Keep columns that have at least one non-null value
    non_empty_columns = df.columns[df.notnull().sum() > 0].tolist()
    # Select multiple score columns
    quiz_columns = [col for col in non_empty_columns if 'e-quiz' in col.lower()]
    selected_scores = st.multiselect("Select Score Column(s)", options=numeric_cols, default=quiz_columns if numeric_cols else [])

    # Allow multiple section codes to be selected
    selected_sections = st.multiselect("Select Section Codes", options=unique_sections, default=unique_sections)

    # Filter data by selected section codes
    if selected_sections:
        filtered_df = df[df['Section_Code'].isin(selected_sections)]
    else:
        filtered_df = df.copy()

    if filtered_df.empty:
        st.warning("No data available for the selected section codes.")
        return

    if not selected_scores:
        st.warning("Please select at least one score column to display.")
        return

    # Sum selected score columns row-wise, skipping NaNs by treating them as zeros
    # (or you can decide how you want to handle NaNs)
    summed_scores = filtered_df[selected_scores].fillna(0).sum(axis=1)

    # Plot histogram of the summed scores
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.hist(summed_scores, bins=5, color='skyblue', edgecolor='black')
    ax.set_title(f'Histogram of summed scores for selected Section(s)')
    ax.set_xlabel('Sum of Selected Scores')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    

if __name__ == "__main__":
    main()
