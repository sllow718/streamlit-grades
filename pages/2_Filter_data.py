import streamlit as st
import pandas as pd
from utils.helpers import extract_section_code

def main():
    st.title("Filter Data")
    
    # Update session state to reflect current page
    st.session_state.page = 'Filter'
    
    if st.session_state.df is None:
        st.error("No data available. Please upload a CSV file on the Upload page.")
        if st.button("Go to Upload Page"):
            st.session_state.page = 'Upload'
            st.rerun()
        return  # Exit early to prevent rendering empty page
    
    df = st.session_state.df
    
    # Extract unique section codes (last 4 characters)
    df['Section_Code'] = df['Sections'].apply(extract_section_code)
    unique_sections = sorted(df['Section_Code'].unique())
    default_sections = ['PC02', 'PC10','PC14']  # Default columns to show

    
    # Filter by Section Code
    st.subheader("Filter by Section Code")
    selected_sections = st.multiselect(
        "Select Section Codes (last 4 characters)",
        options=unique_sections,
        default=default_sections
    )
    
    # Apply section filter
    if selected_sections:
        filtered_df = df[df['Section_Code'].isin(selected_sections)]
    else:
        filtered_df = df
    
    # Column selection
    st.subheader("Select Columns to Display")

    # Keep columns that have at least one non-null value
    non_empty_columns = filtered_df.columns[filtered_df.notnull().sum() > 0].tolist()

    # Define default columns and filter based on what's available
    quiz_columns = [col for col in non_empty_columns if 'e-quiz' in col.lower()]
    default_columns = ['First Name', 'Section_Code'] + quiz_columns
    default_selection = [col for col in default_columns if col in non_empty_columns]

    # Multiselect from non-empty columns only
    selected_columns = st.multiselect(
        "Select columns to display (exclude empty columns)",
        options=non_empty_columns,
        default=default_selection
    )


    # Display filtered data with selected columns
    st.subheader("Filtered Data")

    # Checkbox to show only rows with missing values in the selected columns
    show_only_missing = st.checkbox("Show only rows with missing values", value=False)

    # Ensure at least one column is selected
    if selected_columns:
        display_df = filtered_df[selected_columns]

        # Filter to only rows that have at least one NaN in the selected columns
        if show_only_missing:
            display_df = display_df[display_df.isnull().any(axis=1)]

        st.dataframe(display_df)
    else:
        st.warning("Please select at least one column to display.")
        st.dataframe(filtered_df)


    
    # Navigation button back to Upload page
    if st.button("Back to Upload Page"):
        st.session_state.page = 'Upload'
        st.rerun()

if __name__ == "__main__":
    main()