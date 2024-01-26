import pandas as pd
import mysql.connector
import spacy
import base64
from PIL import Image
import requests
from io import BytesIO
from dash import Dash, html, dcc
import json
import pickle

from sklearn.preprocessing import OrdinalEncoder
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


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


cluster_df = pd.read_csv(r'src/repo_clusters.csv')

enc = OrdinalEncoder()

cluster_df['Owner'] = enc.fit_transform(cluster_df[['Owner']])
cluster_df['Language_Used'] = enc.fit_transform(cluster_df[['Language_Used']])

nlp = spacy.load('en_core_web_md')

#  Load the JSON data into a Python dictionary
with open(r'src/Category_Columns_Encoded_Data.json', 'r') as file:
    unique_value = json.load(file)

unique_value_ref ={i[1]:i[0] for i in unique_value['Owner'].items()}

with open(r'src/Cluster_Classifying_Model.pkl', 'rb') as file:
    knn_classifier = pickle.load(file)
with open(r'src/Cluster_Classifying_Model.pkl', 'rb') as file:
    model = pickle.load(file)

file = open(r'src/Cluster_Classifying_Model.pkl', 'rb')
knn_classifier = pickle.load(file)


def get_repo_details():
    mydb, mycursor = get_mysql_connection()

    mycursor.execute("Select * from repositories_details;")
    data= mycursor.fetchall()
    repo = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])

    repo1 = repo.copy()
    repo1.drop(index=repo[repo.Language_Used.isna()==True]['Repo_Link'].index, inplace = True)

    repo1.drop('Last_Modified', axis = 1, inplace = True)
    repo1.fillna('Not Specified', inplace= True)
    repo1.reset_index(drop = True, inplace = True)

    return repo1

def Yet_to_pred(username):

    repo1 = get_repo_details()

    test_user = cluster_df[cluster_df['Owner']== unique_value['Owner']['Prakash-Kani']]
    # print(test_user)
    pred =knn_classifier.predict(test_user.drop('Predicted_Clusters', axis =1))
    pred = pd.Series(pred)

    user_data = repo1[repo1['Owner']== username][['Repo_Name', 'Description', 'Owner' ]]

    cluster_index = [ind for ind in cluster_df[cluster_df['Predicted_Clusters']==pred.value_counts().index[0]].index]
    cluster_details = repo1.iloc[cluster_index][['Repo_Name', 'Description', 'Owner' ]]
    cluster_details.reset_index(drop= True, inplace = True)
    user_index = cluster_details[cluster_details['Owner']==username].index


    # nlp = spacy.load('en_core_web_md')

    repo_doc = [nlp(i) for i in cluster_details['Repo_Name']]
    description_doc = [nlp(i) for i in cluster_details['Description']]

    repo_vector = [token.vector for token in repo_doc]
    description_vector = [token.vector for token in description_doc]


    repo_df = pd.DataFrame(repo_vector)

    repo_df.columns =['repo_vector_' + str(i) for i in repo_df.columns]

    # Create a DataFrame with the description vectors
    description_df = pd.DataFrame(description_vector)
    description_df.columns = ['description_vector_' + str(i) for i in description_df.columns]
    # Merge the two DataFrames into one
    df1 = pd.merge(repo_df, description_df, left_index=True, right_index=True)
    df1['Owner'] = cluster_details['Owner']
    return user_index, cluster_details, df1

from sklearn.metrics.pairwise import cosine_similarity
def get_similarity(username):
    
    user_indices, cluster_details, df = Yet_to_pred(username)

    enc = OrdinalEncoder()
    df['Owner'] = enc.fit_transform(df[['Owner']])

    similarity_matrix = cosine_similarity(df)

    user_similarity_scores = similarity_matrix[user_indices].mean(axis=0)

    # Create a DataFrame with owner indices and their similarity scores
    similarity_df = pd.DataFrame({'Owner': df['Owner'], 'Similarity': user_similarity_scores})

    # Sort the DataFrame by similarity scores in descending order
    sorted_similarity_df = similarity_df.sort_values(by='Similarity', ascending=False)

    # Exclude the user's own indices
    sorted_similarity_df = sorted_similarity_df[sorted_similarity_df['Owner']!= unique_value['Owner'][username]]

    top_10_recommendations = sorted_similarity_df.head(10)


    # Display the recommendations
    return [unique_value_ref[owner] for owner in sorted_similarity_df.Owner.unique()[:10]]


def top10_user_recommedation(username):

    similarity_user = get_similarity(username)

    mydb, mycursor = get_mysql_connection()

    query = f"""SELECT User_Name, Login, Public_Repos, Avatar_url, Profile_url FROM user_details 
                WHERE Login IN {tuple(similarity_user)};"""
    
    mycursor.execute(query)
    data= mycursor.fetchall()
    recommend = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    print(recommend)

    return recommend

