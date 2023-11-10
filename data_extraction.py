from github import Github
# Authentication is defined via github.Auth
from github import Auth
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


access_token = os.getenv("ACCESS_TOKEN")
# using an access token
auth = Auth.Token(access_token)

# # Public Web Github
g = Github(auth=auth)




# mysql_host_name = os.getenv("MYSQL_HOST_NAME")
# mysql_user_name = os.getenv("MYSQL_USER_NAME")
# mysql_password = os.getenv("MYSQL_PASSWORD")
# mysql_database_name = os.getenv("MYSQL_DATABASE_NAME")

# db = mysql.connector.connect(host = mysql_host_name,
#                              user = mysql_user_name,
#                              password = mysql_password,
#                              database = mysql_database_name)
# mycursor = db.cursor(buffered = True)


def User_details(user_login_name):
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
    return userdetails

