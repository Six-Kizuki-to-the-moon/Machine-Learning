from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from tensorflow.keras.models import Model 
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, Dense
from sklearn.model_selection import train_test_split 
from sklearn.metrics.pairwise import cosine_similarity

import mysql.connector

# Membuat koneksi ke database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='absensi'
)

# Mengeksekusi query untuk mengambil data dari tabel

query = "SELECT * FROM tourism"
destination = pd.read_sql_query(query, conn)

query = "SELECT * FROM ratings"
ratings = pd.read_sql_query(query, conn)

app = Flask(__name__)

# Endpoint untuk route "/"
@app.route("/", methods=["GET"])
def home():
    return "API is running"

# Endpoint untuk route "/recommendCollab"
@app.route("/recommendCollab", methods=["POST"])
def recommend():
    # Mendapatkan data input dari body request
    user_id = request.json.get("user_id", None)
    detail_user = request.json.get("detail_user", None)
    
    # pre processing dataset
    number_user = len(ratings['User_Id'].unique())
    number_destination = len(ratings['Place_Id'].unique())
    train, test = train_test_split(ratings, test_size = 0.2)
    
    # build recommendation system using emmbedding layers 
    EMBEDDING_DIM = 50
    
    # input layers 
    place_input = Input(shape=[1])
    user_input = Input(shape=[1])

    # embedding layers
    place_embedding = Embedding(number_destination+1 , EMBEDDING_DIM)(place_input)
    user_embedding = Embedding(number_user+1 , EMBEDDING_DIM)(user_input)

    # flatte the embedddings
    place_flat = Flatten()(place_embedding)
    user_flat = Flatten()(user_embedding)

    # add dense layers
    dense1 = Dense(64, activation='relu')(place_flat)
    dense2 = Dense(64, activation='relu')(user_flat)

    # output layer
    output = Dot(1)([dense1, dense2])

    # the model
    model = Model([place_input, user_input], [output])
    
    model.compile(loss = 'mean_squared_error', 
              optimizer = Adam(learning_rate = 0.0005)
              )
    
    model.fit(x= [train.Place_Id, train.User_Id], 
                    y= train.Place_Ratings, 
                    validation_data = ([test.Place_Id, test.User_Id], test.Place_Ratings), 
                    batch_size =32 , 
                    epochs =30)
    
    # recommendation system function using collaborative filtering
    def collaborative_rec(User_Id, destination ,model, np_val, detail_user):
        # detail user : digunakan untuk menyimpan data detail user untuk mengerucutkan data yang akan di outputkan
    
        if User_Id in ratings['User_Id'].values:
                destination = destination.copy()
                user_ids = np.array([User_Id] * len(destination))
                results = model([destination.Place_Id.values, user_ids]).numpy().reshape(-1)

                destination['predicted_rating'] = pd.Series(results)
                destination = destination.sort_values('predicted_rating', ascending = False)
        else:
                destination = destination.copy()
                destination = destination.sort_values('Rating', ascending = False)

        if detail_user != None:
            destination = destination[destination['City'] == detail_user]

        dataFinal = destination[:np_val]
        return dataFinal['Place_Id'].tolist()
    
    recommendations = collaborative_rec(user_id, destination, model, 5, detail_user)

    # Mengembalikan hasil rekomendasi sebagai respons JSON
    return jsonify({"recommendations": recommendations})

# Endpoint untuk route "/recommendContent"
@app.route("/recommendContent", methods=["POST"])
def recommendContent():
    # Mendapatkan data input dari body request
    category = request.json['category']
    city = request.json['city']
    price = request.json['price']
    rating = request.json['rating']
    lat = request.json['lat']
    long = request.json['long']
    
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

    # Function to recommend places based on user input
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
    
    recommendations = recommend_places(destination, category, city, price, rating, lat, long)
    
    return jsonify({"recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)