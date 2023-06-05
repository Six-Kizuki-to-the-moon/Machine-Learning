# Machine Learning Deployment
Built using FLASK

## Installation (run local)
Packages
```
pip install Flask 
pip install numpy
pip install pandas
pip install tensorflow
pip install scikit-learn
```
Note<br>
<ul>
  <li>Make sure you already installed <a href="[https://translate.google.com/?sl=en&tl=id&text=packages&op=translate](https://www.anaconda.com/download-success)">anaconda</a></li>
  <li>Make sure you already installed <a href="https://www.apachefriends.org/">xampp</a></li>
  <li>Download database on folder `/app/dataset/` and import on your xampp</li>
</ul>


## Endpoint

### **Home**
#### GET

```
  GET /
```

| Arguments | Output              |
| :-------- | :------------------ |
| none     | API is running  |

### **Content Based Filtering**
#### POST

```
  POST /recommendContent
```

| Payloads     | Type     | Info    |
| :----------- | :------- | :------- | 
| `category`       | `string` | Required |
| `city`   | `string` | Required |
| `price`   | `int` | Required |
| `rating`   | `float` | Required |
| `lat`   | `float` | Required |
| `long`   | `float` | Required |

### **Collaborative Filtering**
#### POST

```
  POST /recommendCollab
```

| Payloads     | Type     | Info    |
| :----------- | :------- | :------- | 
| ` user_id`       | `string` | Optional |
| `detail_user`   | `string` | Optional |
