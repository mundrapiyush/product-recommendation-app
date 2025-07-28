# Create a Python class to serve as a model service for product recommendations
import pickle
import pandas as pd

class ModelService:
    def __init__(self):
        # Load the user-based recommendation model
        with open('development/interim-data/user_based_recommendation.pkl', 'rb') as file:
            self.user_based_recommendations = pickle.load(file)
        
        # Load the item-based recommendation model
        with open('development/interim-data/item_based_recommendation.pkl', 'rb') as file:
            self.item_based_recommendations = pickle.load(file)
        
        # Load the cleaned data DataFrame
        with open('development/interim-data/cleaned_data.pkl', 'rb') as file:
            self.master_data = pickle.load(file)

    # Function to get top N recommendations for a user based on item similarity
    def get_top_n_recommendations_based_on_item(self, username, n=5):
        # Get the user's predicted ratings
        item_recommendations = self.item_based_recommendations[username]
        
        # Sort the ratings in descending order and get the top N recommendations
        top_n_recommendations = item_recommendations.sort_values(ascending=False).head(n)
        
        # Get the brand IDs and their corresponding names
        top_n_brands = self.master_data[self.master_data['reviews_username'] == username]['manufacturer_brand_name'].unique()
        
        return top_n_recommendations, top_n_brands

    # Function to get top N recommendations for a user based on user similarity
    def get_top_n_recommendations_based_on_user(self, username, n=5):
        # Get the user's predicted ratings
        user_recommendations = self.user_based_recommendations.loc[username]
        
        # Sort the ratings in descending order and get the top N recommendations
        top_n_recommendations = user_recommendations.sort_values(ascending=False).head(n)
        
        # Get the brand IDs and their corresponding names
        top_n_brands = self.master_data[self.master_data['reviews_username'] == username]['manufacturer_brand_name'].unique()
        
        return top_n_recommendations, top_n_brands