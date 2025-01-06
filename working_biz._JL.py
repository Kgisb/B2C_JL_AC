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

# Display the filtered data dynamically
if not filtered_data.empty:
    st.subheader(f"Details for AC_Name: {selected_ac}")

    # Display dynamic details in a styled table
    st.dataframe(filtered_data)

    # Summary for the selected AC_Name
    st.subheader("Summary")
    summary = {
        "Cash-in Target (Total)": filtered_data["Cash-in Target"].sum(),
        "Cash-in Achieved (Total)": filtered_data["Cash-in Achieved"].sum(),
        "Enrl. Target (Total)": filtered_data["Enrl. Target"].sum(),
        "Enrl. Achieved (Total)": filtered_data["Enrl. Achieved"].sum(),
        "Self Gen. Ref. Target (Total)": filtered_data["Self Gen. Ref. Target"].sum(),
        "Self Gen. Ref. Achieved (Total)": filtered_data["Self Gen. Ref. Achieved"].sum(),
    }
    summary_df = pd.DataFrame([summary])
    st.table(summary_df)

    # Optional: Weekly breakdown
    st.subheader("Weekly Breakdown (Optional)")
    for week in ["WK_1", "WK_2", "WK_3", "WK_4"]:
        if any(filtered_data.columns.str.contains(week)):
            weekly_summary = {
                f"Cash-in Target {week}": filtered_data.get(f"Cash-in Target {week}", pd.Series(0)).sum(),
                f"Cash-in Achieved {week}": filtered_data.get(f"Cash-in Achieved {week}", pd.Series(0)).sum(),
                f"Enrl. Target {week}": filtered_data.get(f"Enrl. Target {week}", pd.Series(0)).sum(),
                f"Enrl. Achieved {week}": filtered_data.get(f"Enrl. Achieved {week}", pd.Series(0)).sum(),
                f"Self Gen. Ref. Target {week}": filtered_data.get(f"Self Gen. Ref. Target {week}", pd.Series(0)).sum(),
                f"Self Gen. Ref. Achieved {week}": filtered_data.get(f"Self Gen. Ref. Achieved {week}", pd.Series(0)).sum(),
            }
            st.write(f"Weekly Breakdown for {week}")
            st.table(pd.DataFrame([weekly_summary]))
else:
    st.warning(f"No data available for the selected AC_Name: {selected_ac}.")
