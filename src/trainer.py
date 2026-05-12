from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline

def get_all_pipelines():
    models = {
        "Logistic Regression": LogisticRegression(solver='liblinear'),
        "SVM (LinearSVC)": LinearSVC(dual='auto', random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=50, random_state=42),
        "K-Means Clustering": KMeans(n_clusters=2, random_state=42, n_init=10) 
    }
    
    pipelines = {}
    for name, model in models.items():
        pipelines[name] = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2)),
            ('clf', model)
        ])
    
    return pipelines