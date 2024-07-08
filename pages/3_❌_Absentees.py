import streamlit as st
import pandas as pd
import plotly.express as px

st.session_state.data_option = st.sidebar.selectbox(label='Select Contest Name', options=[
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
    st.sidebar.header(st.session_state.data_option)
    
    data = st.session_state.data
    
    #st.set_page_config(layout="wide")
    
    st.header("Absentee Details:")
    
    # Define unique values for filters
    departments = ["All"] + list(data['Department'].unique())
    years = ["All"] + list(data['Year'].unique())
    domains = ["All"] + list(data['Domain'].unique())
    
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
    name = st.sidebar.text_input('Name')
    
    
    
    # Filter data based on selections
    filtered_data = data.copy()
    if year != 'All':
        filtered_data = filtered_data[filtered_data['Year'] == year]
    if department != 'All':
        filtered_data = filtered_data[filtered_data['Department'] == department]
    if domain != 'All':
        filtered_data = filtered_data[filtered_data['Domain'] == domain]
    if name:
        filtered_data = filtered_data[filtered_data['Name'].str.contains(name, case=False)]
    
    
    absentees = filtered_data[filtered_data['Rank']==0].reset_index(drop=True)
    #absentees.index += 1
    
    range = st.sidebar.slider("Select No. of Absentees to be Shown",0,len(absentees), (0,len(absentees)))
    
    st.table(absentees[['Name', 'Year', 'Domain', 'Department','Mobile Number']][range[0]:range[1]+1])
    
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    
    csv = convert_df(absentees)
    
    st.download_button(
        label="Download Absentee data",
        data=csv,
        file_name='LeetCode Weekly Contest Absentees.csv',
        mime='text/csv',
    )
