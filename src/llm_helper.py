#importing the ollama library to interact with your local models
import ollama

#defining a function to generate natural language insights for the report
def generate_insights(user_profile, top_products, active_events):
    #formatting the top products into a simple comma-separated string
    product_names = ", ".join(top_products['name'].tolist())
    
    #formatting the active events into a string, or noting if none are active
    events_str = ", ".join(active_events) if active_events else "no major events"
    
    #creating the prompt that tells the llm what we want it to do
    prompt = f"""
    you are an expert retail ai for a sports goods store.
    
    user profile: {user_profile['age']} year old from {user_profile['region']}. 
    favorite sport: {user_profile['favorite_sport']} (skill level: {user_profile['skill_level']}).
    current regional/global events happening: {events_str}.
    top recommended products for them: {product_names}.
    
    write a short, 3-sentence insight explaining to the store manager why these specific products are recommended for this user right now based on their profile and current events.
    """
    
    #wrapping the call in a try-except block so the app doesn't crash if ollama is off
    try:
        #sending the prompt to the local model 
        response = ollama.chat(model='gemma:2b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        
        #returning the actual text response from the model
        return response['message']['content']
        
    except Exception as e:
        #returning a fallback error message if ollama is not running in the background
        return f"ai insight generation failed. please check if ollama is running locally. error: {e}"