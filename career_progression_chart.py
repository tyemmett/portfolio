import streamlit as st
import pandas as pd
import altair as alt
import datetime

# Load the CSV data
file_path = 'career_progression.csv'  
career_data = pd.read_csv(file_path)

# Combine year and month into a datetime 
career_data['date'] = pd.to_datetime(career_data['year'].astype(str) + '-' + career_data['month'], format='%Y-%B')
career_data['date_str'] = career_data['date'].dt.strftime('%Y-%B')  # Convert for better plotting

# Set wide layout for Streamlit app
st.set_page_config(layout="wide")

# Set up the Streamlit app
st.title('Career Progression and Learning Timeline')

# Add a text description 
st.write("""
This interactive timeline shows the key milestones in my career and learning journey.
Hover over each point to see detailed information. You can also filter out everything prior to the start of my IT Career in 2016.
""")

# Toggle button to filter only IT-related events (after 8/1/2016)
show_it_only = st.checkbox('Show IT only')

# Create a datetime object for filtering
cutoff_date = datetime.datetime(2016, 8, 1)

# Filter the dataframe based on the toggle
if show_it_only:
    filtered_data = career_data[career_data['date'] >= cutoff_date]
else:
    filtered_data = career_data

# Create the Altair chart with calculated vertical offsets for duplicate points
chart = alt.Chart(filtered_data).mark_circle(size=400).encode(
    x=alt.X('date:T', title='Month and Year', axis=alt.Axis(format='%b %Y')),
    y=alt.Y('type:N', title='Event Type'),
    color=alt.Color('type:N', scale=alt.Scale(scheme='set1')),
    tooltip=['date_str', 'role', 'skills', 'notable_acomplishment']
).transform_window(
    rank='rank()',
    sort=[alt.SortField('role', order='ascending')],
    groupby=['date', 'type']
).transform_calculate(
    y_offset='datum.rank * 1'  # Apply a small vertical offset for each rank
).encode(
    y=alt.Y('type:N', title='Event Type'),
    yOffset='y_offset:Q'
).properties(
    width=700,
    height=600,
    title='Career and Learning Timeline'
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
