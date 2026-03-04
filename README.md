
# Sports Goods Intelligent Recommendation & Demand Insight System

This repository contains a modular AI system built to provide smart product recommendations, regional insights, and short-term demand forecasting for a sports goods marketplace. It utilizes structured reasoning (Seshat AI concepts) combined with Machine Learning and a local LLM for natural language insights.

## Live Application Demo
![Live App Demo](./live_app_demo.gif)

## System Architecture

The system is divided into three core "brains" and an interface:
1. **The Reasoning Layer (Knowledge Graph):** Hardcoded logic mapping sports to regions, events, and skill levels to simulate context-aware reasoning.
2. **The Recommendation Engine:** A weighted scoring algorithm that ranks products based on user match (40%), regional popularity (30%), active events (20%), and discounts (10%).
3. **The Demand Predictor:** A trained Random Forest Regression model that forecasts 7-day product demand based on seasonal trends, discounts, and event flags.
4. **The Insight Generator:** Integration with a local LLM (Ollama running Gemma 2B) to generate human-readable explanations for the recommendations.
```
## Project Structure

sports_ai_system/
├── data/                       # Raw CSV datasets (Products, Sales, Users, Events)
├── notebooks/                  
│   └── train_demand_model.ipynb # Model training and evaluation
├── models/                     
│   └── demand_model.pkl        # Serialized Random Forest model
├── src/                        # Core Python logic modules
│   ├── __init__.py             
│   ├── knowledge.py            # Rule-based logic and entity mappings
│   ├── recommender.py          # Match score calculation formula
│   ├── demand_inference.py     # Script for loading and using the ML model
│   └── llm_helper.py           # Local LLM integration for text insights
├── app.py                      # Main Streamlit dashboard application
├── live_app_demo.gif           # Demonstration of the working dashboard
└── requirements.txt            # Python dependencies
```

## Prerequisites

Before running the system, ensure you have the following installed:
* **Python 3.9+**
* **Ollama** installed locally (for AI insights)

You must also pull the specific Gemma model for the insight generator:
```bash
ollama run gemma:2b

```

## Installation & Setup

1. **Clone the repository** and navigate to the project directory:

```bash
cd sports_ai_system

```

2. **Install the required Python packages:**

```bash
pip install -r requirements.txt

```

3. **Train and save the Demand Model:**
Open the Jupyter Notebook located at `notebooks/train_demand_model.ipynb` and run all cells. This will process the historical sales data, train the Random Forest model, and save it as `demand_model.pkl` in the `models/` directory.

## Running the Application

Once the dependencies are installed, the model is trained, and Ollama is running in the background, you can launch the interactive dashboard:

```bash
streamlit run app.py

```

The application will open in your default web browser (typically at `http://localhost:8501`), where you can explore user-specific recommendations, run demand forecasting scenarios, and view the reasoning logic.

