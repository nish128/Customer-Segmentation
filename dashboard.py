import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .segment-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #ff7f0e;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and prepare the data"""
    try:
        # Load the main datasets
        rfm_data = pd.read_csv('RFM_Clustered.csv')
        cleaned_data = pd.read_csv('cleaned_data.csv')
        
        # Convert InvoiceDate to datetime
        cleaned_data['InvoiceDate'] = pd.to_datetime(cleaned_data['InvoiceDate'])
        
        # Calculate total amount
        cleaned_data['TotalAmount'] = cleaned_data['Quantity'] * cleaned_data['UnitPrice']
        
        return rfm_data, cleaned_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def create_cluster_mapping():
    """Define cluster characteristics based on RFM analysis"""
    return {
        0: {
            'name': 'At Risk',
            'description': 'Customers who haven\'t purchased recently but have good frequency/monetary scores',
            'color': '#ff4444'
        },
        1: {
            'name': 'Champions',
            'description': 'Best customers with high frequency, recent purchases, and high monetary value',
            'color': '#44ff44'
        },
        2: {
            'name': 'Loyal Customers',
            'description': 'Customers with good frequency and monetary value',
            'color': '#4444ff'
        },
        3: {
            'name': 'Potential Loyalists',
            'description': 'Recent customers with average frequency and monetary value',
            'color': '#ffaa44'
        }
    }

def main():
    # Header
    st.markdown('<div class="main-header">📊 Customer Segmentation Dashboard</div>', unsafe_allow_html=True)
    
    # Load data
    rfm_data, cleaned_data = load_data()
    
    if rfm_data is None or cleaned_data is None:
        st.error("Unable to load data. Please ensure the data files are present.")
        return
    
    # Sidebar
    st.sidebar.header("Dashboard Controls")
    
    # Cluster mapping
    cluster_mapping = create_cluster_mapping()
    
    # Add segment names to RFM data
    rfm_data['Segment'] = rfm_data['Cluster'].map(lambda x: cluster_mapping[x]['name'])
    rfm_data['Segment_Color'] = rfm_data['Cluster'].map(lambda x: cluster_mapping[x]['color'])
    
    # Sidebar filters
    selected_segments = st.sidebar.multiselect(
        "Select Customer Segments",
        options=list(cluster_mapping.values()),
        default=list(cluster_mapping.values()),
        format_func=lambda x: x['name']
    )
    
    selected_segment_names = [seg['name'] for seg in selected_segments]
    filtered_rfm = rfm_data[rfm_data['Segment'].isin(selected_segment_names)]
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Customers", f"{len(rfm_data):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_monetary = rfm_data['Monetary'].mean()
        st.metric("Avg Customer Value", f"${avg_monetary:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_frequency = rfm_data['Frequency'].mean()
        st.metric("Avg Purchase Frequency", f"{avg_frequency:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_recency = rfm_data['Recency'].mean()
        st.metric("Avg Days Since Last Purchase", f"{avg_recency:.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Segment Overview
    st.header("📈 Customer Segment Overview")
    
    # Segment distribution
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Pie chart for segment distribution
        segment_counts = rfm_data['Segment'].value_counts()
        colors = [cluster_mapping[cluster]['color'] for cluster in rfm_data['Cluster'].unique()]
        
        fig_pie = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="Customer Distribution by Segment",
            color_discrete_sequence=colors
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Segment characteristics table
        st.subheader("Segment Characteristics")
        segment_stats = rfm_data.groupby('Segment').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean',
            'CustomerID': 'count'
        }).round(2)
        segment_stats.columns = ['Avg Recency (days)', 'Avg Frequency', 'Avg Monetary ($)', 'Customer Count']
        st.dataframe(segment_stats, use_container_width=True)
    
    # Segment descriptions
    st.subheader("📋 Segment Descriptions")
    cols = st.columns(2)
    
    for i, (cluster_id, info) in enumerate(cluster_mapping.items()):
        with cols[i % 2]:
            customer_count = len(rfm_data[rfm_data['Cluster'] == cluster_id])
            percentage = (customer_count / len(rfm_data)) * 100
            
            st.markdown(f"""
            <div class="segment-card">
                <h4 style="color: {info['color']};">{info['name']}</h4>
                <p><strong>Count:</strong> {customer_count:,} customers ({percentage:.1f}%)</p>
                <p>{info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # RFM Analysis Visualizations
    st.header("🔍 RFM Analysis")
    
    tab1, tab2, tab3 = st.tabs(["RFM Scatter Plots", "RFM Distributions", "3D RFM Analysis"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Recency vs Monetary
            fig1 = px.scatter(
                filtered_rfm,
                x='Recency',
                y='Monetary',
                color='Segment',
                title="Recency vs Monetary Value",
                labels={'Recency': 'Days Since Last Purchase', 'Monetary': 'Total Spend ($)'},
                hover_data=['Frequency']
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Frequency vs Monetary
            fig2 = px.scatter(
                filtered_rfm,
                x='Frequency',
                y='Monetary',
                color='Segment',
                title="Frequency vs Monetary Value",
                labels={'Frequency': 'Purchase Frequency', 'Monetary': 'Total Spend ($)'},
                hover_data=['Recency']
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        # Box plots for RFM distributions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig3 = px.box(
                filtered_rfm,
                x='Segment',
                y='Recency',
                title="Recency Distribution by Segment",
                labels={'Recency': 'Days Since Last Purchase'}
            )
            fig3.update_xaxes(tickangle=45)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            fig4 = px.box(
                filtered_rfm,
                x='Segment',
                y='Frequency',
                title="Frequency Distribution by Segment",
                labels={'Frequency': 'Purchase Frequency'}
            )
            fig4.update_xaxes(tickangle=45)
            st.plotly_chart(fig4, use_container_width=True)
        
        with col3:
            fig5 = px.box(
                filtered_rfm,
                x='Segment',
                y='Monetary',
                title="Monetary Distribution by Segment",
                labels={'Monetary': 'Total Spend ($)'}
            )
            fig5.update_xaxes(tickangle=45)
            st.plotly_chart(fig5, use_container_width=True)
    
    with tab3:
        # 3D RFM visualization
        fig_3d = px.scatter_3d(
            filtered_rfm,
            x='Recency',
            y='Frequency',
            z='Monetary',
            color='Segment',
            title="3D RFM Analysis",
            labels={
                'Recency': 'Days Since Last Purchase',
                'Frequency': 'Purchase Frequency',
                'Monetary': 'Total Spend ($)'
            },
            hover_data=['CustomerID']
        )
        st.plotly_chart(fig_3d, use_container_width=True)
    
    st.markdown("---")
    
    # Business Insights
    st.header("💡 Business Insights & Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Findings")
        
        # Calculate insights
        champions = rfm_data[rfm_data['Segment'] == 'Champions']
        at_risk = rfm_data[rfm_data['Segment'] == 'At Risk']
        
        total_revenue = rfm_data['Monetary'].sum()
        champions_revenue = champions['Monetary'].sum()
        champions_percentage = (champions_revenue / total_revenue) * 100
        
        st.write(f"• **Champions** represent {len(champions)/len(rfm_data)*100:.1f}% of customers but generate {champions_percentage:.1f}% of total revenue")
        st.write(f"• **At Risk** customers: {len(at_risk)} customers need immediate attention")
        st.write(f"• Average customer lifetime value: **${rfm_data['Monetary'].mean():.2f}**")
        st.write(f"• Customer retention opportunity: **{len(at_risk) + len(rfm_data[rfm_data['Segment'] == 'Potential Loyalists'])}** customers")
    
    with col2:
        st.subheader("Recommended Actions")
        
        st.write("**Champions** 🏆")
        st.write("• Offer exclusive products and VIP treatment")
        st.write("• Use them as brand ambassadors")
        
        st.write("**At Risk** ⚠️")
        st.write("• Send personalized win-back campaigns")
        st.write("• Offer special discounts or incentives")
        
        st.write("**Loyal Customers** 💙")
        st.write("• Provide loyalty rewards and upselling")
        st.write("• Encourage referrals")
        
        st.write("**Potential Loyalists** 🌟")
        st.write("• Create targeted engagement campaigns")
        st.write("• Offer membership programs")
    
    # Customer Details
    st.markdown("---")
    st.header("👥 Customer Details")
    
    # Search and filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_customer = st.text_input("Search by Customer ID")
    
    with col2:
        sort_by = st.selectbox("Sort by", ['Monetary', 'Frequency', 'Recency', 'CustomerID'])
    
    with col3:
        sort_order = st.selectbox("Order", ['Descending', 'Ascending'])
    
    # Filter and sort data
    display_data = filtered_rfm.copy()
    
    if search_customer:
        display_data = display_data[display_data['CustomerID'].astype(str).str.contains(search_customer)]
    
    ascending = sort_order == 'Ascending'
    display_data = display_data.sort_values(sort_by, ascending=ascending)
    
    # Display customer table
    st.dataframe(
        display_data[['CustomerID', 'Segment', 'Recency', 'Frequency', 'Monetary', 'Cluster']],
        use_container_width=True,
        height=400
    )
    
    # Download option
    st.download_button(
        label="📥 Download Customer Data",
        data=display_data.to_csv(index=False),
        file_name=f"customer_segmentation_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()