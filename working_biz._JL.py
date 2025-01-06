import pandas as pd
import streamlit as st

# Sample Data
data = {
    "Cash-in": [18000],
    "Enrl.": [32],
    "Self Gen. Ref.": [24],
    "Dec_Achv": [7243],
    "Dec_Achv.1": [4],
    "Dec_Achv.2": [7],
}
df = pd.DataFrame(data)

# Streamlit App
st.title("AC Target and Achievement Viewer with Styled Table")

# Custom HTML Table with Merged Cells
html_table = """
<table style="border-collapse: collapse; width: 100%; text-align: center;">
    <thead>
        <tr>
            <th rowspan="2" style="border: 1px solid black; padding: 5px;">Cash-in</th>
            <th colspan="2" style="border: 1px solid black; padding: 5px;">Dec</th>
            <th rowspan="2" style="border: 1px solid black; padding: 5px;">Self Gen. Ref.</th>
        </tr>
        <tr>
            <th style="border: 1px solid black; padding: 5px;">Enrl.</th>
            <th style="border: 1px solid black; padding: 5px;">Achv.</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">18,000</td>
            <td style="border: 1px solid black; padding: 5px;">32</td>
            <td style="border: 1px solid black; padding: 5px;">7,243</td>
            <td style="border: 1px solid black; padding: 5px;">24</td>
        </tr>
    </tbody>
</table>
"""

# Display the Table
st.markdown(html_table, unsafe_allow_html=True)
