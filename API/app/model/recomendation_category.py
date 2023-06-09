#  library yang dibutuhkan
from sklearn.metrics.pairwise import cosine_similarity

# fungsi untuk melakukan groouping data
def groupingCategory(df, budget, totalCategory, excepts = []):
    data = []
    
    if len(excepts) == 0:
        for idx, row in df.iterrows():
            if len(data) == totalCategory:
                break
            if row['price'] < budget:
                data.append(row['name_wisata'])
                budget -= row['price']    
    else:
        for x in excepts:
            if df['name_wisata'].eq(x).any():
                df = df.loc[df['price'] != x]
                
        for idx, row in df.iterrows():
            if len(data) == totalCategory:
                break
            if row['price'] < budget:
                data.append(row['name_wisata'])
                budget -= row['price']
        
    return data
    
# Function to recommend places based on user input
def recommend_places(df, category, city, price, rating, top_n=50):
    # Filter dataset based on user input
    filtered_df = df[(df['category'] == category) & (df['city'] == city) & (df['price'] <= price) & (df['rating'] >= rating)]
    
    # Calculate cosine similarity between user input and dataset
    user_input = [[price, rating]]
    dataset = filtered_df[['price', 'rating']]
    similarity_matrix = cosine_similarity(user_input, dataset)
    
    # Sort places based on similarity score
    filtered_df['Similarity'] = similarity_matrix[0]
    recommended_places = filtered_df.sort_values(by='Similarity', ascending=False).head(top_n)
    
    gold = []
    silver = []
    bronze = []
    
    gold = groupingCategory(recommended_places, price, 5)
    silver = groupingCategory(recommended_places, price, 5, gold)
    bronze = groupingCategory(recommended_places, price, 5, (silver + gold))
                
    return {"gold" : gold,
            "silver" : silver, 
            "bronze" : bronze}