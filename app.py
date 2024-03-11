from dash import Dash, html, dcc,callback, Input, Output,State, ctx, dash_table
import dash_bootstrap_components as dbc
import mysql.connector
import pandas as pd


import render_file as render
import data_extraction as extract
import analysis
import recommendation

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mysql_host_name = os.getenv("MYSQL_HOST_NAME")
mysql_user_name = os.getenv("MYSQL_USER_NAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database_name = os.getenv("MYSQL_DATABASE_NAME")

mydb = mysql.connector.connect(host = mysql_host_name,
                             user = mysql_user_name,
                             password = mysql_password,
                             database = mysql_database_name)
mycursor = mydb.cursor(buffered = True)

def get_mysql_connection():
    mysql_host_name = os.getenv("MYSQL_HOST_NAME")
    mysql_user_name = os.getenv("MYSQL_USER_NAME")
    mysql_password = os.getenv("MYSQL_PASSWORD")
    mysql_database_name = os.getenv("MYSQL_DATABASE_NAME")

    mydb = mysql.connector.connect(host = mysql_host_name,
                                user = mysql_user_name,
                                password = mysql_password,
                                database = mysql_database_name)
    mycursor = mydb.cursor(buffered = True)

    return mydb, mycursor

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__,
           title = 'GitHub',
           suppress_callback_exceptions = True,
           external_stylesheets = external_stylesheets)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Extracting Data', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Analysis', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Recommendation', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        # dcc.Tab(label='Tab 4', value='tab-4', style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles),
    html.Div(id='tab-page')
])


@callback(Output('tab-page', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    # mycursor.execute('SELECT DISTINCT(Login) FROM user_details;')
    # data = mycursor.fetchall()
    # uniquelogin = [i[0] for i in data]
    mydb, mycursor = get_mysql_connection()
    if tab == 'tab-1':
        return render.Extracting_Data_tab()
    elif tab == 'tab-2':
        return render.Analysis_tab(mycursor)
        
    elif tab == 'tab-3':
        return render.Recommendation_tab(mycursor)
    

@callback(
    Output("tables", "children"),
    [Input("save to mysql", "n_clicks"), Input("login", "value")],
)

def extract_tab(sql, user_login_name):
    button = ctx.triggered_id
    if button=='save to mysql' and user_login_name:
        mydb, mycursor = get_mysql_connection()

        userdetails = extract.User_Details(user_login_name = user_login_name)
        uservalues = userdetails.to_records(index = False)
        uservalues= uservalues.tolist()
        userinsert=extract.User_Details_Migration(mydb, mycursor, uservalues)
        repodetails = extract.Repositories_Details(user_login_name = user_login_name)
        repovalues = repodetails.to_records(index = False)
        repovalues= repovalues.tolist()
        repoinsert=extract.Repositories_Details_Migration(mydb, mycursor, repovalues)
        if userinsert and repoinsert:
            return [html.H1(user_login_name),
                    html.Label("User Details Table"),
                    dash_table.DataTable(userdetails.to_dict('records'),[{"name": i, "id": i} for i in userdetails.columns], id='user-detials-tbl'),
                    html.Label("Repositories Details Table"),
                    dash_table.DataTable(repodetails.to_dict('records'),[{"name": i, "id": i} for i in repodetails.columns], id='repo-detials-tbl'),
                    html.H2('Successfully insert')]



@app.callback([Output('avatar', 'children'), Output('user-details', 'children'), Output('Contribution fig', 'figure'),
                Output('Repos Per Languages fig', 'figure'), Output('Commits Per Languages fig', 'figure'),
                Output('Stars Per Languages fig', 'figure'), Output('Commits Per Repo fig', 'figure'),
                Output('Stars Per Repo fig', 'figure')],
              Input('user-login-name', 'value'),)

def Analysis_Tab(login_name):
    mydb, mycursor = get_mysql_connection()

    image = analysis.avatar_Image(mycursor, login_name)

    profile_details = analysis.User_Profile_details(mycursor, login_name)

    contribution = analysis.Contributions_fig(mycursor, login_name)

    repo_languages_analysis_fig = analysis.Repo_per_Languages_fig(mycursor, login_name)

    repo_languages_commits_fig = analysis.Commits_Per_Languages_fig(mycursor, login_name)

    stars_per_languages = analysis.Stars_Per_Languages_fig(mycursor, login_name)

    commits_per_repo = analysis.Top_Commits_per_repo_fig(mycursor, login_name)

    stars_per_repo = analysis.Top_Stars_Per_repo_fig(mycursor, login_name)

    return [image, profile_details, contribution, repo_languages_analysis_fig, repo_languages_commits_fig, stars_per_languages,
            commits_per_repo, stars_per_repo]

@app.callback([Output('user1', 'children'), Output('user2', 'children'), Output('user3', 'children'),
               Output('user4', 'children'), Output('user5', 'children'), Output('user6', 'children'),
               Output('user7', 'children'), Output('user8', 'children'), Output('user9', 'children'),
               Output('user1_details', 'children'), Output('user2_details', 'children'), Output('user3_details', 'children'),
               Output('user4_details', 'children'), Output('user5_details', 'children'), Output('user6_details', 'children'),
               Output('user7_details', 'children'), Output('user8_details', 'children'), Output('user9_details', 'children')],
               Input('user-login-name1', 'value'),)

def Recommendation_Tab_image(login_name):

    mydb, mycursor = get_mysql_connection()
    recommend = recommendation.top10_user_recommedation(login_name, mycursor)
    return recommendation.recommendation_details(recommend)

    

if __name__ == '__main__':
    app.run_server(debug=True)