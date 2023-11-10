from dash import Dash, html, dcc,callback, Input, Output,State, ctx, dash_table
import dash_bootstrap_components as dbc
import mysql.connector

import render_file as render
import data_extraction as extract

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
    if tab == 'tab-1':
        return render.Extracting_Data_tab()
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    

@callback(
    Output("new", "children"),
    [Input("fetch", "n_clicks"), Input("save to mysql", "n_clicks"), Input("login", "value")],
)

def extract_tab(fetch, sql, user_login_name):
    button = ctx.triggered_id
    # print(button)
    # print(user_login_name)
    if button =='fetch' and user_login_name:  
        userdetails = extract.User_Details(user_login_name = user_login_name)
        # repodetails = extract.Repositories_Details(user_login_name = user_login_name)
        return [html.H1(user_login_name),
                html.Label("User Details Table"),
                dash_table.DataTable(userdetails.to_dict('records'),[{"name": i, "id": i} for i in userdetails.columns], id='user-detials-tbl'),
                html.Label("Repositories Details Table"),]
                # dash_table.DataTable(repodetails.to_dict('records'),[{"name": i, "id": i} for i in repodetails.columns], id='repo-detials-tbl')]
    if button=='save to mysql' and user_login_name:
        userdetails = extract.User_Details(user_login_name = user_login_name)
        values = userdetails.to_records(index = False)
        uservalues= values.tolist()
        print(uservalues)
        insert=extract.User_Details_Migration(uservalues)
        if insert:
            return [html.H1(user_login_name),
                    html.Label("User Details Table"),
                    dash_table.DataTable(userdetails.to_dict('records'),[{"name": i, "id": i} for i in userdetails.columns], id='user-detials-tbl'),
                    # html.Label("Repositories Details Table"),
                    # dash_table.DataTable(repodetails.to_dict('records'),[{"name": i, "id": i} for i in repodetails.columns], id='repo-detials-tbl')]
                    html.H2('Successfully insert')]
            # return [html.H1(user_login_name),
            #         html.Label("User Details Table"),
            #         dash_table.DataTable(userdetails.to_dict('records'),[{"name": i, "id": i} for i in userdetails.columns], id='user-detials-tbl'),
            #         html.Label("Repositories Details Table"),
            #         dash_table.DataTable(repodetails.to_dict('records'),[{"name": i, "id": i} for i in repodetails.columns], id='repo-detials-tbl')]



if __name__ == '__main__':
    app.run_server(debug=True)