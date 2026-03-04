#mapping regions to their most popular sports for regional boost
region_sport_mapping = {
    'Hyderabad': 'Cricket',
    'Chennai': 'Badminton',
    'Mumbai': 'Gym',
    'Delhi': 'Cricket',
    'London': 'Football',
    'Bangalore': 'Cricket'
}

#mapping sports to their related product categories
sport_category_mapping = {
    'Cricket': ['Bat', 'Balls', 'Helmet', 'Jersey'],
    'Football': ['Shoes', 'Balls', 'Jersey', 'Accessory'],
    'Badminton': ['Racket', 'Shuttle', 'Kit'],
    'Gym': ['Gym Equipment']
}

#creating a function to evaluate the reasoning rules and return boost scores
def calculate_knowledge_boosts(user_region, user_sport, user_skill, product_sport, product_skill, active_events_list):
    #initializing boost score
    boost_score = 0.0
    
    #rule 1: user match (does the product match their favorite sport and skill)
    if user_sport == product_sport:
        #base match for the favorite sport
        boost_score += 0.2
        #checking skill level compatibility ('all' means it fits everyone, like a jersey)
        if user_skill == product_skill or product_skill == 'All':
            boost_score += 0.2
            
    #rule 2: regional popularity
    #if the product's sport is the most popular in the user's region
    if region_sport_mapping.get(user_region) == product_sport:
        boost_score += 0.3
        
    #rule 3: event boost
    #if there is an active event happening right now for this product's sport
    if product_sport in active_events_list:
        boost_score += 0.2
        
    #returning the calculated boost score rounded to 2 decimals
    return round(boost_score, 2)

#helper function to get a list of active sports based on today's date and events data
def get_active_event_sports(events_df, current_date, user_country):
    #filtering events that are currently happening and match the user's region (or global)
    active_events = events_df[
        (events_df['start_date'] <= current_date) & 
        (events_df['end_date'] >= current_date) &
        ((events_df['region'] == user_country) | (events_df['region'] == 'Global'))
    ]
    #returning a unique list of sports that currently have active events
    return active_events['sport'].unique().tolist()