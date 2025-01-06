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

# Display available columns for debugging
st.write("Columns in the dataset:")
st.write(df.columns.tolist())

# Use correct column names for weekly achievements
df['Overall_Cash_Achv'] = df['WK1l_Cash_Achv'] + df['WK2_Cash_Achv'] + df['WK3_Cash_Achv'] + df['WK4_Cash_Achv']
df['Overall_Enrl_Achv'] = df['WK1_Enrl_Achv'] + df['WK2_Enrl_Achv'] + df['WK3_Enrl_Achv'] + df['WK4_Enrl_Achv']
df['Overall_SGR_Achv'] = df['WK1_SGR_Achv'] + df['WK2_SGR_Achv'] + df['WK3_SGR_Achv'] + df['WK4_SGR_Achv']

# Validate required column exists
if 'AC_Name' not in df.columns:
    st.error("The required column 'AC_Name' is missing from the dataset.")
    st.stop()

# Dropdown for selecting an AC_Name
selected_ac = st.selectbox("Select an AC_Name:", df['AC_Name'].dropna().unique())

# Filter data for the selected AC_Name
filtered_data = df[df['AC_Name'] == selected_ac]

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
    summary_df = pd.DataFrame([overall_summary])
    st.table(summary_df)
else:
    st.warning(f"No data available for the selected AC_Name: {selected_ac}.")
