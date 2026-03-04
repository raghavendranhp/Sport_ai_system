#importing pandas to format the input data exactly how the model expects it
import pandas as pd

#importing joblib to load the saved machine learning model
import joblib

#importing os to handle relative file paths safely
import os

#defining the path to our saved random forest model
#we use os.path to ensure it works regardless of where the script is executed from
model_path = os.path.join(os.path.dirname(__file__), '../models/demand_model.pkl')

#creating a helper function to load the model safely
def load_model():
    #checking if the model file actually exists before trying to load
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        #if it doesn't exist, we return none so the app doesn't crash
        return None

#loading the model once when the script starts
demand_model = load_model()

#creating the main function that our streamlit app will call to get predictions
def predict_demand(discount, sale_month, sale_day, sale_dayofweek, event_active):
    #safety check in case the user forgot to run the jupyter notebook
    if demand_model is None:
        return 0
        
    #structuring the input data as a pandas dataframe
    #the columns must exactly match the features list from our training phase
    input_features = pd.DataFrame({
        'discount': [discount],
        'sale_month': [sale_month],
        'sale_day': [sale_day],
        'sale_dayofweek': [sale_dayofweek],
        'event_active': [event_active]
    })
    
    #asking the model to predict the quantity based on the provided features
    predicted_quantity = demand_model.predict(input_features)
    
    #returning the prediction rounded to the nearest whole number (you can't sell half a bat)
    return int(round(predicted_quantity[0]))