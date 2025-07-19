import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

# Load the data
df = pd.read_csv('RFM_Clustered.csv')

# Define segment names based on RFM characteristics
segment_names = {
    0: "Low Value Customers",
    1: "Champions", 
    2: "Loyal Customers",
    3: "At-Risk Customers"
}

# Add segment names to dataframe
df['Segment_Name'] = df['Cluster'].map(segment_names)

# Calculate segment statistics
segment_stats = df.groupby(['Cluster', 'Segment_Name']).agg({
    'Recency': ['mean', 'median'],
    'Frequency': ['mean', 'median'], 
    'Monetary': ['mean', 'median', 'sum'],
    'CustomerID': 'count'
}).round(2)

segment_stats.columns = ['_'.join(col).strip() for col in segment_stats.columns]
segment_stats = segment_stats.reset_index()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Customer Segmentation Dashboard"

# Define color palette for segments
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
color_map = {i: colors[i] for i in range(4)}

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🎯 Customer Segmentation Dashboard", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '10px'}),
        html.P("RFM Analysis & K-Means Clustering Results", 
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': '18px', 'marginBottom': '30px'})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px'}),
    
    # Key Metrics Row
    html.Div([
        html.Div([
            html.H3(f"{len(df):,}", style={'color': '#e74c3c', 'fontSize': '36px', 'margin': '0'}),
            html.P("Total Customers", style={'color': '#7f8c8d', 'fontSize': '14px'})
        ], className='metric-box', style={'textAlign': 'center', 'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '10px'}),
        
        html.Div([
            html.H3(f"${df['Monetary'].sum():,.0f}", style={'color': '#27ae60', 'fontSize': '36px', 'margin': '0'}),
            html.P("Total Revenue", style={'color': '#7f8c8d', 'fontSize': '14px'})
        ], className='metric-box', style={'textAlign': 'center', 'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '10px'}),
        
        html.Div([
            html.H3(f"${df['Monetary'].mean():.0f}", style={'color': '#3498db', 'fontSize': '36px', 'margin': '0'}),
            html.P("Avg. Customer Value", style={'color': '#7f8c8d', 'fontSize': '14px'})
        ], className='metric-box', style={'textAlign': 'center', 'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '10px'}),
        
        html.Div([
            html.H3(f"{df['Frequency'].mean():.1f}", style={'color': '#9b59b6', 'fontSize': '36px', 'margin': '0'}),
            html.P("Avg. Purchase Frequency", style={'color': '#7f8c8d', 'fontSize': '14px'})
        ], className='metric-box', style={'textAlign': 'center', 'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '10px'})
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px'}),
    
    # Segment Overview Row
    html.Div([
        html.H2("📊 Segment Overview", style={'color': '#2c3e50', 'marginBottom': '20px'}),
        
        html.Div([
            # Segment Distribution Pie Chart
            html.Div([
                dcc.Graph(id='segment-distribution')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            
            # Segment Revenue Distribution
            html.Div([
                dcc.Graph(id='segment-revenue')
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
        ])
    ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginBottom': '20px'}),
    
    # RFM Analysis Row
    html.Div([
        html.H2("🔍 RFM Analysis", style={'color': '#2c3e50', 'marginBottom': '20px'}),
        
        # RFM Controls
        html.Div([
            html.Div([
                html.Label("Select RFM Dimensions:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                dcc.Dropdown(
                    id='rfm-x-axis',
                    options=[
                        {'label': 'Recency (Days since last purchase)', 'value': 'Recency'},
                        {'label': 'Frequency (Number of purchases)', 'value': 'Frequency'},
                        {'label': 'Monetary (Total spend)', 'value': 'Monetary'}
                    ],
                    value='Recency',
                    style={'marginBottom': '15px'}
                ),
                dcc.Dropdown(
                    id='rfm-y-axis',
                    options=[
                        {'label': 'Recency (Days since last purchase)', 'value': 'Recency'},
                        {'label': 'Frequency (Number of purchases)', 'value': 'Frequency'},
                        {'label': 'Monetary (Total spend)', 'value': 'Monetary'}
                    ],
                    value='Monetary',
                    style={'marginBottom': '15px'}
                )
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),
            
            # RFM Scatter Plot
            html.Div([
                dcc.Graph(id='rfm-scatter')
            ], style={'width': '70%', 'display': 'inline-block', 'padding': '10px'})
        ])
    ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginBottom': '20px'}),
    
    # Detailed Analysis Row
    html.Div([
        html.H2("📈 Segment Deep Dive", style={'color': '#2c3e50', 'marginBottom': '20px'}),
        
        html.Div([
            # RFM Box Plots
            html.Div([
                dcc.Graph(id='rfm-boxplots')
            ], style={'width': '60%', 'display': 'inline-block', 'padding': '10px'}),
            
            # Segment Comparison Table
            html.Div([
                html.H4("Segment Characteristics", style={'textAlign': 'center', 'marginBottom': '15px'}),
                html.Div(id='segment-table')
            ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'})
        ])
    ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginBottom': '20px'}),
    
    # Business Insights
    html.Div([
        html.H2("💡 Business Insights & Recommendations", style={'color': '#2c3e50', 'marginBottom': '20px'}),
        
        html.Div([
            html.Div([
                html.H4("🏆 Champions (Cluster 1)", style={'color': colors[1]}),
                html.P("• Highest value customers with exceptional spending"),
                html.P("• Very frequent purchasers with recent activity"),
                html.P("• Strategy: VIP treatment, exclusive offers, loyalty rewards")
            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'margin': '10px', 'borderLeft': f'4px solid {colors[1]}'}),
            
            html.Div([
                html.H4("💙 Loyal Customers (Cluster 2)", style={'color': colors[2]}),
                html.P("• Regular customers with good frequency and moderate spend"),
                html.P("• Recent purchasers showing consistent behavior"),
                html.P("• Strategy: Upselling, cross-selling, engagement campaigns")
            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'margin': '10px', 'borderLeft': f'4px solid {colors[2]}'}),
            
            html.Div([
                html.H4("😴 Low Value Customers (Cluster 0)", style={'color': colors[0]}),
                html.P("• Lower spending with moderate recency"),
                html.P("• Infrequent purchasers needing activation"),
                html.P("• Strategy: Discount offers, product recommendations, onboarding")
            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'margin': '10px', 'borderLeft': f'4px solid {colors[0]}'}),
            
            html.Div([
                html.H4("⚠️ At-Risk Customers (Cluster 3)", style={'color': colors[3]}),
                html.P("• Haven't purchased recently (high recency)"),
                html.P("• Low frequency and spending - risk of churn"),
                html.P("• Strategy: Win-back campaigns, special discounts, surveys")
            ], style={'backgroundColor': '#f8f9fa', 'padding': '15px', 'borderRadius': '8px', 'margin': '10px', 'borderLeft': f'4px solid {colors[3]}'})
        ])
    ], style={'backgroundColor': '#fff', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'marginBottom': '20px'}),
    
    # Footer
    html.Div([
        html.P("Customer Segmentation Dashboard | RFM Analysis & K-Means Clustering", 
               style={'textAlign': 'center', 'color': '#7f8c8d', 'margin': '0'})
    ], style={'backgroundColor': '#ecf0f1', 'padding': '15px', 'borderRadius': '10px', 'marginTop': '20px'})
])

# Callback for segment distribution pie chart
@app.callback(
    Output('segment-distribution', 'figure'),
    Input('segment-distribution', 'id')
)
def update_segment_distribution(_):
    segment_counts = df['Segment_Name'].value_counts()
    
    fig = px.pie(
        values=segment_counts.values,
        names=segment_counts.index,
        title="Customer Distribution by Segment",
        color_discrete_sequence=colors,
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        title_x=0.5,
        font=dict(size=12),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    
    return fig

# Callback for segment revenue distribution
@app.callback(
    Output('segment-revenue', 'figure'),
    Input('segment-revenue', 'id')
)
def update_segment_revenue(_):
    segment_revenue = df.groupby('Segment_Name')['Monetary'].sum().reset_index()
    
    fig = px.bar(
        segment_revenue,
        x='Segment_Name',
        y='Monetary',
        title="Total Revenue by Segment",
        color='Segment_Name',
        color_discrete_sequence=colors
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
    )
    
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Customer Segment",
        yaxis_title="Total Revenue ($)",
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    # Add value labels on bars
    for i, row in segment_revenue.iterrows():
        fig.add_annotation(
            x=row['Segment_Name'],
            y=row['Monetary'],
            text=f"${row['Monetary']:,.0f}",
            showarrow=False,
            yshift=10
        )
    
    return fig

# Callback for RFM scatter plot
@app.callback(
    Output('rfm-scatter', 'figure'),
    [Input('rfm-x-axis', 'value'),
     Input('rfm-y-axis', 'value')]
)
def update_rfm_scatter(x_axis, y_axis):
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        color='Segment_Name',
        size='Monetary',
        hover_data=['CustomerID', 'Recency', 'Frequency', 'Monetary'],
        title=f"{y_axis} vs {x_axis} by Customer Segment",
        color_discrete_sequence=colors,
        size_max=20
    )
    
    fig.update_traces(
        hovertemplate='<b>%{customdata[0]}</b><br>' +
                     f'{x_axis}: %{{x}}<br>' +
                     f'{y_axis}: %{{y}}<br>' +
                     'Recency: %{customdata[1]} days<br>' +
                     'Frequency: %{customdata[2]} purchases<br>' +
                     'Monetary: $%{customdata[3]:,.0f}<extra></extra>'
    )
    
    fig.update_layout(
        title_x=0.5,
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        legend_title="Customer Segment"
    )
    
    return fig

# Callback for RFM box plots
@app.callback(
    Output('rfm-boxplots', 'figure'),
    Input('rfm-boxplots', 'id')
)
def update_rfm_boxplots(_):
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Recency Distribution', 'Frequency Distribution', 'Monetary Distribution'),
        horizontal_spacing=0.1
    )
    
    # Recency boxplot
    for i, (cluster, name) in enumerate(segment_names.items()):
        cluster_data = df[df['Cluster'] == cluster]
        fig.add_trace(
            go.Box(
                y=cluster_data['Recency'],
                name=name,
                marker_color=colors[i],
                showlegend=False
            ),
            row=1, col=1
        )
    
    # Frequency boxplot
    for i, (cluster, name) in enumerate(segment_names.items()):
        cluster_data = df[df['Cluster'] == cluster]
        fig.add_trace(
            go.Box(
                y=cluster_data['Frequency'],
                name=name,
                marker_color=colors[i],
                showlegend=False
            ),
            row=1, col=2
        )
    
    # Monetary boxplot
    for i, (cluster, name) in enumerate(segment_names.items()):
        cluster_data = df[df['Cluster'] == cluster]
        fig.add_trace(
            go.Box(
                y=cluster_data['Monetary'],
                name=name,
                marker_color=colors[i],
                showlegend=True if i == 0 else False
            ),
            row=1, col=3
        )
    
    fig.update_layout(
        title_text="RFM Metrics Distribution by Segment",
        title_x=0.5,
        height=400
    )
    
    fig.update_yaxes(title_text="Days", row=1, col=1)
    fig.update_yaxes(title_text="Count", row=1, col=2)
    fig.update_yaxes(title_text="Amount ($)", row=1, col=3)
    
    return fig

# Callback for segment comparison table
@app.callback(
    Output('segment-table', 'children'),
    Input('segment-table', 'id')
)
def update_segment_table(_):
    # Calculate segment statistics
    stats = df.groupby('Segment_Name').agg({
        'CustomerID': 'count',
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': ['mean', 'sum']
    }).round(1)
    
    stats.columns = ['Count', 'Avg Recency', 'Avg Frequency', 'Avg Monetary', 'Total Revenue']
    stats = stats.reset_index()
    
    # Format monetary values
    stats['Avg Monetary'] = stats['Avg Monetary'].apply(lambda x: f"${x:,.0f}")
    stats['Total Revenue'] = stats['Total Revenue'].apply(lambda x: f"${x:,.0f}")
    
    table = dash_table.DataTable(
        data=stats.to_dict('records'),
        columns=[{"name": i, "id": i} for i in stats.columns],
        style_cell={
            'textAlign': 'center',
            'fontFamily': 'Arial',
            'fontSize': '12px',
            'padding': '8px'
        },
        style_header={
            'backgroundColor': '#3498db',
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 0},
                'backgroundColor': '#ffebee'
            },
            {
                'if': {'row_index': 1},
                'backgroundColor': '#e8f5e8'
            },
            {
                'if': {'row_index': 2},
                'backgroundColor': '#e3f2fd'
            },
            {
                'if': {'row_index': 3},
                'backgroundColor': '#fff3e0'
            }
        ]
    )
    
    return table

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)