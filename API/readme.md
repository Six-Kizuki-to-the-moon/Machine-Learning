# Machine Learning Deployment
Built using FLASK

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
| `category`       | `string` | Required |
| `city`   | `string` | Required |
| `price`   | `int` | Required |
| `rating`   | `float` | Required |
| `lat`   | `float` | Required |
| `long`   | `float` | Required |

### **Collaborative Filtering**
#### POST

```http
  POST /recommendCollab
```

| Payloads     | Type     | Info    |
| :----------- | :------- | :------- | 
| ` user_id`       | `string` | Optional |
| `detail_user`   | `string` | Optional |
