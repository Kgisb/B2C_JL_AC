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

# Add missing columns if they don't exist
required_columns = [
    "WK1_Cash_Target", "WK2_Cash_Target", "WK3_Cash_Target", "WK4_Cash_Target",
    "WK1_Cash_Achv", "WK2_Cash_Achv", "WK3_Cash_Achv", "WK4_Cash_Achv",
    "WK1_Enrl_Target", "WK2_Enrl_Target", "WK3_Enrl_Target", "WK4_Enrl_Target",
    "WK1_Enrl_Achv", "WK2_Enrl_Achv", "WK3_Enrl_Achv", "WK4_Enrl_Achv",
    "WK1_Self_Ref_Target", "WK2_Self_Ref_Target", "WK3_Self_Ref_Target", "WK4_Self_Ref_Target",
    "WK1_Self_Ref_Achv", "WK2_Self_Ref_Achv", "WK3_Self_Ref_Achv", "WK4_Self_Ref_Achv",
]

for col in required_columns:
    if col not in df.columns:
        df[col] = 0  # Add missing column with default value 0

# Derive Overall Targets and Achievements
df['Overall_Cash_Target'] = df['WK1_Cash_Target'] + df['WK2_Cash_Target'] + df['WK3_Cash_Target'] + df['WK4_Cash_Target']
df['Overall_Cash_Achv'] = df['WK1_Cash_Achv'] + df['WK2_Cash_Achv'] + df['WK3_Cash_Achv'] + df['WK4_Cash_Achv']

df['Overall_Enrl_Target'] = df['WK1_Enrl_Target'] + df['WK2_Enrl_Target'] + df['WK3_Enrl_Target'] + df['WK4_Enrl_Target']
df['Overall_Enrl_Achv'] = df['WK1_Enrl_Achv'] + df['WK2_Enrl_Achv'] + df['WK3_Enrl_Achv'] + df['WK4_Enrl_Achv']

df['Overall_Self_Ref_Target'] = df['WK1_Self_Ref_Target'] + df['WK2_Self_Ref_Target'] + df['WK3_Self_Ref_Target'] + df['WK4_Self_Ref_Target']
df['Overall_Self_Ref_Achv'] = df['WK1_Self_Ref_Achv'] + df['WK2_Self_Ref_Achv'] + df['WK3_Self_Ref_Achv'] + df['WK4_Self_Ref_Achv']

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
        "Overall Self Ref. Target": filtered_data["Overall_Self_Ref_Target"].sum(),
        "Overall Self Ref. Achieved": filtered_data["Overall_Self_Ref_Achv"].sum(),
    }
    summary_df = pd.DataFrame([overall_summary])
    st.table(summary_df)
else:
    st.warning(f"No data available for the selected AC_Name: {selected_ac}.")
