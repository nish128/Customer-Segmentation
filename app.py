import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

# --- Modern Header & CSS with Branding ---
st.set_page_config(page_title="Customer Segmentation Dashboard by Nisha Nayani", layout="wide")
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
    html, body, .stApp { font-family: 'Poppins', Arial, sans-serif !important; background: #f7fafd !important; }
    .block-container { padding-top: 2rem; }
    .banner {
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 18px;
        box-shadow: 0 4px 24px 0 rgba(0,0,0,0.10);
        padding: 1.5rem 1rem 1.5rem 1rem;
        margin-bottom: 2rem;
        text-align: center;
        color: #1976d2;
        font-size: 2.5rem;
        font-weight: 600;
        letter-spacing: 1px;
        font-family: 'Poppins', Arial, sans-serif;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1.25rem;
        margin-bottom: 1.5rem;
        font-family: 'Poppins', Arial, sans-serif;
    }
    .kpi-card {
        background: linear-gradient(90deg, #e0c3fc 0%, #8ec5fc 100%);
        border-radius: 18px;
        box-shadow: 0 2px 12px 0 rgba(0,0,0,0.07);
        padding: 1.2rem 1rem 1.2rem 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
        transition: box-shadow 0.3s;
        font-size: 1.1rem;
        color: #222;
        font-family: 'Poppins', Arial, sans-serif;
    }
    .kpi-card:hover { box-shadow: 0 4px 24px 0 rgba(0,0,0,0.13); }
    .kpi-value { font-size: 2.5rem; font-weight: bold; color: #1976d2; font-family: 'Poppins', Arial, sans-serif; }
    .kpi-label { font-size: 1.15rem; color: #555; font-family: 'Poppins', Arial, sans-serif; }
    .section-title { font-size: 1.7rem; font-weight: 600; margin-top: 1.5rem; margin-bottom: 0.5rem; color: #1976d2; font-family: 'Poppins', Arial, sans-serif; }
    .divider {
        height: 6px;
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 3px;
        margin: 2rem 0 2rem 0;
        box-shadow: 0 2px 8px 0 rgba(0,0,0,0.07);
    }
    .card-table {
        background: #fff;
        border-radius: 16px;
        box-shadow: 0 2px 12px 0 rgba(0,0,0,0.07);
        padding: 1rem;
        margin-bottom: 1.5rem;
        animation: fadeIn 0.7s;
    }
    .stButton>button {
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
        color: #222;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 2px 8px 0 rgba(0,0,0,0.07);
        transition: background 0.3s, box-shadow 0.3s;
        padding: 0.7rem 2.2rem;
        margin: 0.5rem 0;
        font-family: 'Poppins', Arial, sans-serif;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #fcb69f 0%, #ffecd2 100%);
        color: #1976d2;
        box-shadow: 0 4px 16px 0 rgba(0,0,0,0.13);
    }
    .stDataFrame thead tr th {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #1976d2 !important;
        font-family: 'Poppins', Arial, sans-serif !important;
    }
    .fade-in {
        animation: fadeIn 0.7s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .footer {
        background: linear-gradient(90deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 12px;
        box-shadow: 0 2px 8px 0 rgba(0,0,0,0.07);
        padding: 1rem 0;
        margin-top: 2rem;
        text-align: center;
        color: #1976d2;
        font-size: 1.1rem;
        font-weight: 600;
        font-family: 'Poppins', Arial, sans-serif;
    }
    .footer-small {
        color: #555;
        font-size: 0.95rem;
        font-weight: 400;
        font-family: 'Poppins', Arial, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="banner fade-in">Client Pulse Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Monitor, analyze, and grow your client relationships with RFM insights.</div>', unsafe_allow_html=True)
st.markdown("**Author:** Nisha Nayani  ")
st.markdown("**Project:** RFM-based Customer Segmentation for Business Insights")
st.markdown(
    """
    This dashboard analyzes customer behavior using RFM (Recency, Frequency, Monetary) analysis. It helps you identify high value, active, at risk, and inactive customers for better business decisions.
    """
)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- Load Data ---
@st.cache_data
def load_data():
    rfm = pd.read_csv("RFM_Table.csv")
    rfm_clustered = pd.read_csv("RFM_Clustered.csv")
    return rfm, rfm_clustered
rfm, rfm_clustered = load_data()

# --- Customer Category Assignment (Simple, Clear) ---
def qcut_with_dynamic_labels(series, q, label_order):
    quantiles, bins = pd.qcut(series, q, retbins=True, duplicates='drop')
    n_bins = len(bins) - 1
    if n_bins < 2:
        # Not enough unique values to bin, assign all to the first label
        return pd.Series([label_order[0]] * len(series), index=series.index)
    labels = label_order[:n_bins]
    try:
        return pd.qcut(series, q=n_bins, labels=labels, duplicates='drop')
    except ValueError:
        return pd.Series([label_order[0]] * len(series), index=series.index)

rfm_clustered['R_rank'] = qcut_with_dynamic_labels(rfm_clustered['Recency'], 4, [4,3,2,1])
rfm_clustered['F_rank'] = qcut_with_dynamic_labels(rfm_clustered['Frequency'], 4, [1,2,3,4])
rfm_clustered['M_rank'] = qcut_with_dynamic_labels(rfm_clustered['Monetary'], 4, [1,2,3,4])
def customer_category(row):
    if row['R_rank'] == 4 and row['F_rank'] == 4 and row['M_rank'] == 4:
        return 'High Value', 'Recent, frequent, and high spenders'
    elif row['R_rank'] >= 3 and row['F_rank'] >= 3:
        return 'Active', 'Recent and frequent, moderate spend'
    elif row['R_rank'] <= 2 and (row['F_rank'] >= 3 or row['M_rank'] >= 3):
        return 'At Risk', 'Used to spend, but not recent'
    else:
        return 'Inactive', 'Not recent, low spend/frequency'
rfm_clustered[['Category', 'Category_Desc']] = rfm_clustered.apply(lambda row: pd.Series(customer_category(row)), axis=1)

# --- Advanced Sidebar Filters ---
st.sidebar.header('Advanced Filters')
min_r, max_r = int(rfm_clustered['Recency'].min()), int(rfm_clustered['Recency'].max())
min_f, max_f = int(rfm_clustered['Frequency'].min()), int(rfm_clustered['Frequency'].max())
min_m, max_m = float(rfm_clustered['Monetary'].min()), float(rfm_clustered['Monetary'].max())
recency_range = st.sidebar.slider('Recency Range', min_r, max_r, (min_r, max_r))
frequency_range = st.sidebar.slider('Frequency Range', min_f, max_f, (min_f, max_f))
monetary_range = st.sidebar.slider('Monetary Range', min_m, max_m, (min_m, max_m))

# Optional: Dropdown for categorical column (e.g., Country)
categorical_cols = [col for col in rfm_clustered.columns if rfm_clustered[col].dtype == 'object' and col != 'CustomerID']
cat_filter = None
cat_value = None
if categorical_cols:
    cat_filter = st.sidebar.selectbox('Filter by', ['None'] + categorical_cols)
    if cat_filter != 'None':
        cat_options = sorted(rfm_clustered[cat_filter].dropna().unique())
        cat_value = st.sidebar.selectbox(f'Select {cat_filter}', ['All'] + cat_options)

# Apply filters to filtered_df
filtered_df = rfm_clustered[
    (rfm_clustered['Recency'] >= recency_range[0]) & (rfm_clustered['Recency'] <= recency_range[1]) &
    (rfm_clustered['Frequency'] >= frequency_range[0]) & (rfm_clustered['Frequency'] <= frequency_range[1]) &
    (rfm_clustered['Monetary'] >= monetary_range[0]) & (rfm_clustered['Monetary'] <= monetary_range[1])
]
if cat_filter and cat_filter != 'None' and cat_value and cat_value != 'All':
    filtered_df = filtered_df[filtered_df[cat_filter] == cat_value]

# --- Customer Lookup (with Personalized Recommendation) ---
st.markdown('<div class="section-title fade-in">Customer Lookup (Full Details)</div>', unsafe_allow_html=True)
st.caption("Enter a CustomerID to see every available detail for that customer. If multiple customers match, all will be shown. This lookup displays all columns from your data for full transparency.")
lookup_col1, lookup_col2 = st.columns([4,1])
with lookup_col1:
    lookup_id = st.text_input('Enter CustomerID to lookup:', '')
with lookup_col2:
    if st.button('Clear Search'):
        lookup_id = ''

if not lookup_id.strip():
    st.info("Type a CustomerID above to see all available information for that customer.")
    # Show a sample table
    st.markdown('<div class="card-table">', unsafe_allow_html=True)
    st.dataframe(filtered_df.head(5), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    matches = filtered_df[filtered_df['CustomerID'].astype(str).str.contains(lookup_id.strip())]
    if not matches.empty:
        st.markdown('<div class="card-table">', unsafe_allow_html=True)
        st.dataframe(matches, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Personalized recommendation based on RFM
        for _, row in matches.iterrows():
            rec, freq, mon = row['Recency'], row['Frequency'], row['Monetary']
            if rec <= filtered_df['Recency'].quantile(0.25) and freq >= filtered_df['Frequency'].quantile(0.75) and mon >= filtered_df['Monetary'].quantile(0.75):
                st.success('Recommendation: Reward this loyal, high-value customer with a special offer!')
            elif rec > filtered_df['Recency'].quantile(0.75):
                st.warning('Recommendation: Win back this inactive customer with a re-engagement campaign.')
            elif freq < filtered_df['Frequency'].quantile(0.25):
                st.info('Recommendation: Encourage this customer to purchase more frequently.')
            else:
                st.info('Recommendation: Keep this customer engaged with regular updates.')
    else:
        st.warning('No customer found with that ID.')

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- KPIs ---
kpi1, kpi2 = st.columns(2)
kpi1.markdown(f'<div class="kpi-card"><span style="font-size:2rem;">👥</span><div class="kpi-value">{filtered_df["CustomerID"].nunique():,}</div><div class="kpi-label">Total Customers</div></div>', unsafe_allow_html=True)
kpi2.markdown(f'<div class="kpi-card"><span style="font-size:2rem;">💰</span><div class="kpi-value">{filtered_df["Monetary"].mean():,.2f}</div><div class="kpi-label">Average Spend</div></div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- Customer Category Proportions Pie Chart ---
if 'Category' in rfm_clustered.columns and not filtered_df.empty:
    st.markdown('<div class="section-title fade-in">Customer Category Proportions</div>', unsafe_allow_html=True)
    import plotly.express as px
    pie_fig = px.pie(filtered_df, names='Category', title='Customer Category Proportions', color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(pie_fig, use_container_width=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- Top N Customers (Enhanced) ---
st.markdown('<div class="section-title fade-in">Top N Customers</div>', unsafe_allow_html=True)
st.caption("Explore your top customers by Recency (most recent), Frequency, or Monetary value. Use the tabs to switch views. Download each Top N list as CSV. Hover over bars for details.")
top_n = st.slider("Select N (Top Customers)", 1, 50, 10)
tabs = st.tabs(["Most Recent", "Most Frequent", "Top Monetary"])

# Most Recent
with tabs[0]:
    st.markdown('<div class="card-table">', unsafe_allow_html=True)
    st.caption("Most Recent Customers (Lowest Recency)")
    if not filtered_df.empty:
        top_recent = filtered_df.nsmallest(min(top_n, len(filtered_df)), 'Recency')[['CustomerID', 'Recency', 'Frequency', 'Monetary']]
        st.dataframe(top_recent, use_container_width=True)
        bar_fig = px.bar(top_recent[::-1], x='Recency', y='CustomerID', orientation='h', title="Top N Most Recent Customers", color='Recency', color_continuous_scale=px.colors.sequential.Blues)
        bar_fig.update_traces(marker_line_width=2)
        st.plotly_chart(bar_fig, use_container_width=True)
        csv = top_recent.to_csv(index=False).encode('utf-8')
        st.download_button("Download Top N Most Recent as CSV", data=csv, file_name="top_n_recent.csv", mime="text/csv")
    else:
        st.info("No customers to display.")
    st.markdown('</div>', unsafe_allow_html=True)

# Most Frequent
with tabs[1]:
    st.markdown('<div class="card-table">', unsafe_allow_html=True)
    st.caption("Most Frequent Customers")
    if not filtered_df.empty:
        top_freq = filtered_df.nlargest(min(top_n, len(filtered_df)), 'Frequency')[['CustomerID', 'Recency', 'Frequency', 'Monetary']]
        st.dataframe(top_freq, use_container_width=True)
        bar_fig = px.bar(top_freq[::-1], x='Frequency', y='CustomerID', orientation='h', title="Top N Most Frequent Customers", color='Frequency', color_continuous_scale=px.colors.sequential.Greens)
        bar_fig.update_traces(marker_line_width=2)
        st.plotly_chart(bar_fig, use_container_width=True)
        csv = top_freq.to_csv(index=False).encode('utf-8')
        st.download_button("Download Top N Most Frequent as CSV", data=csv, file_name="top_n_frequent.csv", mime="text/csv")
    else:
        st.info("No customers to display.")
    st.markdown('</div>', unsafe_allow_html=True)

# Top Monetary
with tabs[2]:
    st.markdown('<div class="card-table">', unsafe_allow_html=True)
    st.caption("Top Monetary Customers")
    if not filtered_df.empty:
        top_monetary = filtered_df.nlargest(min(top_n, len(filtered_df)), 'Monetary')[['CustomerID', 'Recency', 'Frequency', 'Monetary']]
        st.dataframe(top_monetary, use_container_width=True)
        bar_fig = px.bar(top_monetary[::-1], x='Monetary', y='CustomerID', orientation='h', title="Top N Monetary Customers", color='Monetary', color_continuous_scale=px.colors.sequential.Purples)
        bar_fig.update_traces(marker_line_width=2)
        st.plotly_chart(bar_fig, use_container_width=True)
        csv = top_monetary.to_csv(index=False).encode('utf-8')
        st.download_button("Download Top N Monetary as CSV", data=csv, file_name="top_n_monetary.csv", mime="text/csv")
    else:
        st.info("No customers to display.")
    st.markdown('</div>', unsafe_allow_html=True)

# Download all Top N as Excel
import xlsxwriter
import tempfile
import os
if not filtered_df.empty:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        with pd.ExcelWriter(tmp.name, engine='xlsxwriter') as writer:
            top_recent.to_excel(writer, index=False, sheet_name='Most Recent')
            top_freq.to_excel(writer, index=False, sheet_name='Most Frequent')
            top_monetary.to_excel(writer, index=False, sheet_name='Top Monetary')
        tmp.seek(0)
        st.download_button("Download All Top N as Excel", data=tmp.read(), file_name="top_n_customers.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    os.unlink(tmp.name)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- RFM Distributions (Interactive) ---
st.markdown('<div class="section-title fade-in">RFM Distributions</div>', unsafe_allow_html=True)
st.caption("Select an RFM variable to view its distribution. All charts are interactive: zoom, pan, hover, and select.")
rfm_var = st.selectbox("Choose RFM variable", ["Recency", "Frequency", "Monetary"])
hist_fig = px.histogram(filtered_df, x=rfm_var, nbins=20, title=f"{rfm_var} Distribution", color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(hist_fig, use_container_width=True)
# Download chart as PNG
try:
    png_bytes = hist_fig.to_image(format="png")
    st.download_button(f"Download {rfm_var} Histogram as PNG", data=png_bytes, file_name=f"{rfm_var.lower()}_histogram.png", mime="image/png")
except Exception as e:
    st.info("Install the 'kaleido' package to enable chart image export: pip install -U kaleido")
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --- Data Table & Export ---
st.markdown('<div class="section-title fade-in">Customer Data Table & Export</div>', unsafe_allow_html=True)
st.caption("Outliers in Recency, Frequency, and Monetary are highlighted. Download as CSV or Excel.")
outlier_flags = pd.DataFrame(index=filtered_df.index)
for col in ['Recency', 'Frequency', 'Monetary']:
    q_low = filtered_df[col].quantile(0.01)
    q_high = filtered_df[col].quantile(0.99)
    outlier_flags[col+'_outlier'] = (filtered_df[col] <= q_low) | (filtered_df[col] >= q_high)
filtered_reset = filtered_df.reset_index(drop=True)
outlier_flags_reset = outlier_flags.reset_index(drop=True)
if not filtered_reset.empty and all(col in filtered_reset.columns for col in ['Recency', 'Frequency', 'Monetary']):
    styled_table = filtered_reset.style
    if 'Recency' in filtered_reset.columns and 'Recency_outlier' in outlier_flags_reset.columns:
        styled_table = styled_table.apply(
            lambda x: [
                'background-color: #ffe0e0' if outlier_flags_reset['Recency_outlier'].iloc[i] else ''
                for i, _ in enumerate(x)
            ], subset=['Recency'])
    if 'Frequency' in filtered_reset.columns and 'Frequency_outlier' in outlier_flags_reset.columns:
        styled_table = styled_table.apply(
            lambda x: [
                'background-color: #e0ffe0' if outlier_flags_reset['Frequency_outlier'].iloc[i] else ''
                for i, _ in enumerate(x)
            ], subset=['Frequency'])
    if 'Monetary' in filtered_reset.columns and 'Monetary_outlier' in outlier_flags_reset.columns:
        styled_table = styled_table.apply(
            lambda x: [
                'background-color: #e0e0ff' if outlier_flags_reset['Monetary_outlier'].iloc[i] else ''
                for i, _ in enumerate(x)
            ], subset=['Monetary'])
    st.markdown('<div class="card-table">', unsafe_allow_html=True)
    st.dataframe(styled_table, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="card-table">', unsafe_allow_html=True)
    st.dataframe(filtered_reset, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# CSV download
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download as CSV", data=csv, file_name="customers.csv", mime="text/csv")

# Excel download
excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    filtered_df.to_excel(writer, index=False, sheet_name='Customers')
st.download_button("Download Filtered Data as Excel", data=excel_buffer.getvalue(), file_name="customers.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# --- Help/About Section ---
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('**How to use this dashboard:**')
st.info('''
- Use the Customer Lookup to see all available details for a customer.
- Review KPIs, Top N tables, and RFM distributions for insights.
- Outliers are highlighted in the data table.
- Download your data as CSV or Excel. Download charts as PNG.
- All charts are interactive. Hover for details.

**Author:** Nisha Nayani  
**Project:** RFM-based Customer Segmentation
**Contact:** nishanayani@gmail.com
''')

# --- Footer ---
st.markdown('<div class="footer">Dashboard by Nisha Nayani</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-small">Made with Streamlit & Plotly</div>', unsafe_allow_html=True)