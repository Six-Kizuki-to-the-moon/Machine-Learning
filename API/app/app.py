# library bawaan yang dibutuhkan
# from flask import Flask, jsonify, request, make_response
from fastapi import FastAPI, Request, Response, Form
# import uvicorn
from pydantic import BaseModel

# import numpy as np
import pandas as pd
import mysql.connector
from datetime import datetime

# module dari model machine learning yang sudah dibuat
from model.recomendation_collab import recomendation 
from model.recomendation_category import recommend_places
from model.recomendation_similarItem import rec_similarItem

# Membuat koneksi ke database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='tourista_db' 
)

# Mengeksekusi query untuk mengambil data dari tabel

query = "SELECT * FROM destination"
destination = pd.read_sql_query(query, conn)

query = "SELECT * FROM review_wisata"
ratings = pd.read_sql_query(query, conn)

query = "SELECT * FROM user_profile"
users = pd.read_sql_query(query, conn)

app = FastAPI()
# app = Flask(__name__)

# Endpoint untuk route "/"
# menerima data menggunakan x-www-form-urlencoded
@app.get("/")
def home():
    data = {
        'message': 'API tourista already running, for documentation can direct on github',
        "github": "https://github.com/Six-Kizuki-to-the-moon/Machine-Learning/tree/main/API",
        'status': 'success',
        'error': False
    }
    return data

# Endpoint untuk route "/recommendCollab"
# menerima data menggunakan x-www-form-urlencoded
@app.post("/recommendCollab")
def recommendCollab(user_id: int = Form(...), user_lat: float = Form(...), user_long: float = Form(...)):
    # if input.headers.get("Content-Type") != 'application/x-www-form-urlencoded':
    #     response = {
    #         'status': 'fail',
    #         'message': 'Content-Type harus application/x-www-form-urlencoded'
    #     }
    #     raise HTTPException(status_code=404, detail=response)

    # Mendapatkan data input dari body request
    user_id =  input.user_id
    user_lat = input.user_lat
    user_long = input.user_long

    # memanggil fungsi dari model yang sudah dibuat
    recommendations = recomendation(destination, ratings, user_id, user_lat, user_long)

    data = {
        'recommendations': recommendations,
        'status': 'success',
    } 

    # Mengembalikan hasil rekomendasi sebagai respons JSON
    return data


class ContentBased(BaseModel):
    user_id: int
    category: str
    city: str
    price: int

# Endpoint untuk route "/recommendContentBased"
# menerima data menggunakan x-www-form-urlencoded
@app.post("/recommendContentBased")
def recommendContent(user_id: int = Form(...), category: str = Form(...), city: str = Form(...), price: int = Form(...)):
    # if input.headers.get("Content-Type") != 'application/x-www-form-urlencoded':
    #     response = {
    #         'status': 'fail',
    #         'message': 'Content-Type harus application/x-www-form-urlencoded'
    #     }
    #     raise HTTPException(status_code=404, detail=response)

    # Mendapatkan data input dari body request  
    user_id = input.user_id
    category = input.category
    city = input.city
    price = input.price

    # memanggil fungsi dari model yang sudah dibuat
    recommendations = recommend_places(destination, category, city, price, 4)

    cursor = conn.cursor()
    
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # syntax sql 
    sql = "INSERT INTO trip_detail (user_id , trip_name_type, name_wisata, createdAt) VALUES (%s, %s, %s, %s)"
    for category, places in recommendations.items():
        for place in places:
            values = (user_id, category, place, current_datetime)
            cursor.execute(sql, values)
            
    conn.commit()
    
    cursor.close()
    
    data = {
        'status': 'success',
    } 

    # Mengembalikan hasil rekomendasi sebagai respons JSON
    return data

# Endpoint untuk route "/recommendSimilarItem"
# menerima data menggunakan x-www-form-urlencoded
@app.post("/recommendSimilarItem")
def recommendSimilarItem(destination_name: str = Form(...)):
    # Mendapatkan data input dari body request
    # if input.headers.get("Content-Type") != 'application/x-www-form-urlencoded':
    #     response = {
    #         'status': 'fail',
    #         'message': 'Content-Type harus application/x-www-form-urlencoded'
    #     }
    #     raise HTTPException(status_code=404, detail=response)
    
    # memanggil fungsi dari model yang sudah dibuat
    recommendations = rec_similarItem(destination, destination_name)

    data = {
    'recommendations': recommendations,
    'status': 'success',
    } 

    # Mengembalikan hasil rekomendasi sebagai respons JSON
    return data