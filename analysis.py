from dash import Dash, html, dcc,callback, Input, Output,State, ctx, dash_table
import pandas as pd
import mysql.connector
import base64
from PIL import Image
import requests
from io import BytesIO
import plotly.express as px
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

def avatar_Image(login_name):
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

def User_Profile_details(login_name):
    mycursor.execute(f"Select * from user_details where Login = '{login_name}' ")
    data= mycursor.fetchall()
    df = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    profile_details= [
        dcc.Markdown('# ***User Details***', style = {'color': '#FAFAFA'}),
        dcc.Markdown(f"### {df.User_Name.iloc[0]}", style = {'color': '#4090F5'}),
        dcc.Markdown(f"### {df.Login.iloc[0]}", style = {'color': '#4090F5'}),
        dcc.Markdown(f"### {df.Bio.iloc[0]}", style = {'color': '#4090F5'}),
        dcc.Markdown(f"### Join At - {df.Joined_At.iloc[0]}", style = {'color': '#4090F5'}),
        dcc.Markdown(f"### {df.Location.iloc[0]}", style = {'color': '#4090F5'}),
        dcc.Markdown(f"### {df.Email.iloc[0]}", style = {'color': '#4090F5'}),
        dcc.Markdown(f"### {df.Company.iloc[0]}", style = {'color': '#4090F5'}),
        dcc.Markdown(f"### {df.Public_Repos.iloc[0]}", style = {'color': '#4090F5'}),
        dcc.Markdown(f"### [View Profile on Github]({df.Profile_url.iloc[0]})", style = {'color': '#4090F5'}),
        # dcc.Markdown(f"# {df.Bio.iloc[0]}", style = {'color': '#4090F5'}),
    ]
    return profile_details


def Repo_per_Languages_fig(login_name):
    mycursor.execute(f"""SELECT Language_Used as Language, COUNT(*) as Count FROM repositories_details
                        WHERE Owner = '{login_name}' AND Language_Used IS NOT NULL
                        GROUP BY Language_Used;""")
    data1 = mycursor.fetchall()
    df1 = pd.DataFrame(data1, columns=[i[0] for i in mycursor.description]) 

    fig1 = px.pie(df1, values='Count', names='Language', title='Repos Per Languages', hole = 0.5)
    fig1.update_layout({
    'plot_bgcolor': '#E8CFCA',  # Setting the plot background color
    'paper_bgcolor': '#E8CFCA'  # Setting the paper background color
        })
    return fig1

def Commits_Per_Languages_fig(login_name):
    mycursor.execute(f"""SELECT Language_Used as Language, sum(Commits) AS Commits FROM repositories_details
                        WHERE Owner = '{login_name}' AND Language_Used IS NOT NULL
                        GROUP BY Language_Used;""")
    data2 = mycursor.fetchall()
    df2 = pd.DataFrame(data2, columns=[i[0] for i in mycursor.description]) 


    fig = px.pie(df2, values='Commits', names='Language', title='Commits Per Languages ', hole = 0.5)
    fig.update_layout({
    'plot_bgcolor': '#E8CFCA',  # Setting the plot background color
    'paper_bgcolor': '#E8CFCA'  # Setting the paper background color
        })
    return fig

def Stars_Per_Languages_fig(login_name):
    mycursor.execute(f"""SELECT Language_Used as Language, sum(Stargazers) AS Stars FROM repositories_details
                        WHERE Owner = '{login_name}' AND Language_Used IS NOT NULL
                        GROUP BY Language_Used;""")
    data3 = mycursor.fetchall()
    df3 = pd.DataFrame(data3, columns=[i[0] for i in mycursor.description]) 

    fig = px.pie(df3, values='Stars', names='Language', title='Stars Per Languages', hole = 0.5)
    fig.update_layout({
    'plot_bgcolor': '#E8CFCA',  # Setting the plot background color
    'paper_bgcolor': '#E8CFCA'  # Setting the paper background color
        })
    return fig

def Top_Commits_per_repo_fig(login_name):
    mycursor.execute(f"""SELECT Repo_Name, sum(Commits) as Commits FROM repositories_details
                        WHERE Owner = '{login_name}' AND Language_Used IS NOT NULL
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

def Top_Stars_Per_repo_fig(login_name):
    mycursor.execute(f"""SELECT Repo_Name, sum(Stargazers) as Stars FROM repositories_details
                        WHERE Owner = '{login_name}' AND Language_Used IS NOT NULL
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