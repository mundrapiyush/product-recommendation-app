# Create a Python class to serve as a model service for product recommendations
import pickle
import pandas as pd

# Load the user-based recommendation model
USER_BASED_RECOMMENDATION_FILE = 'development/interim-data/user_based_recommendation.pkl'
ITEM_BASED_RECOMMENDATION_FILE = 'development/interim-data/item_based_recommendation.pkl'
CLEANED_DATA_FILE = 'development/interim-data/cleaned_data.pkl'
class ModelService:
    def __init__(self):

        with open(USER_BASED_RECOMMENDATION_FILE, 'rb') as file:
            self.user_based_recommendations = pickle.load(file)
        
        with open(ITEM_BASED_RECOMMENDATION_FILE, 'rb') as file:
            self.item_based_recommendations = pickle.load(file)
        
        with open(CLEANED_DATA_FILE, 'rb') as file:
            self.master_data = pickle.load(file)

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