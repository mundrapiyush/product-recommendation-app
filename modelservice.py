# Create a Python class to serve as a model service for product recommendations
import pickle
import pandas as pd
import pickle

# Load the user-based recommendation model
CLEANED_DATA_FILE = 'development/interim-data/cleaned_data.pkl'
VECTORIZED_REVIEWS_FILE = 'development/interim-data/tfidf_data.pkl'
SENTIMENT_ANALYSIS_MODEL_FILE = 'development/models/lr_model_classifier.pkl'
USER_BASED_RECOMMENDATION_FILE = 'development/models/user_based_recommendation.pkl'
ITEM_BASED_RECOMMENDATION_FILE = 'development/models/item_based_recommendation.pkl'
class ModelService:
    def __init__(self):

        with open(USER_BASED_RECOMMENDATION_FILE, 'rb') as file:
            self.user_based_recommendations = pickle.load(file)
        
        with open(ITEM_BASED_RECOMMENDATION_FILE, 'rb') as file:
            self.item_based_recommendations = pickle.load(file)
        
        with open(CLEANED_DATA_FILE, 'rb') as file:
            self.master_data = pickle.load(file)

        with open(VECTORIZED_REVIEWS_FILE, 'rb') as file:
            self.vectorized_reviews = pickle.load(file)

        with open(SENTIMENT_ANALYSIS_MODEL_FILE, 'rb') as file:
            self.sentiment_analysis_model = pickle.load(file)

    # Function to get top N recommendations for a user based on item similarity
    def get_top_n_recommendations_based_on_item(self, username, n=5):
        
        # Check if the user exists in the user-based recommendations
        if username not in self.item_based_recommendations.index:
            return {}, []
        
        # Get the user's predicted ratings
        item_recommendations = self.item_based_recommendations[username]
        
        # Sort the ratings in descending order and get the top N recommendations
        top_n_recommendations = item_recommendations.sort_values(ascending=False).head(n)
        
        # Get the brand IDs and their corresponding names
        top_n_brands = self.master_data[self.master_data['reviews_username'] == username]['manufacturer_brand_name'].unique()
        
        return top_n_recommendations, top_n_brands

    # Function to get top N recommendations for a user based on user similarity
    def get_top_n_recommendations_based_on_user(self, username, n=5):
        
        # Check if the user exists in the user-based recommendations
        if username not in self.user_based_recommendations.index:
            return {}, []
        
        # Get the user's predicted ratings
        user_recommendations = self.user_based_recommendations.loc[username]
        
        # Sort the ratings in descending order and get the top N recommendations
        top_n_recommendations = user_recommendations.sort_values(ascending=False).head(n)
        
        # Get the brand IDs and their corresponding names
        top_n_brands = self.master_data[self.master_data['reviews_username'] == username]['manufacturer_brand_name'].unique()
        
        return top_n_recommendations, top_n_brands
    
    def get_top_productes_based_on_vectorized_reviews(self, top_n_recommendations):

        # Filter the clean_data_df to get the rows where the manufacturer_brand_name is in top_n_recommendations
        filtered_data_df = self.master_data[self.master_data['manufacturer_brand_name'].isin(top_n_recommendations.index)].copy()

        # Use the TF-IDF vectorizer to transform the reviews_lemmatized column in filtered_data_df
        X = self.vectorized_reviews.transform(filtered_data_df['reviews_lemmatized'].values.astype(str))
          
        # Use the trained logistic regression model to predict the sentiment for the reviews in filtered_data_df
        filtered_data_df.loc[:, 'predicted_sentiment'] = self.sentiment_analysis_model.predict(X)

        # Create a new column to map Positive sentiment to 1 and Negative sentiment to 0. This will allow us to easily summarize the data
        filtered_data_df.loc[:, 'positive_sentiment'] = filtered_data_df['predicted_sentiment'].apply(lambda x: 1 if x=="Positive" else 0)

        # Group by manufacturer_brand_name and get the percentage of positive sentiment
        filtered_data_with_sentiments_df = filtered_data_df.groupby('manufacturer_brand_name')['positive_sentiment'].mean().reset_index().sort_values(by='positive_sentiment', ascending=False)

        # Get the top 5 manufacturer_brand_name with highest positive sentiment
        top_5_products = filtered_data_with_sentiments_df.head(5).copy()

        # Split the manufacturer_brand_name value into manufacturer, brand, and name and use only the name for display
        top_5_products.loc[:, 'name'] = top_5_products['manufacturer_brand_name'].apply(lambda x: x.split(' # ')[-1])

        # Format the sentiment percentage for display
        top_5_products.loc[:, 'sentiment'] = top_5_products['positive_sentiment'].apply(lambda x: f"{x:.2%}")

        # Drop the unnecessary columns
        top_5_products.drop(columns=['manufacturer_brand_name', 'positive_sentiment'], inplace=True)
        top_5_products.reset_index(drop=True, inplace=True)

        return top_5_products