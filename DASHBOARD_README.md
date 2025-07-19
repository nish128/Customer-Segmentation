# Customer Segmentation Dashboard 📊

An interactive web dashboard built with Streamlit for visualizing and analyzing customer segmentation results based on RFM (Recency, Frequency, Monetary) analysis.

## Features

### 🎯 Key Metrics Overview
- Total customer count
- Average customer value
- Average purchase frequency  
- Average days since last purchase

### 📈 Interactive Visualizations
- **Customer segment distribution** (pie chart)
- **RFM scatter plots** (Recency vs Monetary, Frequency vs Monetary)
- **Distribution analysis** (box plots for each RFM metric)
- **3D RFM visualization** for comprehensive analysis

### 🔍 Customer Segmentation
Four distinct customer segments based on clustering analysis:
- **Champions** 🏆: Best customers with high frequency, recent purchases, and high monetary value
- **Loyal Customers** 💙: Customers with good frequency and monetary value
- **Potential Loyalists** 🌟: Recent customers with average frequency and monetary value
- **At Risk** ⚠️: Customers who haven't purchased recently but have good frequency/monetary scores

### 💡 Business Insights
- Automated insights generation
- Actionable recommendations for each segment
- Revenue contribution analysis
- Customer retention opportunities

### 🛠️ Interactive Features
- Segment filtering capabilities
- Customer search functionality
- Data sorting options
- CSV export functionality

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure data files are present:**
   - `RFM_Clustered.csv` - Contains customer RFM scores and cluster assignments
   - `cleaned_data.csv` - Contains original transaction data

3. **Run the dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

4. **Open your browser:**
   - The dashboard will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## Usage Guide

### Navigation
- Use the **sidebar** to filter customer segments
- Navigate between different analysis tabs
- Hover over charts for detailed information

### Key Sections

#### 📊 Main Dashboard
- Overview metrics at the top
- Customer segment distribution and characteristics

#### 🔍 RFM Analysis Tabs
1. **RFM Scatter Plots**: Explore relationships between RFM metrics
2. **RFM Distributions**: Compare segment characteristics using box plots
3. **3D RFM Analysis**: Interactive 3D visualization of all RFM dimensions

#### 💡 Business Insights
- Key findings about customer segments
- Actionable recommendations for marketing strategies

#### 👥 Customer Details
- Searchable customer database
- Sortable by any metric
- Export functionality for further analysis

### Interpreting the Segments

#### Champions 🏆
- **Characteristics**: High monetary value, frequent purchases, recent activity
- **Strategy**: VIP treatment, exclusive offers, brand ambassador programs

#### Loyal Customers 💙
- **Characteristics**: Good monetary value and frequency, may need activation
- **Strategy**: Loyalty programs, upselling, referral incentives

#### Potential Loyalists 🌟
- **Characteristics**: Recent customers with growth potential
- **Strategy**: Engagement campaigns, membership programs, nurturing

#### At Risk ⚠️
- **Characteristics**: Haven't purchased recently, need re-engagement
- **Strategy**: Win-back campaigns, special discounts, personalized offers

## Data Requirements

### Input Files
The dashboard expects the following CSV files in the same directory:

1. **RFM_Clustered.csv**
   - Columns: `CustomerID`, `Recency`, `Frequency`, `Monetary`, `Cluster`
   - Contains customer-level RFM metrics and cluster assignments

2. **cleaned_data.csv**
   - Columns: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`
   - Contains transaction-level data

### Data Format
- Dates should be in YYYY-MM-DD HH:MM:SS format
- Monetary values should be numeric
- Customer IDs should be consistent across files

## Customization

### Adding New Segments
To modify segment definitions, edit the `create_cluster_mapping()` function in `dashboard.py`:

```python
def create_cluster_mapping():
    return {
        0: {
            'name': 'Your Segment Name',
            'description': 'Your segment description',
            'color': '#your_color_code'
        },
        # Add more segments as needed
    }
```

### Styling
Customize the appearance by modifying the CSS in the `st.markdown()` section of the dashboard.

## Troubleshooting

### Common Issues

1. **FileNotFoundError**: Ensure CSV files are in the same directory as `dashboard.py`
2. **Import Errors**: Run `pip install -r requirements.txt`
3. **Port Issues**: If port 8501 is busy, Streamlit will suggest an alternative
4. **Memory Issues**: For large datasets, consider data sampling or optimization

### Performance Tips
- Filter data using sidebar controls for faster rendering
- Close unused browser tabs when working with large datasets
- Use the latest version of Streamlit for best performance

## Technical Details

### Architecture
- **Frontend**: Streamlit web framework
- **Visualization**: Plotly for interactive charts
- **Data Processing**: Pandas for data manipulation
- **Styling**: Custom CSS for enhanced UI

### Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library
- **numpy**: Numerical computing
- **matplotlib/seaborn**: Additional plotting capabilities

## Contributing

To enhance the dashboard:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Streamlit documentation
3. Create an issue in the repository

---

**Built with ❤️ using Streamlit and Plotly**