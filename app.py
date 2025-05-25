import streamlit as st

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'Upload'
if 'df' not in st.session_state:
    st.session_state.df = None

# Main app logic
def main():    
    # Main page content: Instructions
    st.title("Welcome to the CSV Data Analysis App")
    st.subheader("How to Use This App")
    st.markdown("""
    1. **Navigate Pages**:
       - Use the sidebar menu to switch between **Upload** and **Filter** pages.
       - Select "upload_page" to upload a CSV file.
       - Select "filter_page" to filter and view the data.
    
    2. **Upload Page**:
       - Upload a CSV file (e.g., a grades dataset) using the file uploader.
       - View a preview of the first 5 rows, dataset info, and column names.
       - Click "Go to Filter Page" to proceed to filtering.
    
    3. **Filter Page**:
       - Filter data by section codes (last 4 characters of the "Sections" column).
       - Select columns to display in the filtered data table.
       - View filter statistics (row count, selected section codes, selected columns).
       - Click "Back to Upload Page" to upload a new file.
    
    **Note**: Ensure a CSV file is uploaded on the Upload page before using the Filter page, or you’ll see an error prompting you to upload a file.
    """)

if __name__ == "__main__":
    main()