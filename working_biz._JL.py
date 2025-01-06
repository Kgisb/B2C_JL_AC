import pandas as pd
import streamlit as st

# Load data from Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/16U4reJDdvGQb6lqN9LF-A2QVwsJdNBV1CqqcyuHcHXk/export?format=csv&gid=908334443"

st.title("AC Target and Achievement Viewer")

# Load the data
try:
    # Read the Google Sheet into a DataFrame
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

# Validate required column exists
if 'AC_Name' not in df.columns:
    st.error("The required column 'AC_Name' is missing from the dataset.")
    st.stop()

# Add "All" option to the dropdown
ac_names = ['All'] + sorted(df['AC_Name'].dropna().unique().tolist())
selected_ac = st.selectbox("Select an AC_Name:", ac_names)

# Filter data for the selected AC_Name
if selected_ac == 'All':
    filtered_data = df
else:
    filtered_data = df[df['AC_Name'] == selected_ac]

# Display the filtered data dynamically
if not filtered_data.empty:
    st.subheader(f"Data for AC_Name: {selected_ac}")
    st.dataframe(filtered_data)

    # Summary for Overall Targets and Achievements
    st.subheader("Overall Summary")
    overall_summary = {
        "Overall Cash Target": filtered_data["Overall_Cash_Target"].sum(),
        "Overall Cash Achieved": filtered_data["Overall_Cash_Achv"].sum(),
        "Overall Enrl. Target": filtered_data["Overall_Enrl_Target"].sum(),
        "Overall Enrl. Achieved": filtered_data["Overall_Enrl_Achv"].sum(),
        "Overall SGR Target": filtered_data["Overall_SGR_Target"].sum(),
        "Overall SGR Achieved": filtered_data["Overall_SGR_Achv"].sum(),
    }
    # Format the summary for clean display
    summary_df = pd.DataFrame([overall_summary])
    summary_df = summary_df.applymap(lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x)
    st.table(summary_df)
else:
    st.warning(f"No data available for the selected AC_Name: {selected_ac}.")
