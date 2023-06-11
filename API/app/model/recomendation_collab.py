import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split 
from tensorflow.keras.models import Model 

import os

# calculations for "haversine distance" and complementary functions for collaborative filtering
from math import radians

def recomendation(destination, ratings, user_id, user_lat, user_long, np_val = 5):
    ratings = ratings.sort_values('wisata_rating', ascending=False).drop_duplicates(subset=['wisata_id', 'user_wisata'], keep='first')
    
    train, test = train_test_split(ratings, test_size = 0.2)
    
    # Load pre-trained model
    model = tf.keras.models.load_model('API\ml-dev\pretrained_collab_rec')
    
    early_stopping = EarlyStopping(patience=5, restore_best_weights=True)
    model.compile(optimizer=Adam(learning_rate = 0.0005), loss='mean_squared_error') 
    
    model.fit(x= [train.wisata_id, train.user_wisata], 
                    y= train.wisata_rating, 
                    validation_data = ([train.wisata_id, train.user_wisata], train.wisata_rating), 
                    epochs =5,
                    verbose = False,
                    callbacks=[early_stopping])
    
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
    
    # recommendation system function using collaborative filtering
    def collaborative_rec(User_Id, destination ,model, u_lat, u_long, np_val = 6 ):
        """
            User_Id : untuk melakukan rekomendasi berdasarkan User_Id yang diberikan
            destinatin : dataframe dengan format column terdapat "user_wisata, wisata_id, wisata_rating, name_wisata, category, description_wisata, destination_lat, destination_long, destination_photo, city"
            model : model hasil yang sudah di training sebelumnya
            np_val : banyaknya output yang akan diberikan
            u_lat & u_long : berguna untuk menentukan destinasi wisata terdekat dari lat & long yang diberikan
        """
    
        if User_Id in ratings['user_wisata'].values:
            destination = destination.copy()
            user_ids = np.array([User_Id] * len(destination))
            results = model([destination.id.values, user_ids]).numpy().reshape(-1)

            destination['predicted_rating'] = pd.Series(results)
            destination = filter_by_location(destination, u_lat, u_long, 30)[:20]
            destination = destination.sort_values('predicted_rating', ascending = False)
        else:
            destination = destination.copy()
            destination = filter_by_location(destination, u_lat, u_long, 30)[:20]
            destination = destination.sort_values('rating', ascending = False)  
            
        return destination[:np_val].to_dict(orient='records')
    
    
    recommendations = collaborative_rec(int(user_id), destination, model, user_lat, user_long, np_val)
    
    return recommendations