import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

def run_full_report(model, X_test, y_test, model_name="Winning Model"):

    print(f"\n" + "="*30)
    print(f"USED {model_name.upper()}:")
    print("="*30 + "\n")


    y_pred = model.predict(X_test)
    
    print("Final Performance Metrics:")
    print(classification_report(y_test, y_pred))
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens')
    
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    
    plt.title(f'Confusion Matrix - Used {model_name}') 
    plt.show()




