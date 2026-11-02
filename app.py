"""Interactive Canadian workforce analysis dashboard.
Run with: python app.py
"""

import dash
from dash import dcc, html, Input, Output, callback, dash_table
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Loading and cleaning data
essential_services = pd.read_csv("data/essential_services.csv")
engineering = pd.read_csv("data/data_engineering.csv")
gender_employment = pd.read_csv("data/data_gender_employment.csv")

def clean_numeric(value):
    if isinstance(value, str):
        
        return float(value.replace(',', '').replace('"', '').strip())
    return float(value)


regions = [col for col in essential_services.columns if col not in ['Geography', 'Canada']]
for region in regions:
    essential_services[region] = essential_services[region].apply(clean_numeric)
    engineering[region] = engineering[region].apply(clean_numeric)

for col in gender_employment.columns[2:]:  # Skip 'Geography' and 'Gender' columns
    gender_employment[col] = gender_employment[col].apply(clean_numeric)

# NOC code mapping for gender employment
NOC_MAPPING = {
    '0': '0 Legislative and senior management occupations',
    '1': '1 Business, finance and administration occupations',
    '2': '2 Natural and applied sciences and related occupations',
    '3': '3 Health occupations',
    '4': '4 Occupations in education, law and social, community and government services',
    '5': '5 Occupations in art, culture, recreation and sport',
    '6': '6 Sales and service occupations',
    '7': '7 Trades, transport and equipment operators and related occupations',
    '8': '8 Natural resources, agriculture and related production occupations',
    '9': '9 Occupations in manufacturing and utilities'
}


# Population data
population_data = {
    'Province': regions,
    'Population': [520000, 160000, 980000, 780000, 8600000, 14700000, 
                   1380000, 1180000, 4400000, 5100000, 42000, 45000, 39000]
}
df_population = pd.DataFrame(population_data)





app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Canadian Workforce Analysis Dashboard", style={'textAlign': 'center', 'color': 'white'}),
    
    # ques1. Essential Services Distribution
    html.Div([
        html.H2("1. Essential Services Distribution visualization", style={'color': 'pink'}),
        html.Div([
            dcc.Dropdown(
                id='service-selector',
                options=[{'label': s, 'value': s} for s in ['Nurses', 'Police', 'Firefighters']],
                value='Nurses',
                style={'width': '50%', 'margin': '10px','color':'green'}
            ),
            dcc.RadioItems(
                id='normalization-toggle',
                options=[
                    {'label': ' Raw Counts', 'value': 'raw'},
                    {'label': ' Per 100k Population', 'value': 'per_capita'}
                ],
                value='raw',
                inline=True,
                style={'margin': '10px','color':'purple'}
            ),
        ], style={'display': 'flex', 'alignItems': 'center'}),
        
        dcc.Graph(id='services-chart'),
       
    ], style={'border': '1px solid #ddd', 'padding': '15px', 'margin': '10px'}),
    
    # ques2. Gender Employment
    html.Div([
        html.H2("2. Gender Employment by NOC Category", style={'color': '#9b59b6'}),
        html.Div([
            dcc.Dropdown(
                id='province-selector',
                options=[{'label': r, 'value': r} for r in regions],
                value='Ontario',
                style={'width': '50%', 'margin': '10px'}
            ),
            dcc.Dropdown(
                id='noc-selector',
                options=[{'label': f"{k}: {v}", 'value': k} for k,v in NOC_MAPPING.items()],
                value='2',
                style={'width': '50%', 'margin': '10px'}
            )
        ], style={'display': 'flex'}),
        dcc.Graph(id='gender-pie'),
        html.Div(id='gender-gap-indicator')
    ], style={'border': '1px solid #ddd', 'padding': '15px', 'margin': '10px'}),
    
    # ques 3. Electronic Vehicle Factory capability
    html.Div([
        html.H2("3. EV Factory Suitability Analysis Visualization", style={'color': 'red'}),
        html.Div([
            dcc.Dropdown(
                id='discipline-selector',
                options=[
                    {'label': 'All Engineering', 'value': 'all'},
                    {'label': 'Computer Engineering', 'value': 'Computer engineering'},
                    {'label': 'Electrical Engineering', 'value': 'Electrical, electronics and communications engineering'},
                    {'label': 'Mechanical Engineering', 'value': 'Mechanical engineering'}
                ],
                value='all',
                style={'width': '50%', 'margin': '10px'}
            ),
            dcc.Slider(
                id='threshold-slider',
                min=0,
                max=100000,
                step=5000,
                value=50000,
                marks={i: f'{i//1000}k' for i in range(0, 100001, 20000)},
                tooltip={'placement': 'bottom'}
            )
        ], style={'margin': '20px 10px'}),
        html.Div(id='threshold-display'),
        dcc.Graph(id='engineering-bars'),
        html.Div(id='ev-recommendation', style={
            'padding': '15px',
            'backgroundColor': '#f8f9fa',
            'borderRadius': '5px',
            'marginTop': '15px'
        })
    ], style={'border': '1px solid #ddd', 'padding': '15px', 'margin': '10px'}),
    
    # question 4. Custom Visualization
    html.Div([
        html.H2("4. Engineering Talent Heatmap", style={'color': '#27ae60'}),
        dcc.RadioItems(
            id='heatmap-scale',
            options=[
                {'label': ' Absolute Numbers', 'value': 'absolute'},
                {'label': ' Per Capita', 'value': 'per_capita'}
            ],
            value='absolute',
            inline=True,
            style={'margin': '10px', 'color':'purple'}
        ),
        dcc.Graph(id='engineering-heatmap')
    ], style={'border': '1px solid #ddd', 'padding': '15px', 'margin': '10px'})
], style={'fontFamily': 'Arial, sans-serif'})

# 1. Essential Services Callback
@app.callback(
    Output('services-chart', 'figure'),
    
    [Input('service-selector', 'value'),
     Input('normalization-toggle', 'value')]
)
def update_services(service, norm_type):
    
    row = essential_services[essential_services['Geography'] == service][regions].values.flatten()
    
    # Normalize 
    if norm_type == 'per_capita':
        data = [{'Region': r, 'Count': row[i]/df_population[df_population['Province']==r]['Population'].values[0]*100000} 
               for i,r in enumerate(regions)]
        title_y = "Count per 100k"
    else:
        data = [{'Region': r, 'Count': row[i]} for i,r in enumerate(regions)]
        title_y = "Count"
    

    fig = px.bar(
        pd.DataFrame(data),
        x='Region',
        y='Count',
        title=f"{service} Distribution ({'Per 100k' if norm_type=='per_capita' else 'Raw Counts'})",
        text='Count'
    )
    fig.update_traces(texttemplate='%{text:,.0f}')
    fig.update_layout(yaxis_title=title_y)

    
    return fig

@app.callback(
    [Output('gender-pie', 'figure'),
     Output('gender-gap-indicator', 'children')],
    [Input('province-selector', 'value'),
     Input('noc-selector', 'value')]
)
def update_gender(province, noc_code):
    column_name = NOC_MAPPING[noc_code]
    
    men = gender_employment[
        (gender_employment["Geography"] == province) & 
        (gender_employment["Gender"] == "Men")
    ][column_name].values[0]
    
    women = gender_employment[
        (gender_employment["Geography"] == province) & 
        (gender_employment["Gender"] == "Women")
    ][column_name].values[0]
    
    ratio = women/men if men != 0 else 0
    indicator_of_gap = "Male-dominated" if ratio < 0.8 else " equal" if ratio < 1.2 else " Female-dominated"
    
    fig = px.pie(
        names=['Men', 'Women'],
        values=[men, women],
        title=f"NOC {noc_code}: {column_name.split(' ', 1)[1]} in {province}",
        color=['Men', 'Women'],
        color_discrete_map={'Men': 'red', 'Women': 'orange'},
        hole=0.4
    )
    fig.update_traces(
        textinfo='percent+value',
        texttemplate='%{label}<br>%{value:,} (%{percent})'
    )
    
    return fig, html.Div([
        html.H4(f"Gender Ratio: {ratio:.2f}",style={'color':'white'}),
        html.P(indicator_of_gap, style={'fontSize': '20px','color':'white'})
    ])
# Q3. EV Factory Callback
@app.callback(
    [Output('engineering-bars', 'figure'),
     Output('threshold-display', 'children'),
     Output('ev-recommendation', 'children')],
    [Input('discipline-selector', 'value'),
     Input('threshold-slider', 'value')]
)
def update_engineering(discipline, threshold):
    if discipline == 'all':
        df = engineering[engineering['Engineering Discipline'].isin([
            'Computer engineering',
            'Electrical, electronics and communications engineering',
            'Mechanical engineering'
        ])]
        title = " Engineering Disciplines(ALL INCLUSIVE)"
    else:
        df = engineering[engineering['Engineering Discipline'] == discipline]
        title = discipline
    
    melted = df.melt(id_vars=['Engineering Discipline'], 
                    var_name='Province', 
                    value_name='Count')
    
    if discipline == 'all':
        melted = melted.groupby('Province')['Count'].sum().reset_index()
    
    melted['Above Threshold'] = melted['Count'] >= threshold
    suitable = melted[melted['Above Threshold']]['Province'].tolist()
    
    fig = px.bar(
        melted,
        x='Province',
        y='Count',
        color='Above Threshold',
        title=f"{title} Workforce by Province",
        color_discrete_map={True: '#27ae60', False: '#e74c3c'},
        text='Count'
    )
    fig.update_traces(texttemplate='%{text:,.0f}')
    
    suggestion = html.Div([
        html.H4("Locations Suggested for setting up EV Factories :"),
        html.Ul([html.Li(p) for p in suitable] if suitable else [html.Li("No provinces reach the threshold ")])
    ])
    
    return fig, html.H4(f"Threshold: {threshold:,} engineers"), suggestion

# 4. Heatmap Callback
@app.callback(
    Output('engineering-heatmap', 'figure'),
    [Input('heatmap-scale', 'value')]
)
def update_heatmap(scale_type):
    if scale_type == 'absolute':
        data = engineering.set_index('Engineering Discipline')[regions]
        title = "Engineering Talent (Absolute Counts)"
    else:
        data = engineering.copy()
        for region in regions:
            pop = df_population[df_population['Province']==region]['Population'].values[0]
            data[region] = data[region]/pop*100000
        data = data.set_index('Engineering Discipline')[regions]
        title = "Engineering Talent per 100k Population"
    
    fig = px.imshow(
        data,
        labels=dict(x="Province", y="Discipline", color="Count"),
        title=title,
        color_continuous_scale='Viridis',
        aspect="auto"
    )
    fig.update_layout(height=600)
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8050)
