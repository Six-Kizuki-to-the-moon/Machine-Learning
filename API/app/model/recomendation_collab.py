import numpy as np
import pandas as pd
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split 
from tensorflow.keras.models import Model 

# calculations for "haversine distance" and complementary functions for collaborative filtering
from math import radians

def recomendation(destination, ratings, user_id, user_lat, user_long, np_val = 5):
    # pre processing dataset
    number_user = len(ratings['user_wisata'].unique())
    number_destination = len(ratings['wisata_id'].unique())
    train, test = train_test_split(ratings, test_size = 0.2)
    
    EMBEDDING_DIM = 50

    # input layers 
    place_input = Input(shape=[1])
    user_input = Input(shape=[1])

    # embedding layers add dropout 
    place_embedding = Embedding(number_destination+1 , EMBEDDING_DIM)(place_input)
    place_embedding = Dropout(0.2)(place_embedding)

    user_embedding = Embedding(number_user+1 , EMBEDDING_DIM)(user_input)
    user_embedding = Dropout(0.2)(user_embedding)

    # flatten the embedddings
    place_flat = Flatten()(place_embedding)
    user_flat = Flatten()(user_embedding)

    # output layer
    output = Dot(1)([place_flat, user_flat])

    # the model
    model = Model([place_input, user_input], [output])
    
    early_stopping = EarlyStopping(patience=5, restore_best_weights=True)
    model.compile(optimizer=Adam(learning_rate = 0.0005), loss='mean_squared_error') 
    
    history = model.fit(x= [train.wisata_id, train.user_wisata], 
                    y= train.wisata_rating, 
                    validation_data = ([train.wisata_id, train.user_wisata], train.wisata_rating), 
                    epochs =25,
                    callbacks=[early_stopping],
                    verbose=0)
    
    def haversine_distance(lat1, long1, lat2, long2):
        earth_radius = 6371  # Radius of the Earth in kilometers (source: google)
        lat1_rad = np.radians(lat1)
        long1_rad = np.radians(long1)
        lat2_rad = np.radians(lat2)
        long2_rad = np.radians(long2)
        diff_lat = lat2_rad - lat1_rad
        diff_long = long2_rad - long1_rad
        a = np.sin(diff_lat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(diff_long / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        distance = earth_radius * c
        return distance

    def filter_by_location(destination, user_lat, user_long, max_distance):
        destination['distance'] = haversine_distance(destination['destination_lat'], destination['destination_long'], user_lat, user_long)
        destination = destination[destination['distance'] <= max_distance]
        destination = destination.drop('distance', axis=1)
        return destination

    def filter_by_city(destination):
        city_filter = ['Jakarta', 'Bandung', 'Yogyakarta', 'Semarang', 'Surabaya']
        destination = destination[destination['city'].isin(city_filter)]
        return destination

    # recommendation system function using collaborative filtering
    def collaborative_rec(User_Id, destination ,model, np_val, user_lat, user_long ):
        # detail user : digunakan untuk menyimpan data detail user untuk mengerucutkan data yang akan di outputkan
    
        if User_Id in ratings['user_wisata'].values:
                destination = destination.copy()
                user_ids = np.array([User_Id] * len(destination))
                results = model([destination.Place_Id.values, user_ids]).numpy().reshape(-1)

                destination['predicted_rating'] = pd.Series(results)
                destination = destination.sort_values('predicted_rating', ascending = False)
        else:
                destination = destination.copy()
                destination = destination.sort_values('rating', ascending = False)

        # if user_location != 'None':
        #     destination = destination[destination['city'] == user_location]

        dataFinal = filter_by_location(destination, user_lat, user_long, 30)
    
        dataFinal = destination[:np_val]
        return dataFinal[['name_wisata', 'city', 'destination_photo','description_wisata']].to_dict(orient='records')
    
    recommendations = collaborative_rec(user_id, destination, model, np_val, user_lat, user_long)
    
    return recommendations