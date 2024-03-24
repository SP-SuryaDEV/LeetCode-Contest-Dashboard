import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import io
from PIL import Image

# Load data
data = pd.read_csv('data.csv')

# st.set_page_config(layout="wide")

# Define unique values for filters
departments = ["All"] + list(data['Department'].unique())
years = ["All"] + list(data['Year'].unique())
domains = ["All"] + list(data['Domain'].unique())

# Sidebar layout
st.sidebar.header("Filter Data")
department = st.sidebar.selectbox('Department', departments, index=0)
year = st.sidebar.selectbox('Year', years, index=0)
domain = st.sidebar.selectbox('Domain', domains, index=0)

# Filter data based on selections
filtered_data = data.copy()
if year != 'All':
    filtered_data = filtered_data[filtered_data['Year'] == year]
if department != 'All':
    filtered_data = filtered_data[filtered_data['Department'] == department]
if domain != 'All':
    filtered_data = filtered_data[filtered_data['Domain'] == domain]

# Main content layout
fig, axs = plt.subplots(2, 2, figsize=(22, 15))

# Plot 1: Presence Distribution (Pie Chart)
rank_presence = filtered_data['Rank'].apply(lambda x: 'Absent' if x == 0 else 'Present')
presence_counts = rank_presence.value_counts()
colors = ['green','red']
axs[0, 0].pie(presence_counts, labels=[f"{presence} ({count})" for presence, count in presence_counts.items()], autopct='%1.1f%%',colors=colors)
axs[0, 0].set_title('Presence Distribution')

# Plot 2: Problems Solved Count (Bar Chart)
problem_counts = range(5)
problems_count = filtered_data[filtered_data['Rank'] != 0]['ProbCount'].value_counts()
problem_data = pd.DataFrame({'Problems': problem_counts,
                             'Count': [problems_count.get(count, 0) for count in problem_counts]})
colors = ['red','brown','orange','yellow','green']
axs[0, 1].bar(problem_data['Problems'], problem_data['Count'],color=colors)
axs[0, 1].set_title('Problems Solved')

# Display problem-wise counts
for i, count in enumerate(problem_data['Count']):
    axs[0, 1].text(problem_data['Problems'][i], count, str(count), ha='center', va='bottom')

# Plot 3: Top 10 Performers (Rank Performance)
viridis_colors = [
    "#440154",  # Deep purple-blue
    "#482878",
    "#3e4989",
    "#31688e",
    "#26828e",
    "#1f9e89",
    "#35b779",
    "#6dcd59",
    "#b4dd2c",
    "#fde725"   # Vibrant yellow-green
]

sorted_filtered = filtered_data[filtered_data['Rank'] > 0].sort_values(by='Rank').head(10)[::-1]
names_with_ranks = [f"{name} ({len(sorted_filtered) - rank}{'th' if (len(sorted_filtered) - rank) % 10 == 0 or (len(sorted_filtered) - rank) % 10 >= 4 or 10 < (len(sorted_filtered) - rank) % 100 < 20 else ['st', 'nd', 'rd'][(len(sorted_filtered) - rank) % 10 - 1]} Rank)" for rank, name in enumerate(sorted_filtered['Name'])]
axs[1, 0].barh(names_with_ranks, sorted_filtered['Rank'],color=viridis_colors)
axs[1, 0].set_xlabel('Ranking Score')
axs[1, 0].set_ylabel('Name')
axs[1, 0].set_title('Top 10 Performers')
# Display the rank above each bar
for i, rank in enumerate(sorted_filtered['Rank']):
    axs[1, 0].text(rank, i, str(rank), ha='left', va='bottom')

# Plot 4: Rank Range Distribution
plasma_colors = [
    "#0d0887",  # Deep purple-blue
    "#46039f",
    "#7201a8",
    "#9c179e",
    "#bd3786",
    "#d8576b",
    "#ed7953",
    "#fb9f3a",
    "#fdca26",
    "#f0f921"   # Vibrant yellow-green
]
bins = [0, 5000, 10000, 15000, 20000, 25000, 30000]
bin_labels = ['0-5000', '5000-10000', '10000-15000', '15000-20000', '20000-25000', '25000-30000']
categories = pd.cut(filtered_data[filtered_data['Rank'] != 0]['Rank'], bins=bins, labels=bin_labels, ordered=True)
rank_counts = categories.value_counts().reindex(bin_labels, fill_value=0)
rank_data = pd.DataFrame({'Rank Range': rank_counts.index, 'Count': rank_counts.values})
axs[1, 1].bar(rank_data['Rank Range'], rank_data['Count'],color=plasma_colors)
axs[1, 1].set_title('Rank Range Distribution')
# Display the count above each bar
for i, count in enumerate(rank_data['Count']):
    axs[1, 1].text(rank_data['Rank Range'][i], count, str(count), ha='center', va='bottom')

# Save figure as image
  
#fig.suptitle('LeetCode Weekly Contest Data', fontsize=40, y=.97)
#fig_text = 'LeetCode Weekly Data'  # Text to be underlined
fig_text = f'LeetCode Weekly Contest Data [24/03/2024] ({department if department != "All" else "All Depts."}) - [{year if year != "All" else "All"}]'  # Dynamic title based on department filter  # Text to be underlined
fig.suptitle(fig_text, fontsize=40, y=.96, fontweight='bold', color='black', style='italic', bbox=dict(facecolor='none', edgecolor='none', boxstyle='round,pad=0.5'))  # Underlined text using bbox

image_stream = io.BytesIO()

# Change the background color to pale
skin_color_rgb = (255/255, 255/255, 224.9/255)
fig.patch.set_facecolor(skin_color_rgb)
plt.rcParams.update({'font.family': 'serif', 'font.size': 12})

dpi = 500

plt.savefig(image_stream, format='png', dpi=dpi)

# Display the image in Streamlit
st.image(image_stream, caption='Combined Plots', use_column_width=True)
image_stream.seek(0)

@st.cache_data
def saveDashboard():
    img = Image.open(image_stream)
    img.save(f'./{fig_text}.png')

saveDashboard()
    
with open(f"./{fig_text}.png", "rb") as file:
    btn = st.download_button(
            label="Download Dashboard",
            data=file,
            file_name=f"{fig_text}.png",
            mime="image/png"
          )
    if btn:
        st.success("Image saved successfully!")
