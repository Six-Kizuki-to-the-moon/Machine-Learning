# library bawaan yang dibutuhkan
from flask import Flask, jsonify, request
# import numpy as np
import pandas as pd
import mysql.connector

# module dari model machine learning yang sudah dibuat
from model.recomendation_collab import recomendation 
from model.recomendation_category import recommend_places
from model.recomendation_similarItem import rec_similarItem


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

query = "SELECT * FROM users"
users = pd.read_sql_query(query, conn)

app = Flask(__name__)

# Endpoint untuk route "/"
@app.route("/", methods=["GET"])
def home():
    return "API tourista already to use baby!!!"

# Endpoint untuk route "/recommendCollab"
@app.route("/recommendCollab", methods=["POST"])
def recommendCollab():
    # Mendapatkan data input dari body request
    user_id = request.json.get("user_id", None)
    detail_user = request.json.get("detail_user", None)
    
    # memanggil fungsi dari model yang sudah dibuat
    recommendations = recomendation(destination, ratings, user_id, detail_user)
    
    # Mengembalikan hasil rekomendasi sebagai respons JSON
    return jsonify({"recommendations": recommendations})

# Endpoint untuk route "/recommendContentBased"
@app.route("/recommendContentBased", methods=["POST"])
def recommendContent():
    # Mendapatkan data input dari body request
    category = request.json['category']
    city = request.json['city']
    price = request.json['price']
    rating = request.json['rating']
    lat = request.json['lat']
    long = request.json['long']
    
    # memanggil fungsi dari model yang sudah dibuat
    recommendations = recommend_places(destination, category, city, price, rating, lat, long)
    
    # Mengembalikan hasil rekomendasi sebagai respons JSON
    return jsonify({"recommendations": recommendations})

# Endpoint untuk route "/recommendSimilarItem"
@app.route("/recommendSimilarItem", methods=["POST"])
def recommendSimilarItem():
    # Mendapatkan data input dari body request
    destination_name = request.json['destination_name']
    
    # memanggil fungsi dari model yang sudah dibuat
    recommendations = rec_similarItem(ratings, destination, users, destination_name)
    
    # Mengembalikan hasil rekomendasi sebagai respons JSON
    return jsonify({recommendations})

if __name__ == "__main__":
    app.run(debug=True)
