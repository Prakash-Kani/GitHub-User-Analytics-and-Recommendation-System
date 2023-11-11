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