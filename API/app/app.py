# library bawaan yang dibutuhkan
from flask import Flask, jsonify, request, make_response
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

# rout untuk menerima data menggunakan x-www-form-urlencoded
@app.route('/process', methods=['POST'])
def process():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        # Mendapatkan nilai dari body permintaan
        user_id = request.form.get('user_id')
        # Melakukan pemrosesan data
        processed_data = user_id.upper()
        # Membuat respons JSON
        response = {
            'status': 'success',
            'message': 'Data berhasil diproses',
            'processed_data': processed_data
        }
        return jsonify(response)
    else:
        response = {
            'status': 'fail',
            'message': 'Content-Type harus application/x-www-form-urlencoded'
        }
        return jsonify(response), 400

# Endpoint untuk route "/"
# menerima data menggunakan x-www-form-urlencoded
@app.route("/", methods=["GET"])
def home():
    data = {
        'message': 'API tourista already running, for documentation can direct on github',
        "github": "https://github.com/Six-Kizuki-to-the-moon/Machine-Learning/tree/main/API",
        'status': 'success',
        'error': False
    }
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json'
    response.headers['Custom-Header'] = 'Custom Value'
    response.status_code = 200
    return response

# Endpoint untuk route "/recommendCollab"
# menerima data menggunakan x-www-form-urlencoded
@app.route("/recommendCollab", methods=["POST"])
def recommendCollab():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        # Mendapatkan data input dari body request
        user_id =  int(request.form.get("user_id"))
        city_user =  str(request.form.get("city_user"))
    
        # memanggil fungsi dari model yang sudah dibuat
        recommendations = recomendation(destination, ratings, user_id, city_user)
    
        data = {
            'recommendations': recommendations,
            'status': 'success',
        } 
    
        response = make_response(jsonify(data))
    
        # Mengembalikan hasil rekomendasi sebagai respons JSON
        return response
    else:
        response = {
            'status': 'fail',
            'message': 'Content-Type harus application/x-www-form-urlencoded'
        }
        return jsonify(response), 400

# Endpoint untuk route "/recommendContentBased"
# menerima data menggunakan x-www-form-urlencoded
@app.route("/recommendContentBased", methods=["POST"])
def recommendContent():
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        # Mendapatkan data input dari body request  
        category = str(request.form.get('category'))
        city = str(request.form.get('city'))
        price = int(request.form.get('price'))
        rating = float(request.form.get('rating'))
    
        # memanggil fungsi dari model yang sudah dibuat
        recommendations = recommend_places(destination, category, city, price, rating)
    
        data = {
            'recommendations': recommendations,
            'status': 'success',
        } 
    
        response = jsonify(data)
    
        # Mengembalikan hasil rekomendasi sebagai respons JSON
        return response
    else:
        response = {
            'status': 'fail',
            'message': 'Content-Type harus application/x-www-form-urlencoded'
        }
        return jsonify(response), 400

# Endpoint untuk route "/recommendSimilarItem"
# menerima data menggunakan x-www-form-urlencoded
@app.route("/recommendSimilarItem", methods=["POST"])
def recommendSimilarItem():
    # Mendapatkan data input dari body request
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        destination_name = str(request.form.get('destination_name'))
     
        # memanggil fungsi dari model yang sudah dibuat
        recommendations = rec_similarItem(ratings, destination, users, destination_name)
    
        data = {
        'recommendations': recommendations,
        'status': 'success',
    } 
    
        response = make_response(jsonify(data))
    
        # Mengembalikan hasil rekomendasi sebagai respons JSON
        return response
    else:
        response = {
            'status': 'fail',
            'message': 'Content-Type harus application/x-www-form-urlencoded'
        }
        
        return jsonify(response), 400

# Error handler response
@app.errorhandler(404)
def page_not_found(error):
    data = {
        'message': 'Route not found',
        'status': 'fail',
        'error': True
    }
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 404
    return response

@app.errorhandler(405)
def methd_not_found(error):
    data = {
        'status': 'fail', 
        'message': 'Unsupported request method'
    }
    
    response = make_response(jsonify(data))
    
    return response

if __name__ == "__main__":
    app.run(debug=True)