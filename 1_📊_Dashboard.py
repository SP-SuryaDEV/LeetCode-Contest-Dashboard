import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Leetcode Contest's Dashboard",
    page_icon="🧊",
    layout="wide")

st.session_state.data_option = st.sidebar.selectbox(label='Select Contest Name', options=[
    'Leetcode Weekly Contest - 409 [04.08.2024]',
    'Leetcode Biweekly Contest - 136 [03.08.2024]',
    'Leetcode Weekly Contest - 408 [28.07.2024]',
    'Leetcode Weekly Contest - 407 [21.07.2024]',
    'Leetcode Weekly Contest - 406 [14.07.2024]',
    'Leetcode Weekly Contest - 405 [07.07.2024]',
    'Leetcode Biweekly Contest - 134 [06.07.2024]',
    'Leetcode Biweekly Contest - 130 [11.05.2024]',
    'Leetcode Weekly Contest - 397 [12.05.2024]'
])

#Load data once
if st.session_state.get('data_option'):
    if st.session_state.data_option == 'Leetcode Biweekly Contest - 130 [11.05.2024]':
        st.session_state.data = pd.read_csv('bw130.csv')
    elif st.session_state.data_option == 'Leetcode Weekly Contest - 397 [12.05.2024]':
        st.session_state.data = pd.read_csv('w397.csv')
    elif st.session_state.data_option == 'Leetcode Weekly Contest - 405 [07.07.2024]':
        st.session_state.data = pd.read_csv('w405.csv')
    elif st.session_state.data_option == 'Leetcode Biweekly Contest - 134 [06.07.2024]':
        st.session_state.data = pd.read_csv('bw134.csv')
    elif st.session_state.data_option == 'Leetcode Weekly Contest - 406 [14.07.2024]':
        st.session_state.data = pd.read_csv('w406.csv')
    elif st.session_state.data_option == 'Leetcode Weekly Contest - 407 [21.07.2024]':
        st.session_state.data = pd.read_csv('w407.csv')
    elif st.session_state.data_option == 'Leetcode Weekly Contest - 408 [28.07.2024]':
        st.session_state.data = pd.read_csv('w408.csv')
    elif st.session_state.data_option == 'Leetcode Weekly Contest - 409 [04.08.2024]':
        st.session_state.data = pd.read_csv('w409.csv')
    elif st.session_state.data_options == 'Leetcode Biweekly Contest - 136 [03.08.2024]':
        st.session_state.data = pd.read_csv('bw136.csv')
    st.sidebar.header(st.session_state.data_option)
    
    data = st.session_state.data
    
    # st.set_page_config(layout="wide")
    st.session_state.filtered = data
    
    # Sidebar layout
    st.sidebar.header("Filter Data")
    
    years = ["All"] + list(st.session_state.data['Year'].unique())
    year_val = st.session_state.get('year')
    year = st.session_state.year = st.sidebar.selectbox('Year', years, index=0 if not year_val else years.index(year_val))
    
    departments = ["All"] + list(st.session_state.data['Department'].unique())
    
    if year != 'All':
        departments = ["All"] + list(st.session_state.data[data.Year == year]['Department'].unique())
    
    dept_val = st.session_state.get('department')
    department = st.session_state.department = st.sidebar.selectbox('Department', departments, index=0 if not dept_val else departments.index(dept_val))
    
    domains = ["All"] + list(st.session_state.data['Domain'].unique())
    
    if year != 'All' and department == 'All':
        domains = ["All"] + list(st.session_state.data[data.Year == year]['Domain'].unique())
    elif year != 'All' and department != 'All':
        domains = ["All"] + list(st.session_state.data[(data.Year == year) & (data.Department == department)]['Domain'].unique())
    
    domain_val = st.session_state.get('domain')
    domain = st.session_state.domain = st.sidebar.selectbox('Domain', domains, index=0 if not domain_val else domains.index(domain_val))
    
    # background_generator = BackgroundCSSGenerator()
    # page_bg_img = background_generator.generate_background_css()
    # st.markdown(page_bg_img, unsafe_allow_html=True)
    
    # Filter data based on selections
    filtered_data = st.session_state.filtered
    if year != 'All':
        filtered_data = filtered_data[filtered_data['Year'] == year]
    if department != 'All':
        filtered_data = filtered_data[filtered_data['Department'] == department]
    if domain != 'All':
        filtered_data = filtered_data[filtered_data['Domain'] == domain]
    
    # Main content layout
    st.title("LeetCode Weekly Contest Analysis:")
    st.divider()
    
    col1,col2 = st.columns([1,1])
    
    with col1:
    
        st.subheader("Domain-wise Distribution:")
        domain_counts = filtered_data['Domain'].value_counts()
        fig_domain = px.pie(values=domain_counts, names=domain_counts.index)
        fig_domain.update_traces(marker=dict(colors=px.colors.sequential.Cividis))
        fig_domain.update_layout(legend=dict(title='Domain',orientation='h', x=1, y=0.7))
        st.plotly_chart(fig_domain)
        cloud_count = sum(filtered_data['Domain'] == 'Cloud')
        fullstack_count = sum(filtered_data['Domain'] == 'FullStack')
        cybersecurity_count = sum(filtered_data['Domain'] == 'Cybersecurity')
        data_analytics_count = sum(filtered_data['Domain'] == 'Data Analytics')
        other_count = sum(filtered_data['Domain'] == 'Other')
        sde_count = sum(filtered_data['Domain'] == 'SDE')
    
        cols1 , cols2 ,cols3 ,cols4 ,cols5 ,cols6= st.columns([1,1,1,1,1,1])
    
        with cols1:
            st.metric("Cloud", cloud_count)
        with cols2:
            st.metric("FullStack", fullstack_count)
        with cols3:
            st.metric("SDE", sde_count)
        with cols4:
            st.metric("Data Analytics", data_analytics_count)
        with cols5:
            st.metric("Cybersecurity", cybersecurity_count)
        with cols6:
            st.metric("Other", other_count)
            
    
    
    with col2:
    
        st.subheader("Participants:")
        rank_presence = filtered_data['Rank'].apply(lambda x: 'Absent' if x == 0 else 'Present')
        presence_data = pd.DataFrame({'Presence': rank_presence.value_counts().index,
                                    'Count': rank_presence.value_counts().values})
        colors = ['green', 'red']
        fig_presence = px.pie(presence_data, values='Count', names='Presence', 
                            color_discrete_sequence=colors)
        fig_presence.update_layout(legend=dict(title='Presence', orientation='h', x=0.8, y=0.7)) 
    
        # Display the chart
        st.plotly_chart(fig_presence)
    
        cold1,cold2,cold3,cold4 = st.columns([1,1,1,1])
        with cold1:
            st.write("")
        with cold2:
            st.metric("Total Students", len(filtered_data))
        with cold3:
            st.metric("Total Present", presence_data[presence_data['Presence'] == 'Present']['Count'].values[0])
        with cold4:
            st.metric("Total Absent", presence_data[presence_data['Presence'] == 'Absent']['Count'].values[0])
            
    # Department-wise Distribution of Participants
            
    st.write("")
    st.write("")
    st.write("")
    st.write("_________")       
    dep1,dep2 = st.columns([1,1])
    with dep1:
        st.subheader('Best Performers:')
        filtered_no_zero = filtered_data[filtered_data['Rank'] > 0]
        sorted_filtered = filtered_no_zero.sort_values(by='Rank').head(10)
        sorted_filtered = sorted_filtered.sort_values(by='Rank', ascending=True)  # Sort by Rank ascending for better visualization
    
        sorted_filtered = sorted_filtered[::-1]
    
        # Add a new column 'Rank_Label' to represent the rank label for each name
        # Create a list of strings with names and their corresponding ranks in brackets
        names_with_ranks = [f"{name} ({len(sorted_filtered) - rank}{'th' if (len(sorted_filtered) - rank) % 10 == 0 or (len(sorted_filtered) - rank) % 10 >= 4 or 10 < (len(sorted_filtered) - rank) % 100 < 20 else ['st', 'nd', 'rd'][(len(sorted_filtered) - rank) % 10 - 1]} Rank)" for rank, name in enumerate(sorted_filtered['Name'])]
    
        # Update the y-axis with the modified list
        fig_top_performers = px.bar(sorted_filtered, y=names_with_ranks, x='Rank', 
                                    hover_data=['Year', 'Domain', 'Department', 'Score', 'ProbCount'],
                                    labels={'Rank': 'Ranking'},
                                    color='Rank',
                                    color_continuous_scale='viridis',
                                    title='Top 10 Performers (Intra College Ranking)',
                                    orientation='h')
        fig_top_performers.update_layout(xaxis_title='Ranking Score', yaxis_title='Name')
        st.plotly_chart(fig_top_performers)
    
    with dep2:
        st.subheader("Department-wise Distribution:")
        department_counts = data['Department'].value_counts()
        fig_department = px.pie(values=department_counts, names=department_counts.index)
        fig_department.update_traces(marker=dict(colors=px.colors.sequential.Viridis))
        fig_department.update_layout(legend=dict(title='Department',orientation='h', x=1, y=0.7))
        st.plotly_chart(fig_department)
    
    
    filtered_data_rank_not_zero = filtered_data[filtered_data['Rank'] != 0]
    
    st.divider()
    colf1 , colf2 = st.columns([1,1])
    
    with colf1:
    # Problems Solved Count
        st.subheader("Problems Solved Count")
        problem_counts = range(5)  # Assuming max problems solved can be 4
        problems_count = filtered_data_rank_not_zero['ProbCount'].value_counts()
        problem_data = pd.DataFrame({'Problems': problem_counts,
                                    'Count': [problems_count.get(count, 0) for count in problem_counts]})
    
        fig_problems = px.bar(problem_data, x='Problems', y='Count')
        fig_problems.update_traces(marker_color='skyblue')
        st.plotly_chart(fig_problems)
        # Calculate the count of participants who solved each specific number of problems
        problem_0_count = sum(filtered_data_rank_not_zero['ProbCount'] == 0)
        problem_1_count = sum(filtered_data_rank_not_zero['ProbCount'] == 1)
        problem_2_count = sum(filtered_data_rank_not_zero['ProbCount'] == 2)
        problem_3_count = sum(filtered_data_rank_not_zero['ProbCount'] == 3)
        problem_4_count = sum(filtered_data_rank_not_zero['ProbCount'] == 4)
        # Display total problems solved metric
        st.metric("Total Problems Solved", sum(problem_data['Count']))
        cool1,cool2,cool3,cool4,cool5 = st.columns([1,1,1,1,1])
        with cool1:
            st.metric("Problem 0 Solved", problem_0_count)
        with cool2:
            st.metric("Problem 1 Solved", problem_1_count)
        with cool3:
            st.metric("Problem 2 Solved", problem_2_count)
        with cool4:              
            st.metric("Problem 3 Solved", problem_3_count)
        with cool5:
            st.metric("Problem 4 Solved", problem_4_count)
        
    with colf2:
        # Rank Distribution by Range
        bins = [0, 5000, 10000, 15000, 20000, 25000, 30000]
        bin_labels = ['0-5000', '5000-10000', '10000-15000', '15000-20000', '20000-25000', '25000-30000']
    
        categories = pd.cut(filtered_data_rank_not_zero['Rank'], bins=bins, labels=bin_labels, ordered=True)
        rank_counts = categories.value_counts().reindex(bin_labels, fill_value=0)  # Reindex to ensure correct order
        rank_data = pd.DataFrame({'Rank Range': rank_counts.index, 'Count': rank_counts.values})
    
        # Create the bar chart
        fig_rank = px.bar(rank_data, x='Rank Range', y='Count')
    
        # Update bar color
        fig_rank.update_traces(marker_color='purple')
    
        # Display the chart
        st.subheader("Rank Range Distribution:")
        st.plotly_chart(fig_rank)
        go1,go2 =st.columns([0.15,1])
        with go1:
            st.write("")
        with go2:
        #st.subheader("Rank Range:")rank_data.iloc[0]['Rank Range'], rank_data.iloc[0]['Count']
         st.metric('Total Ranks Secured',len(filtered_data_rank_not_zero['Rank']))
        # st.write("")
        # st.write("")
        
        cod1,cod2,cod3,cod4,cod5,cod6,cod7 = st.columns([1,1,1,1,1,1,1])
        with cod1:
            st.write("")
        with cod2:
            st.metric(rank_data.iloc[0]['Rank Range'], rank_data.iloc[0]['Count'])
        with cod3:
            st.metric(rank_data.iloc[1]['Rank Range'], rank_data.iloc[1]['Count'])
        with cod4:
            st.metric(rank_data.iloc[2]['Rank Range'], rank_data.iloc[2]['Count'])
        with cod5:
            st.metric(rank_data.iloc[3]['Rank Range'], rank_data.iloc[3]['Count'])
        with cod6:
            st.metric(rank_data.iloc[4]['Rank Range'], rank_data.iloc[4]['Count'])
        with cod7:
            st.metric(rank_data.iloc[5]['Rank Range'], rank_data.iloc[5]['Count'])
            
    
    st.write("")
    st.write("") 
    st.write("") 
    st.divider()
# colll1,colll2,colll3 = st.columns([1,1,1.9])

# with colll1:
#     st.write("")

# with colll2:
#     st.subheader('Best Performers:')
#     filtered_no_zero = filtered_data[filtered_data['Rank'] > 0]
#     sorted_filtered = filtered_no_zero.sort_values(by='Rank').head(10)
#     sorted_filtered = sorted_filtered.sort_values(by='Rank', ascending=True)  # Sort by Rank ascending for better visualization

#     sorted_filtered = sorted_filtered[::-1]

#     # Add a new column 'Rank_Label' to represent the rank label for each name
#     # Create a list of strings with names and their corresponding ranks in brackets
#     names_with_ranks = [f"{name} ({len(sorted_filtered) - rank}{'th' if (len(sorted_filtered) - rank) % 10 == 0 or (len(sorted_filtered) - rank) % 10 >= 4 or 10 < (len(sorted_filtered) - rank) % 100 < 20 else ['st', 'nd', 'rd'][(len(sorted_filtered) - rank) % 10 - 1]} Rank)" for rank, name in enumerate(sorted_filtered['Name'][::-1])]

#     # Update the y-axis with the modified list
#     fig_top_performers = px.bar(sorted_filtered, y=names_with_ranks, x='Rank', 
#                                 hover_data=['Year', 'Domain', 'Department', 'Score', 'ProbCount'],
#                                 labels={'Rank': 'Ranking'},
#                                 color='Rank',
#                                 color_continuous_scale='viridis',
#                                 title='Top 10 Performers by Rank (Intra College Ranking)',
#                                 orientation='h')
#     fig_top_performers.update_layout(xaxis_title='Ranking Score', yaxis_title='Name')
#     st.plotly_chart(fig_top_performers)

# with colll3:
#     st.write("")

# # Custom CSS styling
# st.markdown("""
#     <style>
#         body {
#             background-color: #f0f2f6;
#         }
#         .sidebar .sidebar-content {
#             background-color: #ffffff;
#             color: #333333;
#         }
#         .stButton>button {
#             color: #ffffff;
#             background-color: #4CAF50;
#             border-color: #4CAF50;
#         }
#         .stButton>button:hover {
#             background-color: #45a049;
#             border-color: #45a049;
#         }
#         .fullScreenFrame {
#             background-color: #f0f2f6 !important;
#         }
#         .stTable {
#             background-color: #ffffff;
#             color: #333333;
#         }
#     </style>
# """, unsafe_allow_html=True)
