import pandas as pd
import streamlit as st

# Load data from Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=908334443"

# Custom Styles
st.markdown(
    """
    <style>
    .header-title {
        font-size: 40px;
        font-weight: bold;
        color: #1f77b4;
    }
    .subheader-title {
        font-size: 24px;
        font-weight: bold;
        color: #ff7f0e;
    }
    .summary-card {
        padding: 15px;
        background-color: #f9f9f9;
        border-radius: 10px;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        color: #2ca02c;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown('<h1 class="header-title">AC Target and Achievement Viewer</h1>', unsafe_allow_html=True)

# Load the data
try:
    df = pd.read_csv(sheet_url)
    st.success("Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Clean column names
df.columns = df.columns.str.strip()

# Remove commas and convert relevant columns to numeric
numeric_columns = [
    "Overall_Cash_Target", "Overall_Enrl_Target", "Overall_SGR_Target",
    "Overall_Cash_Achv", "Overall_Enrl_Achv", "Overall_SGR_Achv",
    "WK1l_Cash_Achv", "WK2_Cash_Achv", "WK3_Cash_Achv", "WK4_Cash_Achv",
    "WK1_Enrl_Achv", "WK2_Enrl_Achv", "WK3_Enrl_Achv", "WK4_Enrl_Achv",
    "WK1_SGR_Achv", "WK2_SGR_Achv", "WK3_SGR_Achv", "WK4_SGR_Achv",
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].replace(",", "", regex=True)  # Remove commas
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)  # Convert to numeric

# Exclude rows where AC_Name is "Total" or similar
df = df[df['AC_Name'] != 'Total']

# Validate required column exists
if 'AC_Name' not in df.columns:
    st.error("The required column 'AC_Name' is missing from the dataset.")
    st.stop()

# Add "All" option to the dropdown
ac_names = ['All'] + sorted(df['AC_Name'].dropna().unique().tolist())
selected_ac = st.selectbox("Select an AC_Name:", ac_names, help="Choose 'All' to view data for all ACs")

# Filter data for the selected AC_Name
if selected_ac == 'All':
    filtered_data = df
else:
    filtered_data = df[df['AC_Name'] == selected_ac]

if not filtered_data.empty:
    st.markdown(f'<h2 class="subheader-title">Data for AC_Name: {selected_ac}</h2>', unsafe_allow_html=True)
    st.dataframe(filtered_data.style.format("{:,.0f}"))

    # Summary for Overall Targets and Achievements
    st.markdown('<h2 class="subheader-title">Overall Summary</h2>', unsafe_allow_html=True)
    overall_summary = {
        "Overall Cash Target": filtered_data["Overall_Cash_Target"].sum(),
        "Overall Cash Achieved": filtered_data["Overall_Cash_Achv"].sum(),
        "Overall Enrl. Target": filtered_data["Overall_Enrl_Target"].sum(),
        "Overall Enrl. Achieved": filtered_data["Overall_Enrl_Achv"].sum(),
        "Overall SGR Target": filtered_data["Overall_SGR_Target"].sum(),
        "Overall SGR Achieved": filtered_data["Overall_SGR_Achv"].sum(),
    }

    # Display summary in a card-like format
    summary_cols = st.columns(3)
    for idx, (key, value) in enumerate(overall_summary.items()):
        with summary_cols[idx % 3]:
            st.markdown(
                f'<div class="summary-card">{key}:<br>{value:,.0f}</div>',
                unsafe_allow_html=True,
            )
else:
    st.warning(f"No data available for the selected AC_Name: {selected_ac}.")
