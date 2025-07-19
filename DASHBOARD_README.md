# 🎯 Customer Segmentation Dashboard

An interactive web dashboard for analyzing customer segments using RFM (Recency, Frequency, Monetary) analysis and K-Means clustering.

## 📋 Overview

This dashboard provides comprehensive insights into customer behavior patterns by segmenting customers into four distinct groups:

- **🏆 Champions (Cluster 1)**: High-value customers with exceptional spending and frequent purchases
- **💙 Loyal Customers (Cluster 2)**: Regular customers with good frequency and moderate spend
- **😴 Low Value Customers (Cluster 0)**: Lower spending customers needing activation
- **⚠️ At-Risk Customers (Cluster 3)**: Customers at risk of churning with low recent activity

## 🚀 Features

### 📊 Key Metrics
- Total customer count and revenue overview
- Average customer value and purchase frequency
- Real-time calculations from your data

### 📈 Interactive Visualizations
1. **Segment Distribution**: Pie chart showing customer distribution across segments
2. **Revenue Analysis**: Bar chart displaying total revenue by segment
3. **RFM Scatter Plot**: Interactive scatter plot with customizable X/Y axes
4. **Box Plot Analysis**: Distribution analysis of RFM metrics by segment
5. **Segment Comparison Table**: Detailed statistics for each customer segment

### 💡 Business Insights
- Actionable recommendations for each customer segment
- Marketing strategy suggestions based on RFM characteristics
- Customer retention and growth strategies

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone or download the project files**
   ```bash
   # Ensure you have these files:
   # - customer_segmentation_dashboard.py
   # - RFM_Clustered.csv
   # - requirements.txt
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   python customer_segmentation_dashboard.py
   ```

4. **Access the dashboard**
   - Open your web browser
   - Navigate to: `http://localhost:8050`
   - The dashboard will load automatically

## 📊 Data Requirements

The dashboard expects a CSV file named `RFM_Clustered.csv` with the following columns:
- `CustomerID`: Unique customer identifier
- `Recency`: Days since last purchase
- `Frequency`: Number of purchases
- `Monetary`: Total customer spend
- `Cluster`: Cluster assignment (0-3)

## 🎮 How to Use

### Navigation
The dashboard is organized into several sections:

1. **Header**: Overview and key metrics
2. **Segment Overview**: Distribution and revenue charts
3. **RFM Analysis**: Interactive scatter plot with customizable axes
4. **Segment Deep Dive**: Box plots and comparison table
5. **Business Insights**: Actionable recommendations

### Interactive Features

#### RFM Scatter Plot
- **X-Axis Dropdown**: Choose between Recency, Frequency, or Monetary
- **Y-Axis Dropdown**: Choose between Recency, Frequency, or Monetary
- **Hover Information**: Detailed customer data on mouse hover
- **Zoom & Pan**: Interactive plot navigation

#### Segment Analysis
- **Color-coded segments**: Each segment has a unique color
- **Hover tooltips**: Additional information on chart elements
- **Responsive design**: Works on desktop and tablet devices

## 📈 Understanding the Segments

### 🏆 Champions (Cluster 1)
- **Characteristics**: Highest spenders, frequent buyers, recent activity
- **Strategy**: VIP treatment, exclusive offers, loyalty programs
- **Revenue Impact**: Highest per-customer value

### 💙 Loyal Customers (Cluster 2)
- **Characteristics**: Consistent buyers with good frequency
- **Strategy**: Upselling, cross-selling, engagement campaigns
- **Revenue Impact**: Steady revenue contributors

### 😴 Low Value Customers (Cluster 0)
- **Characteristics**: Lower spending, infrequent purchases
- **Strategy**: Activation campaigns, special offers, product recommendations
- **Revenue Impact**: Growth potential with proper nurturing

### ⚠️ At-Risk Customers (Cluster 3)
- **Characteristics**: High recency, low frequency and spend
- **Strategy**: Win-back campaigns, surveys, special discounts
- **Revenue Impact**: Churn prevention priority

## 🔧 Customization

### Adding New Metrics
To add new metrics to the dashboard:

1. Calculate the metric in the data loading section
2. Add it to the layout in the appropriate section
3. Create or modify callbacks for interactivity

### Changing Colors
Modify the `colors` list in the script:
```python
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
```

### Adjusting Segment Names
Update the `segment_names` dictionary:
```python
segment_names = {
    0: "Your Custom Name",
    1: "Another Name",
    # ... etc
}
```

## 📝 Technical Details

### Built With
- **Dash**: Web application framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations

### Performance
- Optimized for datasets up to 10,000 customers
- Real-time calculations and updates
- Responsive design for various screen sizes

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" error**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Dashboard won't load**
   - Check that port 8050 is available
   - Ensure RFM_Clustered.csv is in the same directory

3. **Data format errors**
   - Verify CSV column names match expected format
   - Check for missing values in required columns

### Getting Help
- Check the terminal/console for error messages
- Ensure all dependencies are installed
- Verify data file format and location

## 📊 Example Use Cases

1. **Marketing Campaign Planning**
   - Identify high-value customers for premium campaigns
   - Target at-risk customers with retention offers

2. **Customer Lifetime Value Analysis**
   - Compare segment profitability
   - Forecast revenue by segment

3. **Business Strategy Development**
   - Understand customer behavior patterns
   - Optimize resource allocation across segments

## 🔄 Future Enhancements

Potential improvements to consider:
- Real-time data connectivity
- Additional clustering algorithms
- Predictive analytics features
- Export functionality for reports
- Mobile-responsive design improvements

---

**Happy Analyzing! 📈**

For questions or support, refer to the documentation or check the code comments for detailed explanations.