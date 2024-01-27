import pandas as pd
import spacy
import base64
from PIL import Image
import requests
from io import BytesIO
from dash import Dash, html, dcc
import json
import pickle

from sklearn.preprocessing import OrdinalEncoder
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity


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


def get_repo_details(mycursor):

    mycursor.execute("Select * from repositories_details;")
    data= mycursor.fetchall()
    repo = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])

    repo1 = repo.copy()
    repo1.drop(index=repo[repo.Language_Used.isna()==True]['Repo_Link'].index, inplace = True)

    repo1.drop('Last_Modified', axis = 1, inplace = True)
    repo1.fillna('Not Specified', inplace= True)
    repo1.reset_index(drop = True, inplace = True)

    return repo1

def to_get_test_data(username, mycursor):
    query = f"""Select Repo_Name, Description, Owner, Language_Used, Commits, 
                    Stargazers, Forks_Count, Is_Fork from repositories_details
                    where Owner = '{username}';"""
    mycursor.execute(query)
    data= mycursor.fetchall()
    user_data = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    user_data['Description'] = user_data['Description'].apply(lambda x:'Not Specified' if x == None  else x)

    repo_doc = [nlp(i) for i in user_data['Repo_Name']]
    description_doc = [nlp(i) for i in user_data['Description']]

    repo_vector = [token.vector for token in repo_doc]
    description_vector = [token.vector for token in description_doc]

    repo_df = pd.DataFrame(repo_vector)

    repo_df.columns =['repo_vector_' + str(i) for i in repo_df.columns]

    # Create a DataFrame with the description vectors
    description_df = pd.DataFrame(description_vector)
    description_df.columns = ['description_vector_' + str(i) for i in description_df.columns]
    # Merge the two DataFrames into one
    df1 = pd.merge(repo_df, description_df, left_index=True, right_index=True)

    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(df1)
    test_data =pd.DataFrame(pca_data, columns = ['Compnent_1', 'Compnent_2'])
    test_data[['Owner','Language_Used', 'Commits', 'Stargazers', 'Forks_Count','Is_Fork']] = user_data[['Owner','Language_Used', 'Commits', 'Stargazers', 'Forks_Count','Is_Fork']]
    test_data.dropna(axis = 0, inplace = True)

    test_data['Language_Used'] = test_data['Language_Used'].apply(lambda x: unique_value['Language_Used'][x])
    if username in unique_value['Owner'].keys():
        test_data['Owner'] = test_data['Owner'].apply(lambda x: unique_value['Owner'][x])
    else:
        test_data['Owner'] = test_data['Owner'].apply(lambda x: len(unique_value['Owner'].keys())+1)

    return test_data



def Yet_to_pred(username, mycursor):

    repo1 = get_repo_details(mycursor)
    test_data = to_get_test_data(username, mycursor)

    # test_user = cluster_df[cluster_df['Owner']== unique_value['Owner']['Prakash-Kani']]
    # print(test_user)
    pred =knn_classifier.predict(test_data)
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

def to_encoding(df3):
    data = df3['Owner'].unique()
    data.sort()
    unique_value_user ={}
    enc = OrdinalEncoder()
    df3['Owner'] = enc.fit_transform(df3[['Owner']])

    globals()['Owner'] = {}
    for i in df3['Owner'].unique():
        globals()['Owner'][data[int(i)]] = i
        unique_value_user['Owner'] = globals()['Owner']
    return df3, unique_value_user


def get_similarity(username, mycursor):
    
    user_indices, cluster_details, df = Yet_to_pred(username, mycursor)

    df, unique_value_user = to_encoding(df[['Owner']])
    # df['Owner'] = enc.fit_transform(df[['Owner']])

    similarity_matrix = cosine_similarity(df)

    user_similarity_scores = similarity_matrix[user_indices].mean(axis=0)

    # Create a DataFrame with owner indices and their similarity scores
    similarity_df = pd.DataFrame({'Owner': df['Owner'], 'Similarity': user_similarity_scores})

    # Sort the DataFrame by similarity scores in descending order
    sorted_similarity_df = similarity_df.sort_values(by='Similarity', ascending=False)
   
    # Exclude the user's own indices
    sorted_similarity_df = sorted_similarity_df[sorted_similarity_df['Owner']!= unique_value_user['Owner'][username]]

    top_10_recommendations = sorted_similarity_df.head(10)


    # Display the recommendations
    return [unique_value_ref[owner] for owner in sorted_similarity_df.Owner.unique()[:10]]


def top10_user_recommedation(username, mycursor):

    similarity_user = get_similarity(username, mycursor)

    query = f"""SELECT User_Name, Login, Public_Repos, Avatar_url, Profile_url FROM user_details 
                WHERE Login IN {tuple(similarity_user)};"""
    
    mycursor.execute(query)
    data= mycursor.fetchall()
    recommend = pd.DataFrame(data, columns=[i[0] for i in mycursor.description])
    
    return recommend


def recommendation_details(df):

    userdetails = []
    for i in range(9):
        url = df['Avatar_url'].iloc[i]
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        encoded_img = 'data:image/png;base64,' + base64.b64encode(img_bytes.getvalue()).decode()
        image = html.Img(src=encoded_img, style={'width': '90%', 'height': '80%'})
        userdetails.append(image)

    for i in range(9):
        profile = [dcc.Markdown(f'#### ***Top {i+1} User Details***', style = {'color': '#4090F5'}),
                  dcc.Markdown(f''' > User Name : {df.User_Name.iloc[i]}
                                \n > Login Name :{df.Login.iloc[i]}
                                \n > Repo Count : {df.Public_Repos.iloc[i]}
                                \n > [View Profile on Github]({df.Profile_url.iloc[i]})''', style = {'color': '#4090F5',})]
               
        userdetails.append(profile)

    return userdetails
