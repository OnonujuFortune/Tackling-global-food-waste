"""
Global Food Wastage — Plotly Dash App
--------------------------------------
Run locally with:  pip install dash pandas plotly
                    python dash_app.py
Then open the printed local URL (usually http://127.0.0.1:8050) in your browser.

This gives full independent dropdown filters for Country, Year, and Food Type
(the static Food_Waste_Dashboard.html only filters by Country, since combining
all three filters client-side in a single static file isn't practical — this
script is the "live" version the project brief asks for).
"""
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv('global_food_wastage_cleaned.csv')

countries = ['All'] + sorted(df['Country'].unique().tolist())
years = ['All'] + sorted(df['Year'].unique().tolist())
foods = ['All'] + sorted(df['Food_Category'].unique().tolist())

app = Dash(__name__)
app.title = "Global Food Wastage Dashboard"

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1200px', 'margin': '0 auto'}, children=[
    html.H1("🌍 Global Food Wastage — Interactive Dashboard", style={'color': '#E85D2F'}),
    html.P("Filter by country, year, and food category to explore waste trends, economic loss, and household vs industrial share."),
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}, children=[
        html.Div([html.Label("Country"), dcc.Dropdown(countries, 'All', id='country-filter')], style={'flex': 1}),
        html.Div([html.Label("Year"), dcc.Dropdown(years, 'All', id='year-filter')], style={'flex': 1}),
        html.Div([html.Label("Food Category"), dcc.Dropdown(foods, 'All', id='food-filter')], style={'flex': 1}),
    ]),
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'}, children=[
        dcc.Graph(id='trend-chart'),
        dcc.Graph(id='food-bar-chart'),
        dcc.Graph(id='loss-map'),
        dcc.Graph(id='pie-chart'),
    ])
])


def filter_df(country, year, food):
    d = df.copy()
    if country != 'All':
        d = d[d['Country'] == country]
    if year != 'All':
        d = d[d['Year'] == int(year)]
    if food != 'All':
        d = d[d['Food_Category'] == food]
    return d


@app.callback(
    Output('trend-chart', 'figure'),
    Output('food-bar-chart', 'figure'),
    Output('loss-map', 'figure'),
    Output('pie-chart', 'figure'),
    Input('country-filter', 'value'),
    Input('year-filter', 'value'),
    Input('food-filter', 'value'),
)
def update_charts(country, year, food):
    d = filter_df(country, year, food)

    trend = d.groupby('Year', as_index=False)['Total_Waste_Tons'].sum()
    fig_trend = px.line(trend, x='Year', y='Total_Waste_Tons', markers=True,
                         title='Total Waste Over Time', labels={'Total_Waste_Tons': 'Tons'})
    fig_trend.update_traces(line_color='#E85D2F')

    food_bar = d.groupby('Food_Category', as_index=False)['Total_Waste_Tons'].sum().sort_values('Total_Waste_Tons', ascending=False)
    fig_food = px.bar(food_bar, x='Food_Category', y='Total_Waste_Tons', title='Waste by Food Category',
                       color='Total_Waste_Tons', color_continuous_scale='Oranges')

    loss_country = d.groupby('Country', as_index=False)['Economic_Loss_Million_USD'].sum()
    fig_map = px.choropleth(loss_country, locations='Country', locationmode='country names',
                             color='Economic_Loss_Million_USD', color_continuous_scale='Reds',
                             title='Economic Loss by Country ($M)')

    hh = d['Household_Waste_Pct'].mean() if len(d) else 0
    ind = d['Industrial_Waste_Pct'].mean() if len(d) else 0
    fig_pie = px.pie(names=['Household', 'Industrial'], values=[hh, ind],
                      title='Household vs Industrial Waste Share',
                      color=['Household', 'Industrial'],
                      color_discrete_map={'Household': '#E85D2F', 'Industrial': '#2F5DE8'})

    return fig_trend, fig_food, fig_map, fig_pie


if __name__ == '__main__':
    app.run(debug=True)
