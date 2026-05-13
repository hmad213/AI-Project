from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline

def get_all_pipelines():
    models = {
        "Logistic Regression": LogisticRegression(solver='liblinear', class_weight="balanced"),
        "SVM (LinearSVC)": LinearSVC(dual='auto', random_state=42, class_weight="balanced"),
        "Decision Tree": DecisionTreeClassifier(max_depth=50, random_state=42),
        "K-Means Clustering": KMeans(n_clusters=2, random_state=42, n_init=10) 
    }
    
    pipelines = {}
    for name, model in models.items():
        pipelines[name] = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 3), min_df=2, max_df=0.9, sublinear_tf=True, max_features=50000)),
            ('clf', model)
        ])
    
    return pipelines