#  library yang dibutuhkan
from sklearn.metrics.pairwise import cosine_similarity

# fungsi untuk melakukan groouping data
def groupingCategory(df, budget, totalCategory, excepts = []):
        data = []

        if len(excepts) == 0:
            for idx, row in df.iterrows():
                if len(data) == totalCategory:
                    break
                if row['Price'] < budget:
                    data.append(row['Place_Id'])
                    budget -= row['Price']    
        else:
            for x in excepts:
                if df['Place_Id'].eq(x).any():
                    df = df.loc[df['Place_Id'] != x]

            for idx, row in df.iterrows():
                if len(data) == totalCategory:
                    break
                if row['Price'] < budget:
                    data.append(row['Place_Id'])
                    budget -= row['Price']

        return data
    
# fungsi untuk merekomendasikan tempat wisata berdasarakan input user
def recommend_places(df, category, city, price, rating, lat, long, top_n=50):
    # Filter dataset based on user input
    filtered_df = df[(df['Category'] == category) & (df['City'] == city) & (df['Price'] <= price) & (df['Rating'] >= rating)]

    # Calculate cosine similarity between user input and dataset
    user_input = [[price, rating, lat, long]]
    dataset = filtered_df[['Price', 'Rating', 'Lat', 'Long']]
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

    return {"gold": gold, "silver": silver, "bronze": bronze}