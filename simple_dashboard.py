#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import pandas as pd
import json
from urllib.parse import parse_qs, urlparse

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Load RFM data
            try:
                rfm_data = pd.read_csv('RFM_Clustered.csv')
                total_customers = len(rfm_data)
                avg_monetary = rfm_data['Monetary'].mean()
                avg_frequency = rfm_data['Frequency'].mean()
                avg_recency = rfm_data['Recency'].mean()
                
                # Count segments
                segment_counts = rfm_data['Cluster'].value_counts().to_dict()
                segment_mapping = {
                    0: 'At Risk',
                    1: 'Champions', 
                    2: 'Loyal Customers',
                    3: 'Potential Loyalists'
                }
                
                html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Customer Segmentation Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #ffd700;
        }}
        .segments {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .segment-card {{
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 15px;
        }}
        .streamlit-link {{
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
            margin: 20px 10px;
            transition: transform 0.3s ease;
        }}
        .streamlit-link:hover {{
            transform: scale(1.05);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }}
        th {{
            background: rgba(255,255,255,0.2);
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Customer Segmentation Dashboard</h1>
            <p>RFM Analysis Results</p>
            
            <a href="http://localhost:8080" class="streamlit-link">🚀 Open Full Interactive Dashboard (Port 8080)</a>
            <a href="http://localhost:8501" class="streamlit-link">🚀 Try Port 8501</a>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{total_customers:,}</div>
                <div>Total Customers</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">${avg_monetary:,.2f}</div>
                <div>Avg Customer Value</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{avg_frequency:.1f}</div>
                <div>Avg Purchase Frequency</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{avg_recency:.0f}</div>
                <div>Avg Days Since Last Purchase</div>
            </div>
        </div>
        
        <h2>Customer Segments</h2>
        <div class="segments">
"""
                
                for cluster_id, name in segment_mapping.items():
                    count = segment_counts.get(cluster_id, 0)
                    percentage = (count / total_customers) * 100 if total_customers > 0 else 0
                    
                    descriptions = {
                        'Champions': 'Best customers with high frequency, recent purchases, and high monetary value',
                        'Loyal Customers': 'Customers with good frequency and monetary value',
                        'Potential Loyalists': 'Recent customers with average frequency and monetary value',
                        'At Risk': 'Customers who haven\'t purchased recently but have good frequency/monetary scores'
                    }
                    
                    html += f"""
            <div class="segment-card">
                <h3>{name}</h3>
                <p><strong>{count:,} customers ({percentage:.1f}%)</strong></p>
                <p>{descriptions.get(name, '')}</p>
            </div>
"""
                
                # Add sample data table
                html += f"""
        </div>
        
        <h2>Sample Customer Data</h2>
        <table>
            <tr>
                <th>Customer ID</th>
                <th>Segment</th>
                <th>Recency (days)</th>
                <th>Frequency</th>
                <th>Monetary ($)</th>
            </tr>
"""
                
                # Show first 10 customers
                for _, row in rfm_data.head(10).iterrows():
                    segment_name = segment_mapping.get(row['Cluster'], 'Unknown')
                    html += f"""
            <tr>
                <td>{row['CustomerID']}</td>
                <td>{segment_name}</td>
                <td>{row['Recency']:.0f}</td>
                <td>{row['Frequency']:.0f}</td>
                <td>${row['Monetary']:.2f}</td>
            </tr>
"""
                
                html += """
        </table>
        
        <div style="text-align: center; margin-top: 30px;">
            <p><strong>For full interactive analysis, charts, and 3D visualizations, use the Streamlit dashboard above!</strong></p>
        </div>
    </div>
</body>
</html>
"""
                
            except Exception as e:
                html = f"""
<!DOCTYPE html>
<html>
<head><title>Dashboard Error</title></head>
<body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
        <h1 style="color: #e74c3c;">⚠️ Dashboard Error</h1>
        <p>Could not load data: {str(e)}</p>
        <p>Please ensure RFM_Clustered.csv file exists.</p>
        <a href="http://localhost:8080" style="display: inline-block; background: #3498db; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Try Streamlit Dashboard</a>
    </div>
</body>
</html>
"""
            
            self.wfile.write(html.encode())
        else:
            super().do_GET()

PORT = 9000
with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
    print(f"🌐 Simple Dashboard Server running at http://localhost:{PORT}/")
    print("🚀 Full Dashboard available at http://localhost:8080/")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()