from dash import Dash, html, dcc,callback, Input, Output,State, ctx, dash_table
import pandas as pd
import base64
from PIL import Image
import requests
from io import BytesIO
import plotly.express as px


def avatar_Image(mycursor, login_name):
    mycursor.execute(f"Select * from user_details where Login = '{login_name}' ")
    data= mycursor.fetchall()
    df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    # print(df.Avatar_url.iloc[0])
    url = df['Avatar_url'].iloc[0]
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    encoded_img = 'data:image/png;base64,' + base64.b64encode(img_bytes.getvalue()).decode()
    image = html.Img(src=encoded_img, style={'width': '80%', 'height': '80%'})
    return image

def User_Profile_details(mycursor, login_name):
    mycursor.execute(f"Select * from user_details where Login = '{login_name}' ")
    data= mycursor.fetchall()
    df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])

    profile_details = [dcc.Markdown('## ***User Details***', style = {'color': '#FAFAFA'}),
                        dcc.Markdown(f''' > User Name: {df.User_Name.iloc[0]}
                                        \n > Login Name:{df.Login.iloc[0]}
                                        \n > Bio: {df.Login.iloc[0]}
                                        \n > Joined At: {df.Joined_At.iloc[0]}
                                        \n > Location: {df.Location.iloc[0]}
                                        \n > Email: {df.Email.iloc[0]}
                                        \n > Organization: {df.Company.iloc[0]}
                                        \n > Repo Count: {df.Public_Repos.iloc[0]}
                                        \n > [View Profile on Github]({df.Profile_url.iloc[0]})''', style = {'color': '#4090F5',})]

    return profile_details

def Contributions_fig(mycursor, login_name):
    mycursor.execute(f"Select Created_At, Commits from repositories_details where Owner = '{login_name}' AND Is_Fork = False;")
    data= mycursor.fetchall()
    df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    df['Created_At'] = pd.to_datetime(df['Created_At'], errors='coerce')
    df['YearMonth'] = df['Created_At'].dt.to_period('M').dt.strftime('%Y-%m')

    # Group by year-month and sum the commits
    monthly_commits = df.groupby('YearMonth')['Commits'].sum().reset_index()
  
    fig = px.area(monthly_commits, x='YearMonth', y='Commits', title='Commit Trend Over Time', markers=True)
    # fig.update_traces(mode='lines')  # Change mode to lines to create an area plot
    df=df.groupby('Created_At')['Commits'].sum().reset_index()
    fig = px.line(df, x='Created_At', y='Commits', markers='o', text = 'Commits',
                   height=400)
    # fig.update_traces(textposition= 'top') 
    return fig


def Repo_per_Languages_fig(mycursor, login_name):
    mycursor.execute(f"""SELECT Language_Used as Language, COUNT(*) as Count FROM repositories_details
                        WHERE Owner = '{login_name}' AND Is_Fork = False AND Language_Used IS NOT NULL
                        GROUP BY Language_Used;""")
    data1 = mycursor.fetchall()
    df1 = pd.DataFrame(data1, columns=[i[0] for i in mycursor.description]) 

    fig1 = px.pie(df1, values='Count', names='Language', title='Repos Per Languages', hole = 0.5)
    fig1.update_layout({
    'plot_bgcolor': '#E8CFCA',  # Setting the plot background color
    'paper_bgcolor': '#E8CFCA'  # Setting the paper background color
        })
    return fig1

def Commits_Per_Languages_fig(mycursor, login_name):
    mycursor.execute(f"""SELECT Language_Used as Language, sum(Commits) AS Commits FROM repositories_details
                        WHERE Owner = '{login_name}' AND Is_Fork = False AND Language_Used IS NOT NULL
                        GROUP BY Language_Used;""")
    data2 = mycursor.fetchall()
    df2 = pd.DataFrame(data2, columns=[i[0] for i in mycursor.description]) 


    fig = px.pie(df2, values='Commits', names='Language', title='Commits Per Languages ', hole = 0.5)
    fig.update_layout({
    'plot_bgcolor': '#E8CFCA',  # Setting the plot background color
    'paper_bgcolor': '#E8CFCA'  # Setting the paper background color
        })
    return fig

def Stars_Per_Languages_fig(mycursor, login_name):
    mycursor.execute(f"""SELECT Language_Used as Language, sum(Stargazers) AS Stars FROM repositories_details
                        WHERE Owner = '{login_name}' AND Is_Fork = False AND Language_Used IS NOT NULL
                        GROUP BY Language_Used;""")
    data3 = mycursor.fetchall()
    df3 = pd.DataFrame(data3, columns=[i[0] for i in mycursor.description]) 

    fig = px.pie(df3, values='Stars', names='Language', title='Stars Per Languages', hole = 0.5)
    fig.update_layout({
    'plot_bgcolor': '#E8CFCA',  # Setting the plot background color
    'paper_bgcolor': '#E8CFCA'  # Setting the paper background color
        })
    return fig

def Top_Commits_per_repo_fig(mycursor, login_name):
    mycursor.execute(f"""SELECT Repo_Name, sum(Commits) as Commits FROM repositories_details
                        WHERE Owner = '{login_name}' AND Is_Fork = False AND Language_Used IS NOT NULL
                        GROUP BY Repo_Name
                        ORDER BY Commits DESC LIMIT 10;""")
    data4 = mycursor.fetchall()
    df4 = pd.DataFrame(data4, columns=[i[0] for i in mycursor.description]) 

    fig = px.pie(df4, values='Commits', names='Repo_Name', title='Commits Per Repo', hole = 0.5)
    fig.update_layout({
    'plot_bgcolor': '#E8CFCA',  # Setting the plot background color
    'paper_bgcolor': '#E8CFCA'  # Setting the paper background color
        })
    
    return fig

def Top_Stars_Per_repo_fig(mycursor, login_name):
    mycursor.execute(f"""SELECT Repo_Name, sum(Stargazers) as Stars FROM repositories_details
                        WHERE Owner = '{login_name}' AND Is_Fork = False AND Language_Used IS NOT NULL
                        GROUP BY Repo_Name
                        ORDER BY Stars DESC LIMIT 10;""")
    data5= mycursor.fetchall()
    df5 = pd.DataFrame(data5, columns=[i[0] for i in mycursor.description]) 

    fig = px.pie(df5, values='Stars', names='Repo_Name', title='Stars Per Repo', hole = 0.5)
    fig.update_layout({
    'plot_bgcolor': '#E8CFCA',  # Setting the plot background color
    'paper_bgcolor': '#E8CFCA'  # Setting the paper background color
        })
    
    return fig