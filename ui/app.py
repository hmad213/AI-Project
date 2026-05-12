import os
import sys
import joblib
import pandas as pd

# Setup paths
UI_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(UI_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.tokenizer import clean_text

# Defined the  Paths
MODEL_PATH = os.path.join(ROOT_DIR, "models", "sarcasm_model.pkl")
STATS_PATH = os.path.join(ROOT_DIR, "models", "model_comparison.csv")
WINNER_PATH = os.path.join(ROOT_DIR, "models", "winner_name.txt")

try:
    # Benchmarks
    if os.path.exists(STATS_PATH):
        stats_df = pd.read_csv(STATS_PATH)
        print("\n ALL MODEL METRICS (Benchmarking Results):")
        print("="*50)
        print(stats_df.to_string(index=False))
        print("="*50)
    
    # Load the Best Model
    model = joblib.load(MODEL_PATH)
    with open(WINNER_PATH, "r") as f:
        model_name = f.read().strip()
        
    print(f"\n Deploying Winner: {model_name}")

except Exception as e:
    print(f" Error loading stats or model: {e}")
    sys.exit()


test_headlines = [
    "Allyan is very smart", 
    "Maaz is available 25 hours a day",
    "Local cat clearly plotting world domination",
    "I just love it when my computer crashes during a demo",
    "Alyan is wearing maaz clothes"
]

print(f"\n--- Predictions (Using {model_name}) ---")
for headline in test_headlines:
    cleaned = clean_text(headline)
    pred = model.predict([cleaned])[0]
    status = "Sarcastic " if pred == 1 else "Not Sarcastic 📰"
    print(f"[{status}] -> {headline}")