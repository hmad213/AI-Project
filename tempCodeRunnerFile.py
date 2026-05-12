or nb in notebooks:
        if os.path.exists(nb):
            run_notebook(nb)
        else:
            print(f"Could not find {nb}")

    print("\n🚀 Launching Prediction App...")
    app_path 