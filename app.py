from dash import Dash, html, dcc,callback, Input, Output, ctx
import dash

import render_file as render

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
    [Input("fetch", "n_clicks"),Input("login", "value")],
)

def extract_tab(fetch, login):
    button = ctx.triggered_id
    if button =='fetch' and login:  
        # print(login)
        return html.H1(login)



if __name__ == '__main__':
    app.run_server(debug=True)