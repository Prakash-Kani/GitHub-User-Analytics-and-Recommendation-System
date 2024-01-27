from dash import Dash, html, dcc

def User_Details(mycursor):
    mycursor.execute('SELECT DISTINCT(Login) FROM user_details;')
    data = mycursor.fetchall()
    uniquelogin = [i[0] for i in data]
    return uniquelogin

def Extracting_Data_tab():
    page =[
        html.Div([
            html.Div([
                html.Label('Enter the Login Name to Fetch the Details'),
                html.Br(),
                dcc.Input(id="login", type="text", placeholder="", style={'marginRight':'10px'}),]),
            html.Button("Fetch Details", id = "fetch", n_clicks = 0),
            html.Hr(),
            html.Div(id='tables'),
            html.Button("Save To MYSQL", id = "save to mysql", n_clicks = 0),
        ])
    ]
    return page



def Analysis_tab(mycursor):
    uniquelogin = User_Details(mycursor)
    page = [html.Div([
            html.Div([

                html.Label('Select the Username'),
                dcc.Dropdown(
                id = "user-login-name",
                options = [{"label": x, "value": x} for x in uniquelogin],
                value = uniquelogin[0],
                clearable = False,
            ),
            ]),

            # Second Column (Figures and Charts)
            html.Div([

                html.Div(id='avatar', style={'width': '20%', 'display': 'inline-block', 'backgroundColor':"#E8CFCA"}),
                html.Div(id ='user-details', style={'width': '20%', 'display': 'inline-block', 'backgroundColor':"#E8CFCA"}),
                html.Div([html.H1('Contribution Figure'),
                          dcc.Graph(id='Contribution fig')], style={'width': '60%', 'display': 'inline-block', 'backgroundColor':"#E8CFCA"}),
                html.Hr(),
            ], style = {'display': 'flex', 'flex-direction': 'row'}),
            html.Div([

                html.Div(dcc.Graph(id='Repos Per Languages fig'), style={'width': '33%', 'display': 'inline-block', 'backgroundColor':"#E8CFCA"}),
                html.Div(dcc.Graph(id='Commits Per Languages fig'), style={'width': '33%', 'display': 'inline-block', 'backgroundColor':"#E8CFCA"}),
                html.Div(dcc.Graph(id='Stars Per Languages fig'), style={'width': '34%', 'display': 'inline-block', 'backgroundColor':"#E8CFCA"}),
                html.Hr(),
            ], style = {'display': 'flex', 'flex-direction': 'row'}),
             html.Div([

                html.Div(dcc.Graph(id='Commits Per Repo fig'), style={'width': '50%', 'display': 'inline-block', 'backgroundColor':"#E8CFCA"}),
                html.Div(dcc.Graph(id='Stars Per Repo fig'), style={'width': '50%', 'display': 'inline-block', 'backgroundColor':"#E8CFCA"}),
                html.Hr(),
            ], style = {'display': 'flex', 'flex-direction': 'row'})
    ])

            ]

    return page

def Recommendation_tab(mycursor):
    uniquelogin = User_Details(mycursor)
    page = [html.Div([
            html.Div([
               html.Label('Select the Username'),
                dcc.Dropdown(
                id = "user-login-name1",
                options = [{"label": x, "value": x} for x in uniquelogin],
                value = uniquelogin[0],
                clearable = False,
            ),
            ]),

    ]),
    html.Hr(),
        html.Div([
            html.Div([html.Div(id = 'user1', style={'width': '13%', 'display': 'inline-block'}), 
                      html.Div(id = 'user1_details', style={'width': '30%', 'display': 'inline-block'}),
                      html.Div(id = 'user2', style={'width': '13%', 'display': 'inline-block'}), 
                      html.Div(id = 'user2_details', style={'width': '30%', 'display': 'inline-block'}),
                      html.Div(id = 'user3', style={'width': '14%', 'display': 'inline-block'}), 
                      html.Div(id = 'user3_details', style={'width': '30%', 'display': 'inline-block'})], style={'display': 'flex', 'flex-direction': 'row'}),

            html.Hr(),
            html.Div([html.Div(id = 'user4', style={'width': '13%', 'display': 'inline-block'}), 
                      html.Div(id = 'user4_details', style={'width': '30%', 'display': 'inline-block'}),
                      html.Div(id = 'user5', style={'width': '13%', 'display': 'inline-block'}), 
                      html.Div(id = 'user5_details', style={'width': '30%', 'display': 'inline-block'}),
                      html.Div(id = 'user6', style={'width': '14%', 'display': 'inline-block'}), 
                      html.Div(id = 'user6_details', style={'width': '30%', 'display': 'inline-block'})], style = {'display': 'flex', 'flex-direction': 'row'}),
            
            html.Hr(),
            html.Div([html.Div(id = 'user7', style={'width': '13%', 'display': 'inline-block'}), 
                      html.Div(id = 'user7_details', style={'width': '30%', 'display': 'inline-block'}),
                      html.Div(id = 'user8', style={'width': '13%', 'display': 'inline-block'}), 
                      html.Div(id = 'user8_details', style={'width': '30%', 'display': 'inline-block'}),
                      html.Div(id = 'user9', style={'width': '14%', 'display': 'inline-block'}), 
                      html.Div(id = 'user9_details', style={'width': '30%', 'display': 'inline-block'})], style = {'display': 'flex', 'flex-direction': 'row'}),

        ], style = {'display': 'flex', 'flex-direction': 'column'})

            ]

    return page