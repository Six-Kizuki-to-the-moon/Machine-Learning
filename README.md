# Machine-Learning
This repository is used to create travel recommendation systems based on user preferences

# Resource
- Dataset : The first step we do is clean the dataset we got from <a href="https://www.kaggle.com/datasets/aprabowo/indonesia-tourism-destination">Indonesia Tourism Destination</a> that we will use and then we save it in the dataset folder in this repository. 
- Model : We creating the three models with using <a href="https://www.tensorflow.org/">Tensorflow</a>, <a href="https://scikit-learn.org/">Sklearn</a> technology.
    - Content Based Filtering, for giving best preference based on user input such as category, city, and price. {<a href="https://github.com/Six-Kizuki-to-the-moon/Machine-Learning/blob/main/model/recomendation_category.ipynb">model1</a>, <a href="https://github.com/Six-Kizuki-to-the-moon/Machine-Learning/blob/main/model/recomendation_similarItem.ipynb">model2</a>}
    - Collaborative filtering, for giving recomendations based on ratings user on every destination {<a href="https://github.com/Six-Kizuki-to-the-moon/Machine-Learning/blob/main/model/recomendation_collab.ipynb">model3</a>}

# About Member Machine Learning Path 
| Name                       | Student ID  | Social Media     |
|----------------------------|------------ |------------------|
| Mochammed Daffa El Ghifari | M181DKX4080 | <a href="https://www.linkedin.com/in/daffa-el-ghifari-b05377208/">![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)</a> |
| Dewa Putra Hernanda        | M131DSX0533 | <a href="https://www.linkedin.com/in/dewa-putra-hernanda-147a99202/">![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)</a> |
| Fadhila Salsabila          | M038DSY2929 |  <a href="https://www.linkedin.com/in/fadhilasalsabila/">![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)</a> |

# Documentation
- API folder contains model Machine Learning & FLASK
    - For model machine learing on this folder we used mysql to read the dataset
- dataset folder contains cleaned data for synchronizing the database from <a href="https://github.com/Six-Kizuki-to-the-moon/tourista-api">Cloud Computing</a>
- model folder contain model machine learning for recomendation system
- file data_cleaning_visualization.ipynb for see the visualization results to get better understanding of the data that we used.

# Model explanation
## Recomendation Collab 
This <a href="https://github.com/Six-Kizuki-to-the-moon/Machine-Learning/blob/main/model/recomendation_collab.ipynb">model</a> focuses on **rating predictions** for users based on their ratings of other destinations and provides the closest tourist destinations by implementing the "haversine distance" method.
- On the training process, we got the best graph with loss: 0.5242 - val_loss: 0.0807
    
    ![TrainValGraph!](/resource/TrainValGraph.png "TrainValGraph")

- Because we will train again this model on flask API with fewer epochs so we create **pre-trained model** 
for making faster computation & optimal result

    | Type                       | Ephocs  | time       | result                         |
    |----------------------------|---------|------------|--------------------------------|
    | Without pre-trained        | 200     | 2m,7.5s    |loss: 0.5242 - val_loss: 0.0807 |
    | With pre-trained           | 10      | 3.4s       |loss: 0.9272 - val_loss: 0.4587 |

- This model will be implemented on "Destination near you" section

    ![Implementation!](/resource/Recomendation_collab_implementation.png "Implementation")

## Recomendation Similar Item
This <a href="https://github.com/Six-Kizuki-to-the-moon/Machine-Learning/blob/main/model/recomendation_similarItem.ipynb">model</a> focusing for giving **similar item destination** after user click or open the detail destination.
- On this model we just using Mathematics like **cosine similarity** for getting similar item between place_name & place_category
- This model will be implemented on "Another options for you"

    ![Implementation!](/resource/RecomendationSimilarItem_implementation.png "Implementation")

## Recomendation Category
This <a href="https://github.com/Six-Kizuki-to-the-moon/Machine-Learning/blob/main/model/recomendation_category.ipynb">model</a> focusing to give the best destination from user preferences such as { Category, City, and Price } and after that will give the 3 options {Gold, Silver, Bronze} with 5 destinations on every options.
- First, our model will filtering category, city, price, and rating from the database, based on user preferences 
- After that on this model we just using Mathematics like **cosine similarity** for getting similar item between price & rating
- This model will be implemented on "Explore {Main Features}"

    ![Implementation!](/resource/Recomendation_Category_implementation.png "Implementation")
    ![Implementation!](/resource/Recomendation_Category_implementation2.png "Implementation")