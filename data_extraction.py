from github import Github
# Authentication is defined via github.Auth
from github import Auth
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


access_token = os.getenv("ACCESS_TOKEN")
# using an access token
auth = Auth.Token(access_token)

# # Public Web Github
g = Github(auth=auth)




mysql_host_name = os.getenv("MYSQL_HOST_NAME")
mysql_user_name = os.getenv("MYSQL_USER_NAME")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_database_name = os.getenv("MYSQL_DATABASE_NAME")

mydb = mysql.connector.connect(host = mysql_host_name,
                             user = mysql_user_name,
                             password = mysql_password,
                             database = mysql_database_name)
mycursor = mydb.cursor(buffered = True)


def User_Details(user_login_name):
    try:
        user = g.get_user(user_login_name)
        # Languages used
        languages_used = set()
        for repo in user.get_repos():
            languages = repo.get_languages().keys()
            for language in languages:
                languages_used.add(language)
            # Fetching user details
        data=dict(User_Name = user.name,
        Login = user.login,
        Bio = user.bio,
        Joined_At =user.created_at,
        Email =user.email,
        Location =user.location,
        Company = user.company,
        # subscriber_count = user.get_subscribers().totalCount
        Following_Count = user.get_following().totalCount,
        Followers_Count = user.get_followers().totalCount,
        Public_Repos = user.public_repos,

        # Avatar URL
        Avatar_url = user.avatar_url,
        # Profile URL
        Profile_url = user.html_url,

        # Languages used
        Languages_Used = " ".join(list(languages_used)),
        # Starred Repositories
        Starred_Repos = " ".join([repo.full_name for repo in user.get_starred()]))

    except Exception as e:
        print(f"An error occurred: {e}")
    userdetails=pd.DataFrame([data])
    userdetails['Joined_At'] = pd.to_datetime(userdetails['Joined_At']).dt.date
    return userdetails


def Repositories_Details(user_login_name):
    repo_list =[]
    for repo in g.get_user(user_login_name).get_repos():
        try:
            commits_count = repo.get_commits().totalCount
        except:
            commits_count = 0
        data = dict(Owner = repo.owner.login,
                    Repo_Name = repo.name,
                    Repo_Link = repo.clone_url,
                    Created_At = repo.created_at,
                    Description = repo.description,
                    Forks_Count = repo.forks_count,
                    Repo_Fullname = repo.full_name,
                    Repo_ID = repo.id,
                    Language_Used = repo.language,
                    Last_Modified = repo.last_modified,
                    Pushed_At = repo.pushed_at,
                    Size =  repo.size,
                    Subscriber = repo.subscribers_count,
                    Stargazers = repo.stargazers_count,
                    Updated_At = repo.updated_at,
                    Watchers_Counts = repo.watchers_count,
                    Commits = commits_count



                    )
        repo_list.append(data)

    repo_details = pd.DataFrame(repo_list)
    return repo_details


def User_Details_Migration(uservalues):
    mycursor.execute("""CREATE TABLE IF NOT EXISTS user_details(
                        User_Name VARCHAR(250),
                        Login VARCHAR(250) PRIMARY KEY,
                        Bio TEXT,
                        Joined_AT DATE,
                        Email VARCHAR(250),
                        Location VARCHAR(250),
                        Company VARCHAR(250), 
                        Following_Count INT,
                        Followers_Count INT,
                        Public_Repos INT,
                        Avatar_url VARCHAR(250),
                        Profile_url VARCHAR(250),
                        Languages_Used TEXT,
                        Starred_Repo LONGTEXT);""")
    mydb.commit()
    query = f"""INSERT INTO userdetails
                (User_Name, Login, Bio, Joined_At, Email, Location, Company, Following_Count, Followers_Count, Public_Repos, Avatar_url, Profile_url, Languages_Used, Starred_Repo) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                User_Name = VALUES(User_Name), 
                Login = VALUES(Login), 
                Bio = VALUES(Bio), 
                Joined_At = VALUES(Joined_At),
                Email = VALUES(Email),
                Location = VALUES(Location),
                Company = VALUES(Company),
                Following_Count = VALUES(Following_Count),
                Followers_Count = VALUES(Followers_Count),
                Public_Repos = VALUES(Public_Repos),
                Avatar_url = VALUES(Avatar_url),
                Profile_url = VALUES(Profile_url),
                Languages_used = VALUES(Languages_Used),
                Starred_Repo = VALUES(Starred_Repo);"""
    mycursor.executemany(query,uservalues)
    mydb.commit()
    return 'Successfully Inserted!'