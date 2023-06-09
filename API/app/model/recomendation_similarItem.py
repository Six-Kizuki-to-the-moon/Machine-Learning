from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
import pandas as pd

def rec_similarItem(ratings, destinations, users, destination_name, n_item = 5):
    # merge rating dataset with destination dataset on Place_Id column 
    full = pd.merge(ratings, destinations[['Place_Id', 'Place_Name', 'Category', 'Description']], on = 'Place_Id',
                        how = 'left')

    # merge full dataset (destination & rating) with user dataset (age's column)
    merged_df = pd.merge(full, users, on='User_Id')

    # sort merged_df by Place_Id
    merged_df = merged_df.sort_values('Place_Id')
    # drop duplicates 
    merged_df = merged_df.sort_values('Place_Id', ascending = True).drop_duplicates(subset = ['Place_Id', 'User_Id'])
    
    # new variable for content based filtering 
    place_id = destinations['Place_Id'].unique().tolist()
    place_name = destinations['Place_Name'].unique().tolist()
    place_category = destinations['Category'].tolist()
    
    # dictionary for place_recommend
    place_recommend = pd.DataFrame({
    'place_id' : place_id,
    'place_name' : place_name,
    'place_category' : place_category
    })
    
    # data frame for content based filtering 
    data_content = place_recommend
    
    tfidf= TfidfVectorizer()
    tfidf.fit(data_content['place_name'])
    
    # change data into matrix 
    tfidf_matrix = tfidf.fit_transform(data_content['place_name'])
    
    # change vector TF-IDF into matrix 
    tfidf_matrix.todense()
    
    # calculate the cosine similairty between the place name and each entry in 
    result_cosine_similarity = cosine_similarity(tfidf_matrix)
    
    df_cosine_similarity = pd.DataFrame(result_cosine_similarity, index = data_content['place_name'], columns = data_content['place_name'])
    
    items = data_content[['place_id','place_name', 'place_category']]
    index = df_cosine_similarity.loc[:, destination_name].to_numpy().argpartition(range(-1, -n_item, -1))
    
    closest = df_cosine_similarity.columns[index[-1:-(n_item+2): -1]]
    closest = closest.drop(destination_name, errors = 'ignore')
    
    result = pd.DataFrame(closest).merge(items).head(n_item)
    
    return result['place_id'].tolist()