import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Load data
df = pd.read_csv('RFM_Clustered.csv')

# Segment names
segment_names = {0: "Low Value", 1: "Champions", 2: "Loyal", 3: "At-Risk"}
df['Segment_Name'] = df['Cluster'].map(segment_names)

# Colors
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

# Initialize app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🎯 Customer Segmentation Dashboard", style={'textAlign': 'center'}),
    
    # Metrics
    html.Div([
        html.Div([html.H3(f"{len(df):,}"), html.P("Customers")], 
                style={'textAlign': 'center', 'margin': '20px'}),
        html.Div([html.H3(f"${df['Monetary'].sum():,.0f}"), html.P("Revenue")], 
                style={'textAlign': 'center', 'margin': '20px'}),
        html.Div([html.H3(f"${df['Monetary'].mean():.0f}"), html.P("Avg Value")], 
                style={'textAlign': 'center', 'margin': '20px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-around'}),
    
    # Charts
    html.Div([
        dcc.Graph(id='pie-chart'),
        dcc.Graph(id='bar-chart')
    ], style={'display': 'flex'}),
    
    # RFM Analysis
    html.H3("RFM Analysis"),
    html.Div([
        dcc.Dropdown(id='x-axis', options=[
            {'label': 'Recency', 'value': 'Recency'},
            {'label': 'Frequency', 'value': 'Frequency'},
            {'label': 'Monetary', 'value': 'Monetary'}
        ], value='Recency'),
        dcc.Dropdown(id='y-axis', options=[
            {'label': 'Recency', 'value': 'Recency'},
            {'label': 'Frequency', 'value': 'Frequency'},
            {'label': 'Monetary', 'value': 'Monetary'}
        ], value='Monetary'),
    ], style={'width': '30%'}),
    
    dcc.Graph(id='scatter-plot'),
    dcc.Graph(id='box-plots'),
    
    # Table
    html.Div(id='stats-table')
])

@app.callback(Output('pie-chart', 'figure'), Input('pie-chart', 'id'))
def update_pie(_):
    counts = df['Segment_Name'].value_counts()
    return px.pie(values=counts.values, names=counts.index, 
                  title="Customer Distribution", color_discrete_sequence=colors)

@app.callback(Output('bar-chart', 'figure'), Input('bar-chart', 'id'))
def update_bar(_):
    revenue = df.groupby('Segment_Name')['Monetary'].sum().reset_index()
    return px.bar(revenue, x='Segment_Name', y='Monetary', 
                  title="Revenue by Segment", color='Segment_Name',
                  color_discrete_sequence=colors)

@app.callback(Output('scatter-plot', 'figure'), 
              [Input('x-axis', 'value'), Input('y-axis', 'value')])
def update_scatter(x, y):
    return px.scatter(df, x=x, y=y, color='Segment_Name', size='Monetary',
                      title=f"{y} vs {x}", color_discrete_sequence=colors)

@app.callback(Output('box-plots', 'figure'), Input('box-plots', 'id'))
def update_box(_):
    fig = make_subplots(rows=1, cols=3, 
                       subplot_titles=['Recency', 'Frequency', 'Monetary'])
    
    for i, metric in enumerate(['Recency', 'Frequency', 'Monetary']):
        for j, (cluster, name) in enumerate(segment_names.items()):
            data = df[df['Cluster'] == cluster][metric]
            fig.add_trace(go.Box(y=data, name=name, marker_color=colors[j],
                               showlegend=(i==0)), row=1, col=i+1)
    
    fig.update_layout(title="RFM Distributions by Segment")
    return fig

@app.callback(Output('stats-table', 'children'), Input('stats-table', 'id'))
def update_table(_):
    stats = df.groupby('Segment_Name').agg({
        'CustomerID': 'count',
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean'
    }).round(1).reset_index()
    
    return dash_table.DataTable(
        data=stats.to_dict('records'),
        columns=[{"name": i, "id": i} for i in stats.columns],
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': '#3498db', 'color': 'white'}
    )

if __name__ == '__main__':
    app.run_server(debug=True)