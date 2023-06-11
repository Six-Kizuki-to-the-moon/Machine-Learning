from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
import pandas as pd

def rec_similarItem(destinations_df, destination_name, n_item = 5):
    # new variable for content based filtering 
    place_id = destinations_df['id'].unique().tolist()
    place_name = destinations_df['name_wisata'].unique().tolist()
    place_category = destinations_df['category'].tolist()
    
    # dictionary for data_content
    data_content = pd.DataFrame({
        'place_id' : place_id,
        'place_name' : place_name,
        'place_category' : place_category
    })
    
    tfidf= TfidfVectorizer()
    tfidf.fit(data_content['place_name'])
    
    # change data into matrix 
    tfidf_matrix = tfidf.fit_transform(data_content['place_name'])
    
    # change vector TF-IDF into matrix 
    tfidf_matrix.todense() 
    
    # calculate the cosine similairty between the place name and each entry in 
    result_cosine_similarity = cosine_similarity(tfidf_matrix)
    
    df_cosine_similarity = pd.DataFrame(result_cosine_similarity, index = data_content['place_name'], columns = data_content['place_name'])
    
    # recommendation function for content based filtering 

    def content_rec(place_name, similarity_data = df_cosine_similarity, items = data_content[['place_name', 'place_category']], k = 5):
        index = similarity_data.loc[:, place_name].to_numpy().argpartition(range(-1, -k, -1))

        closest = similarity_data.columns[index[-1:-(k+2): -1]]
        closest = closest.drop(place_name, errors = 'ignore')

        return pd.DataFrame(closest).merge(items).head(k)
    
    result = content_rec(destination_name)
    
    destinations_df = destinations_df.rename(columns={'name_wisata' : 'place_name'})
    
    merged_df = pd.merge(result, destinations_df, on='place_name')
    
    return merged_df.to_dict(orient='records')
    
    