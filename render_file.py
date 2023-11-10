from dash import Dash, html, dcc

def Extracting_Data_tab():
    page =[
        html.Div([
            html.Div([
                html.Label('Enter the Login Name to Fetch the Details'),
                html.Br(),
                dcc.Input(id="login", type="text", placeholder="", style={'marginRight':'10px'}),]),
            html.Button("Fetch Details", id = "fetch", n_clicks = 0),
            html.Hr(),
            html.Div(id='new'),
            html.Button("Save To MYSQL", id = "save", n_clicks = 0),
        ])
    ]
    return page
