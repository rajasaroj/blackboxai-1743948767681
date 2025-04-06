## Working Code
import streamlit as st
from datetime import date
import json
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# Configure page
st.set_page_config(
    page_title="Modern Dashboard",
    page_icon="📊",
    layout="wide"
)

# Sidebar navigation
with st.sidebar:
    st.title("Navigation")
    page = st.radio("Go to", ["Dashboard", "Analytics", "Settings"])

    st.divider()
    st.write(f"Today: {date.today().strftime('%B %d, %Y')}")

# Main content area
st.title("📊 Modern Dashboard")
st.subheader("Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

df = None

if uploaded_file is not None and 'edited_df' not in st.session_state:

    print("entering val----------------")
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Display the content of the CSV
    st.write("### Uploaded CSV Content")
    st.dataframe(df)

    if 'Select' not in df.columns:
        df['Select'] = False

    # Initialize session state
    if 'original_df' not in st.session_state:
        st.session_state.original_df = df.copy()
        st.session_state.edited_df = df.copy()
        st.session_state.edited_rows = set()

if 'edited_df' in st.session_state:

    # Configure AgGrid
    gb = GridOptionsBuilder.from_dataframe(st.session_state.edited_df)
    gb.configure_default_column(editable=True)
    gb.configure_column("Select", editable=True, checkbox=True)
    gb.configure_selection("multiple", use_checkbox=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        st.session_state.edited_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        height=400,
        allow_unsafe_jscode=True,
        reload_data=False
    )

    edited_df = grid_response["data"]

    # # Compare and persist edited rows
    # for idx in edited_df.index:
    #     row_original = st.session_state.edited_df.loc[idx]
    #     row_new = edited_df.loc[idx]
    #     if not row_original.equals(row_new):
    #         st.session_state.edited_df.loc[idx] = row_new  # persist change

    # Add single Train button below table
    if st.button("Train Selected Rows"):
        selected_rows = edited_df[edited_df['Select'] == True]
        for idx, row in selected_rows.iterrows():
            row_data = row.drop('Select').to_dict()
            json_data = json.dumps(row_data, indent=2)

            st.toast(f"Sent row {int(idx) + 1} to training pipeline")
            print(f"Training data for row {int(idx) + 1}:\n{json_data}")

    # Download button
    if st.button("Download Updated CSV"):
        st.session_state.edited_df.to_csv("updated_file.csv", index=False)
        st.success("Updated file is ready for download!")

st.caption("A responsive Streamlit application")

# Create responsive columns
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Total Users", value="1,234", delta="12%")
    st.write("""
    ### Recent Activity
    - User signups: 45
    - Page views: 1,234
    - Conversions: 32%
    """)

with col2:
    st.metric(label="Revenue", value="$12,345", delta="-3%")
    st.write("""
    ### Performance
    - Load time: 1.2s
    - Uptime: 99.9%
    - Active sessions: 56
    """)

# Responsive chart section
st.subheader("Analytics Overview")
st.line_chart({
    'Users': [100, 200, 300, 400, 500, 600],
    'Revenue': [50, 60, 70, 80, 90, 100]
})

# Footer
st.divider()
st.caption("© 2023 Modern Dashboard - All rights reserved")
