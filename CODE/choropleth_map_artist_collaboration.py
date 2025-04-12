import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

# Load the dataset
file_path = "assets/artist_collaboration_predictions_by_market.csv"
df = pd.read_csv(file_path)

# Map country codes to full names
country_mapping = {
    'predicted_revenue_us': 'United States',
    'predicted_revenue_jp': 'Japan',
    'predicted_revenue_fr': 'France',
    'predicted_revenue_gb': 'Great Britain',
    'predicted_revenue_ca': 'Canada',
    'predicted_revenue_br': 'Brazil',
    'predicted_revenue_de': 'Denmark',
    'predicted_revenue_au': 'Australia'
}


# Melt the data for visualization
market_cols = list(country_mapping.keys())
melted_df = df.melt(id_vars=['artist_1_name', 'artist_2_name'], value_vars=market_cols, 
                     var_name='market', value_name='revenue')
melted_df['country'] = melted_df['market'].map(country_mapping)

# Calculate total revenue for each artist
total_revenue_artist_1 = melted_df.groupby('artist_1_name')['revenue'].sum()
total_revenue_artist_2 = melted_df.groupby('artist_2_name')['revenue'].sum()
total_revenue = total_revenue_artist_1.add(total_revenue_artist_2, fill_value=0)

# Sort artists by total revenue
sorted_artists = total_revenue.sort_values(ascending=False).index

# Create dropdown options with artist names only
artist_options = [{'label': artist, 'value': artist} for artist in sorted_artists]

# Initialize Dash app
app = dash.Dash(__name__)

# Layout with the map, total revenue tracker, sidebar, and filter
app.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#F5F5F5',
    'padding': '40px'
}, children=[

    # Title with music icon
    html.Div(style={
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'marginBottom': '20px'
    }, children=[
        html.Img(src='/assets/music_icon.png', 
                 style={'width': '60px', 'height': '60px', 'marginRight': '15px'}),
        html.H1("Artist Collaboration Earnings by Market",
                style={'color': '#003057', 'fontSize': '36px', 'fontWeight': 'bold',
                       'textShadow': '1px 1px 3px #ccc'})
    ]),

    # Total Revenue Tracker
    html.Div(id='total-revenue-tracker', 
             style={
                 'textAlign': 'center',
                 'fontSize': '28px',
                 'color': '#204060',
                 'backgroundColor': '#FFFFFF',
                 'border': '1px solid #ccc',
                 'borderRadius': '8px',
                 'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)',
                 'padding': '20px',
                 'marginBottom': '40px'
             }),

    # Container for map and sidebar
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between'}, children=[

        # Map and Filter (left side)
        html.Div(style={'flex': '2', 'marginRight': '20px'}, children=[

            # Choropleth Map
            dcc.Graph(id='choropleth-map', 
                      style={'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)'}),

            # Filter below the map and aligned to the left
            html.Div([
                html.Label("Select Artist:", style={'fontSize': '20px', 'color': '#333'}),
                dcc.Dropdown(
                    id='primary-artist-dropdown',
                    options=artist_options,
                    value=sorted_artists[0],  # Default to the top artist
                    multi=False,
                    style={'width': '90%', 'fontSize': '18px', 'marginTop': '20px'}
                ),
            ], style={'width': '80%', 'margin': '30px auto'})
        ]),

        # Sidebar (right side)
        html.Div(style={
            'flex': '1',
            'backgroundColor': '#FFFFFF',
            'border': '1px solid #ccc',
            'borderRadius': '8px',
            'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.1)',
            'padding': '20px',
            'overflowY': 'auto',
            'height': '700px'
        }, children=[
            
            # Title above the list
            html.H3("Top 10 Potential Artist Collaborations", 
                    style={
                        'textAlign': 'center',
                        'color': '#003057',
                        'marginBottom': '15px',
                        'fontSize': '22px',
                        'fontWeight': 'bold'
                    }),
            
            # Collaboration list container
            html.Div(id='collaboration-list')
        ])
    ])
])

# Callback to update the map, revenue tracker, and collaborations list
@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('total-revenue-tracker', 'children'),
     Output('collaboration-list', 'children')],
    [Input('primary-artist-dropdown', 'value')]
)
def update_dashboard(primary_artist):
    # Filter data for the selected artist
    filtered_df = melted_df[
        (melted_df['artist_1_name'] == primary_artist) | 
        (melted_df['artist_2_name'] == primary_artist)
    ]

    # Count collaborations and revenue by country
    collab_count = filtered_df.groupby('country').size().reset_index(name='collaborations')
    revenue_by_country = filtered_df.groupby('country', as_index=False).sum()
    merged_df = revenue_by_country.merge(collab_count, on='country', how='left')

    # Calculate total revenue for the selected artist
    total_revenue = filtered_df['revenue'].sum()
    total_revenue_display = f"Total Estimated Revenue: ${total_revenue:,.2f}"

    # Generate the top collaborations list
    top_collaborations = (
        filtered_df.groupby(['artist_1_name', 'artist_2_name'])
        .agg({'revenue': 'sum'})
        .reset_index()
        .sort_values(by='revenue', ascending=False)
        .head(10)
    )

    # Generate HTML list items
    collaboration_items = [
        html.Div(
            children=[
                html.P(f"{row['artist_1_name']} & {row['artist_2_name']}",
                       style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#003057'}),
                html.P(f"Revenue: ${row['revenue']:,.2f}",
                       style={'fontSize': '16px', 'color': '#204060'})
            ],
            style={
                'padding': '15px',
                'borderBottom': '1px solid #ccc',
                'backgroundColor': '#F9F9F9' if i % 2 == 0 else '#FFFFFF'
            }
        )
        for i, row in top_collaborations.iterrows()
    ]

    # Custom navy color scale
    custom_colorscale = [
        [0, "#F0F4F8"],
        [1, "#003057"]
    ]

    fig = px.choropleth(
        merged_df,
        locations='country',
        locationmode='country names',
        color='revenue',
        hover_name='country',
        hover_data={'revenue': ':$,.2f', 'collaborations': True},
        color_continuous_scale=custom_colorscale
    )

    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})

    return fig, total_revenue_display, collaboration_items

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
