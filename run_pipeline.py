import subprocess
import os
import sys
import asyncio



def run_notebook(notebook_path):
    print(f"⏳ Executing {notebook_path}...")
    
    # 10-minute timeout because the SARC dataset is huge
    result = subprocess.run([
        "jupyter", "nbconvert", 
        "--to", "notebook", 
        "--execute", 
        "--ExecutePreprocessor.timeout=600", 
        "--inplace", 
        notebook_path
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"{notebook_path} completed successfully.")
    else:
        print(f"Error in {notebook_path}:")
        print(result.stderr)
    
        sys.exit(1)

def main():
    if not os.path.exists("notebooks"):
        print("Error: Run this script from the project root folder.")
        sys.exit(1)

    notebooks = [
        "notebooks/01_preprocessing.ipynb",
        "notebooks/02_finetuning.ipynb",
        "notebooks/03_evaluation.ipynb"
    ]

    for nb in notebooks:
        if os.path.exists(nb):
            run_notebook(nb)
        else:
            print(f"Could not find {nb}")

    print("\n🚀 Launching Prediction App...")
    app_path = os.path.join("ui", "app.py")
    
    subprocess.run(["python", app_path])

if __name__ == "__main__":
    main()