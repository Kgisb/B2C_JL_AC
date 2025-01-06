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

# Map and rename columns for clarity
column_mapping = {
    "Dec_Target": "Cash-in Target",
    "Dec_Target.1": "Enrl. Target",
    "Dec_Target.2": "Self Gen. Ref. Target",
    "Dec_Achv": "Cash-in Achieved",
    "Dec_Achv.1": "Enrl. Achieved",
    "Dec_Achv.2": "Self Gen. Ref. Achieved",
}
df.rename(columns=column_mapping, inplace=True)

# Validate required column exists
if 'AC_Name' not in df.columns:
    st.error("The required column 'AC_Name' is missing from the dataset.")
    st.stop()

# Dropdown for selecting an AC_Name
selected_ac = st.selectbox("Select an AC_Name:", df['AC_Name'].dropna().unique())

# Filter data for the selected AC_Name
filtered_data = df[df['AC_Name'] == selected_ac]

# Display the filtered data
st.subheader(f"Data for AC_Name: {selected_ac}")
st.dataframe(filtered_data)

# Generate and display the summary
if not filtered_data.empty:
    st.subheader("Weekly Summary")
    summary_data = {}

    # Summarize data for each category and week
    for category, mapped_category in [
        ("Cash-in", "Cash-in Target"),
        ("Enrl.", "Enrl. Target"),
        ("Self Gen. Ref.", "Self Gen. Ref. Target"),
    ]:
        for week in ['WK_1', 'WK_2', 'WK_3', 'WK_4']:
            target_col = f"{mapped_category} {week}"
            achv_col = f"{category} Achieved {week}"
            if target_col in filtered_data.columns and achv_col in filtered_data.columns:
                summary_data[f"{category} {week} Target"] = filtered_data[target_col].sum()
                summary_data[f"{category} {week} Achieved"] = filtered_data[achv_col].sum()

    # Create summary DataFrame for display
    summary_df = pd.DataFrame(summary_data, index=[0]).T.reset_index()
    summary_df.columns = ['Metric', 'Value']
    st.table(summary_df)
else:
    st.warning("No data available for the selected AC_Name.")
