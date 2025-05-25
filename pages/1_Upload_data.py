import streamlit as st
import pandas as pd
import io

def main():
    st.title("Upload and Preview CSV")
    
    # Update session state to reflect current page
    st.session_state.page = 'Upload'
    
    # Initialize session state for uploaded file
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    
    # File uploader with persistent key
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'], key="csv_uploader")
    
    # Update session state when a new file is uploaded
    if uploaded_file is not None and uploaded_file != st.session_state.uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
            st.session_state.df = None
            st.session_state.uploaded_file = None
    
        # Display preview if data exists in session state
    if st.session_state.df is not None:
        st.subheader("Data Preview")
        st.write("First 5 rows of the uploaded data:")
        st.dataframe(st.session_state.df.head())

        st.subheader("Dataset Info")
        df = st.session_state.df

        # Add toggle for filtering out entirely null columns
        hide_empty_columns = st.checkbox(
            "Only show columns with at least one non-null value", value=True
        )

        # Build summary DataFrame
        info_df = pd.DataFrame({
            "Column Name": df.columns,
            "Non-Null Count": df.notnull().sum().values,
            "Data Type": df.dtypes.astype(str).values
        })

        if hide_empty_columns:
            info_df = info_df[info_df["Non-Null Count"] > 0]

        st.dataframe(info_df)


        
        # Navigation button to Filter page
        if st.button("Go to Filter Page"):
            st.session_state.page = 'Filter'
            st.rerun()
    else:
        st.info("Please upload a CSV file to proceed.")

if __name__ == "__main__":
    main()