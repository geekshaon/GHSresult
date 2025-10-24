import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio 
import numpy as np

# --- 1. CONFIGURATION AND DATA LOADING ---

# Set Streamlit page configuration
st.set_page_config(
    page_title="SSC Result Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Set the default Plotly template globally to a standard, eye-catching option
pio.templates.default = 'seaborn' 

# Load and clean data with caching for efficiency
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    # Clean column names by stripping leading/trailing whitespace
    df.columns = df.columns.str.strip()
    return df

df = load_data("data.csv")
df_agg = df.copy() 

# --- Inject Custom CSS for Center Alignment, Styling, and MODERN CARDS (UPDATED) ---
st.markdown("""
<style>
/* Center the main title and subheader using specific selectors */
.st-emotion-cache-18ni2g6 p, .st-emotion-cache-10o4uv .st-emotion-cache-18ni2g6 p, .st-emotion-cache-10o4uv .st-emotion-cache-18ni2g6 div {
    text-align: center;
}
/* Ensure all headers (h1, h2, h3) are centered */
h1, h2, h3, h4 {
    text-align: center;
}
/* Style the main header for emphasis */
h1 {
    color: #0E7490; /* Vibrant Teal */
}
/* Style the section headers */
h2 {
    color: #DC2626; /* Contrasting Red */
}

/* --- MODERN CARD STYLES (UPDATED FOR TEXT SIZE, BOLD, AND CENTER) --- */
.metric-card {
    background-color: #ffffff; /* White background for card */
    padding: 15px 15px 5px 15px; 
    border-radius: 10px; 
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
    border-left: 5px solid #0E7490; /* Left border accent */
    margin-bottom: 20px; 
    height: 100px; 
    display: flex;
    flex-direction: column;
    justify-content: center; /* Centers content vertically */
    text-align: center; /* Ensure horizontal center for entire card content */
}
.metric-card .card-label {
    font-size: 18px; /* Increased size */
    color: #4b5563; 
    margin-bottom: 5px;
    font-weight: bold; /* Made bold */
    text-align: center; /* Centered */
}
.metric-card .card-value {
    font-size: 28px; 
    font-weight: bold; 
    color: #1f2937; 
    line-height: 1; 
    text-align: center; /* Centered */
}


/* Style the footer - fixed position at the bottom */
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f0f2f6; 
    color: #333;
    text-align: center;
    padding: 10px;
    font-size: 0.8em;
    z-index: 1000; 
}
</style>
""", unsafe_allow_html=True)


# --- Helper Function to Display the Styled Metric Card ---
def display_metric_card_styled(column, label, value):
    column.markdown(f"""
    <div class="metric-card">
        <div class="card-label">{label}</div>
        <div class="card-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


# --- 2. AGGREGATE METRICS FOR OVERALL CARDS ---

overall_data = df_agg.agg({
    'Examinee': 'sum', 'Male': 'sum', 'Female': 'sum', 'Total Passed': 'sum', 'Appeared': 'sum',
    'Total GPA 5': 'sum', 'Male Passed': 'sum', 'Female Passed': 'sum', 'GPA 5 - Male': 'sum',
    'GPA 5 - Female': 'sum', 'BS_Appeared': 'sum', 'BUSINESS STUDIES Passed': 'sum',
    'BUSINESS STUDIES GPA 5': 'sum', 'HUM_Appeared': 'sum', 'HUMANITIES Passed': 'sum',
    'HUMANITIES GPA 5': 'sum', 'SCI_Appeared': 'sum', 'SCIENCE Passed': 'sum',
    'SCIENCE GPA 5': 'sum',
}).to_dict()

overall_data['Total Failed'] = overall_data['Appeared'] - overall_data['Total Passed']

# --- 3. IMAGE BANNER AND TITLES ---

# st.markdown("""
# <div style='text-align: center;'>
#     <img src='https://via.placeholder.com/1200x200/228B22/FFFFFF?text=Gobindashi+High+School+Banner' style='width: 100%; max-width: 1200px; margin-bottom: 20px; border-radius: 10px;'>
# </div>
# """, unsafe_allow_html=True) 

st.title("Gobindashi High School")
st.subheader("SSC Result analysis year 2011 to 2025")

st.markdown("---") 

st.header("1. Overall Performance (All Years)")

# --- 4. OVERALL METRICS CARDS (3-COLUMN LAYOUT) ---
st.subheader("Key Performance Indicators (KPIs)")

# Row 1: General Metrics
col1, col2, col3 = st.columns(3)
display_metric_card_styled(col1, "Total Examinees", f"{overall_data['Examinee']:,}")
display_metric_card_styled(col2, "Total Passed", f"{overall_data['Total Passed']:,}")
display_metric_card_styled(col3, "Total Failed", f"{overall_data['Total Failed']:,}")

# Row 2: Gender and GPA 5
col4, col5, col6 = st.columns(3)
display_metric_card_styled(col4, "Total Male Examinees", f"{overall_data['Male']:,}")
display_metric_card_styled(col5, "Total Female Examinees", f"{overall_data['Female']:,}")
display_metric_card_styled(col6, "Total GPA 5 Achieved", f"{overall_data['Total GPA 5']:,}")

# Row 3 & 4: Department Performance
st.markdown("<h3 style='text-align: center;'>Departmental Performance</h3>", unsafe_allow_html=True)
col7, col8, col9 = st.columns(3)
display_metric_card_styled(col7, "BS Examinees", f"{overall_data['BS_Appeared']:,}")
display_metric_card_styled(col8, "HUM Examinees", f"{overall_data['HUM_Appeared']:,}")
display_metric_card_styled(col9, "SCI Examinees", f"{overall_data['SCI_Appeared']:,}")

col10, col11, col12 = st.columns(3)
display_metric_card_styled(col10, "BS Passed", f"{overall_data['BUSINESS STUDIES Passed']:,}")
display_metric_card_styled(col11, "HUM Passed", f"{overall_data['HUMANITIES Passed']:,}")
display_metric_card_styled(col12, "SCI Passed", f"{overall_data['SCIENCE Passed']:,}")

st.markdown("---") 

# --- 5. OVERALL DATA RELATIONS (CHARTS) (3-COLUMN LAYOUT) ---

st.subheader("Overall Data Relations")

# Prepare dataframes for charts
examinee_pass_data = pd.DataFrame({'Category': ['Passed', 'Failed'], 'Count': [overall_data['Total Passed'], overall_data['Total Failed']]})
gender_examinee_data = pd.DataFrame({'Gender': ['Male', 'Female'], 'Count': [overall_data['Male'], overall_data['Female']]})
gender_pass_data = pd.DataFrame({'Gender': ['Male Passed', 'Female Passed'], 'Count': [overall_data['Male Passed'], overall_data['Female Passed']]})
dept_examinee_data = pd.DataFrame({'Department': ['Business Studies', 'Humanities', 'Science'], 'Count': [overall_data['BS_Appeared'], overall_data['HUM_Appeared'], overall_data['SCI_Appeared']]})
dept_gpa5_data = pd.DataFrame({'Department': ['Business Studies', 'Humanities', 'Science'], 'Count': [overall_data['BUSINESS STUDIES GPA 5'], overall_data['HUMANITIES GPA 5'], overall_data['SCIENCE GPA 5']]})
gender_gpa5_data = pd.DataFrame({'Gender': ['Male GPA 5', 'Female GPA 5'], 'Count': [overall_data['GPA 5 - Male'], overall_data['GPA 5 - Female']]})

# Row 1 of Charts (3 columns)
col_a, col_b, col_c = st.columns(3)

with col_a:
    fig_a = px.pie(examinee_pass_data, values='Count', names='Category', title='Examinees vs Passed (All Years)', hole=.3)
    col_a.plotly_chart(fig_a) # Removed width='stretch'

with col_b:
    fig_b = px.pie(gender_examinee_data, values='Count', names='Gender', title='Male vs Female Examinees (All Years)', hole=.3)
    col_b.plotly_chart(fig_b) # Removed width='stretch'

with col_c:
    fig_c = px.pie(gender_pass_data, values='Count', names='Gender', title='Male vs Female Passed (All Years)', hole=.3)
    col_c.plotly_chart(fig_c) # Removed width='stretch'

# Row 2 of Charts (3 columns)
col_d, col_e, col_f = st.columns(3)

with col_d:
    fig_d = px.pie(dept_examinee_data, values='Count', names='Department', title='Examinee Distribution by Department', hole=.3)
    col_d.plotly_chart(fig_d) # Removed width='stretch'

with col_e:
    fig_e = px.pie(dept_gpa5_data, values='Count', names='Department', title='GPA 5 Distribution by Department', hole=.3)
    col_e.plotly_chart(fig_e) # Removed width='stretch'

with col_f:
    fig_f = px.pie(gender_gpa5_data, values='Count', names='Gender', title='Male vs Female GPA 5', hole=.3)
    col_f.plotly_chart(fig_f) # Removed width='stretch'

# Row 3: Department Pass vs Fail (Individual Pie Charts)
st.markdown("#### Pass vs Fail by Department")
col_g, col_h, col_i = st.columns(3)

dept_pass_fail_data = pd.DataFrame({
    'Department': ['Business Studies', 'Humanities', 'Science'],
    'Passed': [overall_data['BUSINESS STUDIES Passed'], overall_data['HUMANITIES Passed'], overall_data['SCIENCE Passed']],
    'Failed': [
        overall_data['BS_Appeared'] - overall_data['BUSINESS STUDIES Passed'],
        overall_data['HUM_Appeared'] - overall_data['HUMANITIES Passed'],
        overall_data['SCI_Appeared'] - overall_data['SCIENCE Passed']
    ]
})

departments = ['Business Studies', 'Humanities', 'Science']
cols = [col_g, col_h, col_i]

for i, dept in enumerate(departments):
    dept_df = pd.DataFrame({
        'Status': ['Passed', 'Failed'],
        'Count': [dept_pass_fail_data.iloc[i]['Passed'], dept_pass_fail_data.iloc[i]['Failed']]
    })
    
    fig_dept = px.pie(dept_df, values='Count', names='Status', title=f'{dept} Pass vs Fail', hole=.3)
    cols[i].plotly_chart(fig_dept) # Removed width='stretch'


# --- 6. TREND ANALYSIS (LINE GRAPHS) (SINGLE COLUMN) ---

st.markdown("---")
st.header("2. Annual Performance Trends")

# Ensure Year is sorted for line graphs
df_sorted = df.sort_values(by='Year', ascending=True)

# Line Graph 1: Pass Rate Trend
st.subheader("Year-wise Pass Percentage Trend")
fig_pass_rate = px.line(
    df_sorted,
    x='Year',
    y='Percentage of Pass',
    title='SSC Pass Percentage Trend (2011 - 2025)',
    markers=True,
    labels={'Percentage of Pass': 'Pass Rate (%)', 'Year': 'Year'},
)
fig_pass_rate.update_xaxes(dtick=1) 
st.plotly_chart(fig_pass_rate) # Removed width='stretch'

# Line Graph 2: GPA 5 Count Trend
st.subheader("Year-wise GPA 5 Count Trend")
fig_gpa5_count = px.line(
    df_sorted,
    x='Year',
    y='Total GPA 5',
    title='Total GPA 5 Achieved Trend (2011 - 2025)',
    markers=True,
    labels={'Total GPA 5': 'Total GPA 5 Count', 'Year': 'Year'},
)
fig_gpa5_count.update_xaxes(dtick=1) 
st.plotly_chart(fig_gpa5_count) # Removed width='stretch'

# --- 7. YEAR-SPECIFIC DATA SECTION (INTERACTIVE) ---

st.markdown("---")
st.header("3. Year-Specific Analysis")

# Year Selector (default to 2025, reverse sorted)
year_options = sorted(df['Year'].unique().tolist(), reverse=True)
selected_year = st.selectbox(
    'Select a Year for Detailed Analysis:',
    options=year_options,
    index=year_options.index(2025) if 2025 in year_options else 0
)

# Filter data for the selected year
df_year = df[df['Year'] == selected_year].iloc[0]

st.subheader(f"Detailed Results for Year {selected_year}")

# Row 1: Year-Specific Charts (3 columns)
col_y1, col_y2, col_y3 = st.columns(3)

# Chart 1: Examinee vs Pass
year_pass_data = pd.DataFrame({
    'Category': ['Passed', 'Failed'],
    'Count': [df_year['Total Passed'], df_year['Appeared'] - df_year['Total Passed']]
})
with col_y1:
    fig_y1 = px.pie(year_pass_data, values='Count', names='Category', title=f'{selected_year} Examinee vs Passed', hole=.3)
    col_y1.plotly_chart(fig_y1) # Removed width='stretch'

# Chart 2: Male vs Female Examinee
year_gender_examinee_data = pd.DataFrame({
    'Gender': ['Male', 'Female'],
    'Count': [df_year['Male'], df_year['Female']]
})
with col_y2:
    fig_y2 = px.pie(year_gender_examinee_data, values='Count', names='Gender', title=f'{selected_year} Male vs Female Examinees', hole=.3)
    col_y2.plotly_chart(fig_y2) # Removed width='stretch'

# Chart 3: Department Examinee
year_dept_examinee_data = pd.DataFrame({
    'Department': ['Business Studies', 'Humanities', 'Science'],
    'Count': [df_year['BS_Appeared'], df_year['HUM_Appeared'], df_year['SCI_Appeared']]
})
with col_y3:
    fig_y3 = px.pie(year_dept_examinee_data, values='Count', names='Department', title=f'{selected_year} Dept. Examinee Distribution', hole=.3)
    col_y3.plotly_chart(fig_y3) # Removed width='stretch'


# Row 2: Year-Specific Charts (3 columns)
col_y4, col_y5, col_y6 = st.columns(3)

# Chart 4: Department Pass vs Fail (Bar Chart - Recommended for comparison)
year_dept_pass_fail_data = pd.DataFrame({
    'Department': ['Business Studies', 'Humanities', 'Science'],
    'Passed': [df_year['BUSINESS STUDIES Passed'], df_year['HUMANITIES Passed'], df_year['SCIENCE Passed']],
    'Failed': [
        df_year['BS_Appeared'] - df_year['BUSINESS STUDIES Passed'],
        df_year['HUM_Appeared'] - df_year['HUMANITIES Passed'],
        df_year['SCI_Appeared'] - df_year['SCIENCE Passed']
    ]
}).set_index('Department').T.melt(ignore_index=False, var_name='Department', value_name='Count').reset_index().rename(columns={'index': 'Status'})

with col_y4:
    fig_y4 = px.bar(
        year_dept_pass_fail_data,
        x='Department',
        y='Count',
        color='Status',
        title=f'{selected_year} Dept. Pass vs Fail',
        barmode='group'
    )
    col_y4.plotly_chart(fig_y4) # Removed width='stretch'

# Chart 5: Department GPA 5
year_dept_gpa5_data = pd.DataFrame({
    'Department': ['Business Studies', 'Humanities', 'Science'],
    'GPA 5 Count': [df_year['BUSINESS STUDIES GPA 5'], df_year['HUMANITIES GPA 5'], df_year['SCIENCE GPA 5']]
})
with col_y5:
    fig_y5 = px.bar(
        year_dept_gpa5_data,
        x='Department',
        y='GPA 5 Count',
        title=f'{selected_year} GPA 5 by Department'
    )
    col_y5.plotly_chart(fig_y5) # Removed width='stretch'

# Chart 6: GPA 5 Male vs Female
year_gender_gpa5_data = pd.DataFrame({
    'Gender': ['Male GPA 5', 'Female GPA 5'],
    'Count': [df_year['GPA 5 - Male'], df_year['GPA 5 - Female']]
})
with col_y6:
    fig_y6 = px.pie(year_gender_gpa5_data, values='Count', names='Gender', title=f'{selected_year} GPA 5: Male vs Female', hole=.3)
    col_y6.plotly_chart(fig_y6) # Removed width='stretch'


# --- 8. RAW DATA TABLE ---
# Add extra margin to ensure the Raw Data table is visible above the fixed footer
st.markdown("<div style='margin-bottom: 50px;'></div>", unsafe_allow_html=True) 

st.markdown("---")
st.header("4. Raw Data Table")
# Removed width='stretch' from st.dataframe
st.dataframe(df) 

# --- 9. FOOTER (FIXED POSITION) ---
# Footer is fixed at the bottom of the page
st.markdown(f"""
<div class='footer'>
    Developed by <a href='#' style='color: #DC2626; text-decoration: none;'>Mehedi Hasan</a>
</div>
""", unsafe_allow_html=True)