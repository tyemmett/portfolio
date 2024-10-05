import streamlit as st
import pandas as pd
import altair as alt

# Load the CSV data
file_path = 'career_progression.csv'  # Update with the path to your CSV file
career_data = pd.read_csv(file_path)
career_data['year'] = pd.to_datetime(career_data['year'], format='%Y')
career_data['year_str'] = career_data['year'].dt.strftime('%Y')  # Convert for better plotting

# Set up the Streamlit app
st.title('Career Progression and Learning Timeline')

# Add a text description if desired
st.write("""
This interactive timeline shows the key milestones in my career and learning journey.
Hover over each point to see detailed information.
""")

# Create the Altair chart
chart = alt.Chart(career_data).mark_circle(size=100).encode(
    x='year:T',
    y=alt.Y('type:N', title='Event Type'),
    color='type',
    tooltip=['year_str', 'role', 'skills', 'notable_accomplishment']
).properties(
    width=800,
    height=400,
    title='Career and Learning Timeline'
)

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)