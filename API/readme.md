# Machine Learning Deployment
Buil using FLASK

## Endpoint

### **Home**
#### GET

```http
  GET /
```

| Arguments | Output              |
| :-------- | :------------------ |
| none     | API is running  |

### **Content Based Filtering**
#### POST

```http
  POST /recommendContent
```

| Payloads     | Type     | Info    |
| :----------- | :------- | :------- | 
| `category`       | `string` | 
| `city`   | `string` | 
| `price`   | `int` | 
| `rating`   | `float` | 
| `lat`   | `float` | 
| `long`   | `float` | 

### **Collaborative Filtering**
#### POST

```http
  POST /recommendCollab
```

| Payloads     | Type     | Info    |
| :----------- | :------- | :------- | 
| ` user_id`       | `string` | Optional |
| `detail_user`   | `string` | Optional |
