#importing pandas for data handling
import pandas as pd

#importing knowledge layer variables and functions
from .knowledge import region_sport_mapping, get_active_event_sports

#function to calculate the match score based on the required formula
def calculate_score(user_row, product_row, active_sports):
    #initialize score components
    user_match = 0.0
    regional_pop = 0.0
    event_boost = 0.0
    
    #user match logic (max 1.0)
    #checking if the sport matches
    if user_row['favorite_sport'] == product_row['sport']:
        user_match += 0.5
    #checking if the skill level matches or if the product is for everyone
    if user_row['skill_level'] == product_row['skill_level'] or product_row['skill_level'] == 'All':
        user_match += 0.5
        
    #regional popularity logic (max 1.0)
    #checking if the product's sport is the top sport in the user's city
    if region_sport_mapping.get(user_row['region']) == product_row['sport']:
        regional_pop = 1.0
        
    #event boost logic (max 1.0)
    #checking if there is a tournament happening for this sport right now
    if product_row['sport'] in active_sports:
        event_boost = 1.0
        
    #discount boost
    #since discounts live in the sales data, we use a default mock value here for the catalog
    #in a live system, you would join this with active marketing campaigns
    discount_boost = 0.8 
    
    #applying the exact weighted formula requested: 0.4 + 0.3 + 0.2 + 0.1
    final_score = (0.4 * user_match) + (0.3 * regional_pop) + (0.2 * event_boost) + (0.1 * discount_boost)
    
    #returning the rounded score
    return round(final_score, 3)

#function to get top 5 products for a specific user
def get_top_5(user_id, users_df, products_df, events_df, current_date):
    #extracting the specific user's profile from the dataframe
    user_data = users_df[users_df['user_id'] == user_id]
    
    #safety check in case user does not exist
    if user_data.empty:
        return None
        
    #getting the single row of user data
    user_row = user_data.iloc[0]
    
    #determining user country for global vs local event filtering
    indian_cities = ['Hyderabad', 'Delhi', 'Mumbai', 'Chennai', 'Bangalore']
    user_country = 'India' if user_row['region'] in indian_cities else 'UK'
    
    #getting the list of active sports from the knowledge layer
    active_sports = get_active_event_sports(events_df, current_date, user_country)
    
    #creating a copy of products to store our calculated scores safely
    scored_products = products_df.copy()
    
    #calculating the final score for every product row by row
    scored_products['final_score'] = scored_products.apply(
        lambda row: calculate_score(user_row, row, active_sports), 
        axis=1
    )
    
    #sorting the catalog by the highest score
    top_5_products = scored_products.sort_values(by='final_score', ascending=False).head(5)
    
    #returning only the most relevant columns for the streamlit dashboard
    return top_5_products[['product_id', 'name', 'category', 'sport', 'price', 'final_score']]