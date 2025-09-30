import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
import pickle
import numpy as np

location_keys = np.array(['Airoli', 'Ambernath East', 'Ambernath West', 'Andheri',
       'Andheri East', 'Andheri West', 'Badlapur East', 'Bandra West',
       'Belapur', 'Bhandup West', 'Bhayandar East', 'Bhiwandi', 'Boisar',
       'Borivali East', 'Borivali West', 'Chembur', 'Chembur East',
       'Dahisar', 'Dahisar East', 'Dahisar West', 'Dattapada',
       'Dombivali', 'Dombivali East', 'Dombivli (West)', 'Dronagiri',
       'Ghansoli', 'Ghatkopar West', 'Goregaon', 'Goregaon East',
       'Goregaon West', 'Jogeshwari West', 'Juhu', 'Kalwa', 'Kalyan East',
       'Kalyan West', 'Kamothe', 'Kandivali East', 'Kandivali West',
       'Kanjurmarg', 'Karanjade', 'Karjat', 'Khar West', 'Kharghar',
       'Kolshet Road', 'Koper Khairane', 'Koproli', 'Kurla', 'Kurla West',
       'Magathane', 'Majiwada', 'Malad East', 'Malad West',
       'Mira Road East', 'Mira Road and Beyond', 'Mulund', 'Mulund East',
       'Mulund West', 'Mumbai Central', 'Naigaon East', 'Nala Sopara',
       'Nalasopara East', 'Nalasopara West', 'Nerul', 'Panvel', 'Parel',
       'Powai', 'Sanpada', 'Santacruz East', 'Seawoods', 'Sector 10',
       'Sector 17 Ulwe', 'Sector 19 Kharghar', 'Sector 20 Kharghar',
       'Sector-18 Ulwe', 'Sector12 Kamothe', 'Sector9 Kamothe', 'Sion',
       'Taloja', 'Thakur Village', 'Thane', 'Thane West', 'Titwala',
       'Ulwe', 'Vasai', 'Vasai West', 'Vasai east', 'Vashi',
       'Ville Parle East', 'Virar', 'Virar East', 'Virar West', 'Wadala',
       'Wadala East Wadala', 'matunga east', 'mumbai', 'other']).astype(object)

# Load the model
with open('model.pickle', 'rb') as f:
    model = pickle.load(f)
    
# Increase the intercept of the Ridge model
model.named_steps["ridge"].intercept_ = 2800000

# Create the Dash app
app = dash.Dash(__name__)

# Set up Flask server to serve static files
server = app.server

app.layout = html.Div([
    # Background image container
    html.Div(style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'width': '100%',
        'height': '100%',
        'zIndex': '-1',
        'backgroundImage': 'url("/assets/background.jpg")',
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'backgroundRepeat': 'no-repeat',
        'filter': 'brightness(0.7)'  # Slightly darken the background for better text readability
    }),

    # Content container with semi-transparent background
    html.Div(style={
        'backgroundColor': 'rgba(255, 255, 255, 0.85)',
        'minHeight': '100vh',
        'padding': '40px', # Increased padding for PC
        'maxWidth': '800px', # Max width for content on PC
        'margin': '40px auto', # Center the content container
        'borderRadius': '10px', # Add some border radius
        'boxShadow': '0 0 20px rgba(0, 0, 0, 0.1)', # Add a subtle shadow
        'fontFamily': 'Georgia, serif' # Changed font family
    }, children=[
        html.H1("Mumbai Apartment Price Prediction", style={
            'textAlign': 'center',
            'marginBottom': '40px',
            'color': '#2c3e50',
            'fontFamily': 'Georgia, serif', # Changed font family
            'fontSize': '36px' # Increased font size
        }),

        html.Div([
            html.H3("Area Sq/ft", style={'textAlign': 'center', 'marginBottom': '5px', 'color': '#34495e', 'fontSize': '20px'}), # Increased font size
            dcc.Input(id='area-input', type='number', value=1000, style={
                'width': '80%', # Adjusted width
                'padding': '8px', # Increased padding
                'borderRadius': '10px',
                'border': '1px solid #ddd',
                'textAlign': 'center',
                'margin': '0 auto', # Center the input
                'display': 'block' # Make it a block element to center
            })
        ], style={'marginBottom': '25px', 'width': '80%', 'margin': 'auto'}),

        html.Div([
            html.H3("Location", style={'textAlign': 'center', 'marginBottom': '5px', 'color': '#34495e', 'fontSize': '20px'}), # Increased font size
            dcc.Dropdown(
                id='location-dropdown',
                options=[{'label': i, 'value': i} for i in location_keys],
                value='Kharghar',
                style={
                    'width': '80%', # Adjusted width
                    'padding': '8px', # Increased padding
                    'borderRadius': '5px',
                    'border': '1px solid #ddd',
                    'textAlign': 'center',
                    'margin': '0 auto', # Center the dropdown
                    'display': 'block' # Make it a block element to center
                }
            )
        ], style={'marginBottom': '25px', 'width': '80%', 'margin': 'auto'}),

        html.Div([
            html.H3("BHK", style={'textAlign': 'center', 'marginBottom': '5px', 'color': '#34495e', 'fontSize': '20px'}), # Increased font size
            dcc.Dropdown(
                id='bhk-input',
                options=[{'label': i, 'value': i} for i in range(1, 6)],  # Assuming BHK values from 1 to 5
                value=2,
                style={
                    'width': '80%', # Adjusted width
                    'padding': '8px', # Increased padding
                    'borderRadius': '5px',
                    'border': '1px solid #ddd',
                    'textAlign': 'center',
                    'margin': '0 auto', # Center the dropdown
                    'display': 'block' # Make it a block element to center
                }
            )
        ], style={'marginBottom': '25px', 'width': '80%', 'margin': 'auto'}),

        html.Div([
            html.H3("Resale", style={'textAlign': 'center', 'marginBottom': '5px', 'color': '#34495e', 'fontSize': '20px'}), # Increased font size
            dcc.Dropdown(
                id='resale-dropdown',
                options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                value=True,
                style={
                    'width': '80%', # Adjusted width
                    'padding': '8px', # Increased padding
                    'borderRadius': '5px',
                    'border': '1px solid #ddd',
                    'textAlign': 'center',
                    'margin': '0 auto', # Center the dropdown
                    'display': 'block' # Make it a block element to center
                }
            )
        ], style={'marginBottom': '25px', 'width': '80%', 'margin': 'auto'}),

        html.Div([
            html.H3("Swimming Pool", style={'textAlign': 'center', 'marginBottom': '5px', 'color': '#34495e', 'fontSize': '20px'}), # Increased font size
            dcc.Dropdown(
                id='swimmingpool-dropdown',
                options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                value=False,
                style={
                    'width': '80%', # Adjusted width
                    'padding': '8px', # Increased padding
                    'borderRadius': '5px',
                    'border': '1px solid #ddd',
                    'textAlign': 'center',
                    'margin': '0 auto', # Center the dropdown
                    'display': 'block' # Make it a block element to center
                }
            )
        ], style={'marginBottom': '25px', 'width': '80%', 'margin': 'auto'}),

        html.Div([
            html.H3("Landscaped Gardens", style={'textAlign': 'center', 'marginBottom': '5px', 'color': '#34495e', 'fontSize': '20px'}), # Increased font size
            dcc.Dropdown(
                id='landscapedgardens-dropdown',
                options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                value=False,
                style={
                    'width': '80%', # Adjusted width
                    'padding': '8px', # Increased padding
                    'borderRadius': '5px',
                    'border': '1px solid #ddd',
                    'textAlign': 'center',
                    'margin': '0 auto', # Center the dropdown
                    'display': 'block' # Make it a block element to center
                }
            )
        ], style={'marginBottom': '25px', 'width': '80%', 'margin': 'auto'}),

        html.Div([
            html.H3("Club House", style={'textAlign': 'center', 'marginBottom': '5px', 'color': '#34495e', 'fontSize': '20px'}), # Increased font size
            dcc.Dropdown(
                id='clubhouse-dropdown',
                options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                value=False,
                style={
                    'width': '80%', # Adjusted width
                    'padding': '8px', # Increased padding
                    'borderRadius': '5px',
                    'border': '1px solid #ddd',
                    'textAlign': 'center',
                    'margin': '0 auto', # Center the dropdown
                    'display': 'block' # Make it a block element to center
                }
            )
        ], style={'marginBottom': '25px', 'width': '80%', 'margin': 'auto'}),

        html.Div([
            html.H3("Car Parking", style={'textAlign': 'center', 'marginBottom': '5px', 'color': '#34495e', 'fontSize': '20px'}), # Increased font size
            dcc.Dropdown(
                id='carparking-dropdown',
                options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                value=True,
                style={
                    'width': '80%', # Adjusted width
                    'padding': '8px', # Increased padding
                    'borderRadius': '5px',
                    'border': '1px solid #ddd',
                    'textAlign': 'center',
                    'margin': '0 auto', # Center the dropdown
                    'display': 'block' # Make it a block element to center
                }
            )
        ], style={'marginBottom': '25px', 'width': '80%', 'margin': 'auto'}),

        html.Div([
            html.H3("Lift Available", style={'textAlign': 'center', 'marginBottom': '5px', 'color': '#34495e', 'fontSize': '20px'}), # Increased font size
            dcc.Dropdown(
                id='liftavailable-dropdown',
                options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                value=True,
                style={
                    'width': '80%', # Adjusted width
                    'padding': '8px', # Increased padding
                    'borderRadius': '5px',
                    'border': '1px solid #ddd',
                    'textAlign': 'center',
                    'margin': '0 auto', # Center the dropdown
                    'display': 'block' # Make it a block element to center
                }
            )
        ], style={'marginBottom': '25px', 'width': '80%', 'margin': 'auto'}),


        html.Button('Predict Price', id='predict-button', n_clicks=0, style={
            'display': 'block',
            'margin': '40px auto',
            'padding': '15px 30px',
            'fontSize': '18px',
            'backgroundColor': '#3498db',
            'color': 'white',
            'border': 'none',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'transition': 'background-color 0.3s'
        }),

        html.Div(id='output-prediction', style={
            'textAlign': 'center',
            'marginTop': '40px',
            'fontSize': '28px', # Increased font size for prediction
            'fontWeight': 'bold',
            'color': '#2c3e50'
        })
    ])
])

@app.callback(
    Output('output-prediction', 'children'),
    Input('predict-button', 'n_clicks'),
    State('area-input', 'value'),
    State('location-dropdown', 'value'),
    State('bhk-input', 'value'),
    State('resale-dropdown', 'value'),
    State('swimmingpool-dropdown', 'value'),
    State('landscapedgardens-dropdown', 'value'),
    State('clubhouse-dropdown', 'value'),
    State('carparking-dropdown', 'value'),
    State('liftavailable-dropdown', 'value')
)
def update_output(n_clicks, area, location, bhk, resale, swimmingpool, landscapedgardens, clubhouse, carparking, liftavailable):
    if n_clicks > 0:
        input_data = pd.DataFrame([[area, location, bhk, resale, swimmingpool, landscapedgardens, clubhouse, carparking, liftavailable]],
                                  columns=['Area', 'Location', 'BHK', 'Resale', 'SwimmingPool', 'LandscapedGardens', 'ClubHouse', 'CarParking', 'LiftAvailable'])
        prediction = model.predict(input_data)[0]
        return f'Predicted Price: ₹{prediction:,.0f}'
    return ''

if __name__ == '__main__':

    app.run(debug=True)

