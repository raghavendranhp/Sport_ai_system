#importing necessary libraries for the web app and data handling
import streamlit as st
import pandas as pd
from datetime import datetime

#importing our custom "brains" from the src folder
from src.recommender import get_top_5
from src.demand_inference import predict_demand
from src.llm_helper import generate_insights

#setting up the web page layout
st.set_page_config(page_title="sports goods ai system", layout="wide")

#caching the data loading so the app doesn't slow down on every click
@st.cache_data
def load_data():
    #loading the datasets from our data folder
    users = pd.read_csv('data/Users.csv')
    products = pd.read_csv('data/Products.csv')
    events = pd.read_csv('data/Events.csv')
    
    #converting event dates to pandas datetime objects
    events['start_date'] = pd.to_datetime(events['start_date'])
    events['end_date'] = pd.to_datetime(events['end_date'])
    return users, products, events

#loading the data into variables
users_df, products_df, events_df = load_data()

#adding the main title to the dashboard
st.title("sports goods intelligent recommendation & demand insight system")

#creating three clickable tabs for rajesh to navigate
tab1, tab2, tab3 = st.tabs(["smart recommendations", "demand insights", "knowledge graph"])

# --- tab 1: smart recommendations ---
with tab1:
    st.header("user-specific recommendations")
    
    #creating a readable list of users for the dropdown menu
    user_list = users_df.apply(lambda row: f"{row['user_id']} - {row['age']}yo {row['favorite_sport']} fan in {row['region']}", axis=1)
    
    #dropdown menu to select a user
    selected_user_str = st.selectbox("select a user profile:", user_list)
    
    if selected_user_str:
        #extracting just the user_id (e.g., 'u001') from the selected string
        user_id = selected_user_str.split(" - ")[0]
        
        #setting a fixed "current date" that falls within our dataset's event timeline
        current_date = pd.to_datetime("2026-02-16") 
        
        #asking our recommender brain for the top 5 products
        top_products = get_top_5(user_id, users_df, products_df, events_df, current_date)
        
        #displaying the results as a clean table
        st.subheader("top 5 recommended products")
        st.dataframe(top_products, use_container_width=True)
        
        # --- gemma 2b insight generation ---
        st.subheader("ai reasoning insight (powered by gemma:2b)")
        
        #getting the raw user profile data
        user_profile = users_df[users_df['user_id'] == user_id].iloc[0]
        
        #finding active events for this specific user's region
        indian_cities = ['Hyderabad', 'Delhi', 'Mumbai', 'Chennai', 'Bangalore']
        user_country = 'India' if user_profile['region'] in indian_cities else 'UK'
        
        active_events = events_df[
            (events_df['start_date'] <= current_date) & 
            (events_df['end_date'] >= current_date) & 
            ((events_df['region'] == user_country) | (events_df['region'] == 'Global'))
        ]['event_name'].tolist()
        
        #calling our llm helper function and displaying the response in a blue box
        with st.spinner("gemma is thinking..."):
            insight_text = generate_insights(user_profile, top_products, active_events)
            st.info(insight_text)

# --- tab 2: demand insights ---
with tab2:
    st.header("short-term demand prediction")
    
    #creating two columns to place inputs on the left and results on the right
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### scenario simulator")
        #sliders and buttons for the manager to test different scenarios
        discount_val = st.slider("planned discount (%)", 0, 50, 10)
        is_event = st.radio("is there an active event?", [1, 0], format_func=lambda x: "yes" if x == 1 else "no")
        
    with col2:
        st.markdown("### predicted demand")
        #feeding the inputs into our saved random forest model
        #we use placeholder dates here (e.g., month 3, day 14, saturday) for the simulation
        predicted_qty = predict_demand(discount=discount_val, sale_month=3, sale_day=14, sale_dayofweek=5, event_active=is_event)
        
        #displaying the result in a large, bold metric widget
        st.metric(label="expected units sold per product", value=f"{predicted_qty} units")


# --- tab 3: knowledge graph ---
with tab3:
    st.header("seshat-style reasoning logic")
    st.markdown('''
    ### how the system thinks:
    the recommendation engine doesn't just guess; it uses structured rules to boost product relevance.
    
    * **regional boost:** if a user is in hyderabad, the system automatically prioritizes cricket gear.
    * **event boost:** if the ipl or world cup is currently active, relevant sports gear gets a 20% score increase.
    * **skill matching:** beginner users are shielded from highly advanced, expensive equipment unless it is universally applicable (like a jersey).
    ''')
