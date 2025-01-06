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

if not filtered_data.empty:
    # Custom HTML Table with Merged Header
    html_table = f"""
    <table style="border-collapse: collapse; width: 100%; text-align: center; border: 1px solid black;">
        <thead>
            <tr>
                <th rowspan="2" style="border: 1px solid black; padding: 5px;">AC Name</th>
                <th colspan="3" style="border: 1px solid black; padding: 5px;">Dec</th>
                <th rowspan="2" style="border: 1px solid black; padding: 5px;">Cash-in Achieved</th>
                <th rowspan="2" style="border: 1px solid black; padding: 5px;">Enrl. Achieved</th>
                <th rowspan="2" style="border: 1px solid black; padding: 5px;">Self Gen. Ref. Achieved</th>
            </tr>
            <tr>
                <th style="border: 1px solid black; padding: 5px;">Cash-in Target</th>
                <th style="border: 1px solid black; padding: 5px;">Enrl. Target</th>
                <th style="border: 1px solid black; padding: 5px;">Self Gen. Ref. Target</th>
            </tr>
        </thead>
        <tbody>
    """
    # Generate rows dynamically based on the filtered data
    for _, row in filtered_data.iterrows():
        html_table += f"""
            <tr>
                <td style="border: 1px solid black; padding: 5px;">{row['AC_Name']}</td>
                <td style="border: 1px solid black; padding: 5px;">{row['Cash-in Target']}</td>
                <td style="border: 1px solid black; padding: 5px;">{row['Enrl. Target']}</td>
                <td style="border: 1px solid black; padding: 5px;">{row['Self Gen. Ref. Target']}</td>
                <td style="border: 1px solid black; padding: 5px;">{row['Cash-in Achieved']}</td>
                <td style="border: 1px solid black; padding: 5px;">{row['Enrl. Achieved']}</td>
                <td style="border: 1px solid black; padding: 5px;">{row['Self Gen. Ref. Achieved']}</td>
            </tr>
        """
    html_table += """
        </tbody>
    </table>
    """
    # Display the custom table
    st.markdown(html_table, unsafe_allow_html=True)

    # Summary of Weekly Data (Optional)
    st.subheader("Weekly Summary")
    st.write("This can be added if needed for detailed weekly breakdowns.")
else:
    st.warning("No data available for the selected AC_Name.")
