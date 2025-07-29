# Sentiment Based Product Recommendation System

This project was undertaken as part of the Capstone Project for the Post Graduate Program in AI/ML. It is set in the context of an e-commerce company offering products across a wide range of categories. Users of the platform share ratings and reviews for the products they purchase. The primary objective of the project is to develop a recommendation system that suggests products aligned with user preferences. The recommendations aim to prioritize products that have received positive sentiment in reviews from other users.

## Project Plan

To achieve a sentiment-based product recommendation system identified the following key tasks:

- Sourcing data and performing sentiment analysis

- Building a product recommendation engine

- Enhancing the recommendations using insights from the sentiment analysis model

- Deploying the end-to-end solution with a simple user-friendly interface

## Repository Content

1. **`development/`** – This folder contains the Jupyter notebooks used during the development of the recommendation engine and sentiment analysis model. It also includes the input datasets, intermediate processed data, and the trained models.

    - **input-data** - This folder contains the input CSV used to train the recommendation engine and the sentiment analysis model.
    - **interim-data** - This folder contains the clean data in the (.pkl) format. This clean data is used to train and evaluate the Sentiment Models built using ML Algorithms for NLP. This data is also leveraged to train and evaluate the User-User and Item-Item similarity based recommendation model.
    - **models** - This folder contains all the different models built for Sentiment Analysis and Recommendation System.

> Note: Note: Because GitHub restricts file uploads larger than 100MB, the models generated using Random Forest and XGB have not been included in this repository. Only the smaller model obtained using Logistic Regression is provided.

2. **`modelservice.py`** – This file defines the `Model` class, which serves as a wrapper around both the User-Based Recommendation logic and the Sentiment Analyzer. It first identifies products purchased by similar users, then analyzes the sentiment of existing reviews for those products, filters them based on sentiment scores, and finally recommends the top 5 products to the user.

3. **`app.py`** – Acts as the bridge between the backend (`modelservice.py`) and the frontend. It exposes the `/results` endpoint, which invokes the model, retrieves the recommendations, and displays them on the user interface.

4. **`templates/`** – A required directory in Flask where all HTML files must be stored. It contains the HTML templates rendered by the frontend.


## System Development 

1. **Sentiment Analysis Model**: This model focuses on identifying the sentiment expressed in product reviews from the input data. Natural Language Processing (NLP) techniques are used to preprocess the text by removing stop words, punctuation, and other noise, followed by lemmatization. The cleaned and lemmatized text is then transformed into numerical features using a TF-IDF vectorizer. These features are subsequently used to train various machine learning models for sentiment classification.

2. **Recommendation Engine Model**: This model analyzes user preferences and item similarities within the product catalog. By evaluating both user-to-user and item-to-item similarities, the algorithm recommends products that are closely related to those previously purchased by the user.

### Deployment to Render.com

1. With the transition of [https://heroku.com](https://heroku.com) to a paid service, we opted to deploy the application using [https://render.com](https://render.com) as an alternative hosting platform.

2. The live application can be accessed at: [https://product-recommendation-app-ougv.onrender.com](https://product-recommendation-app-ougv.onrender.com)

3. Please note that Render.com puts inactive applications into sleep mode. As a result, the initial request to the above URL may take up to 5 minutes to wake the server and generate a response.