import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

def train_models(df):
    """Train multiple ML models to predict Pass/Fail."""
    # Assume 'Status' is the target column
    if "Status" not in df.columns:
        return None, "Target column 'Status' not found."
        
    # Features for prediction (excluding target, names, identifiers, and derived percentage/grades)
    # We will predict Pass/Fail based on Study Hours, Attendance, Previous Semester (%), and subject scores
    features = ["Study Hours", "Attendance (%)", "Previous Semester (%)", 
                "Math Score", "Science Score", "English Score", "History Score"]
    
    # Check if features exist
    available_features = [f for f in features if f in df.columns]
    
    if not available_features:
        return None, "No suitable numeric features found for training."
        
    X = df[available_features]
    y = df["Status"].apply(lambda x: 1 if x == "Pass" else 0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    models = {
        "Logistic Regression": LogisticRegression(),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5)
    }
    
    results = {}
    trained_models = {}
    
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        results[name] = accuracy
        trained_models[name] = model
        
    return {
        "results": results,
        "models": trained_models,
        "scaler": scaler,
        "features": available_features
    }, "Success"

def predict_risk(student_data, trained_models, scaler, features, model_name="Random Forest"):
    """Predict if a specific student is at risk of failing."""
    if model_name not in trained_models:
        return None
        
    model = trained_models[model_name]
    
    # Ensure correct order of features
    X_new = student_data[features].values.reshape(1, -1)
    X_new_scaled = scaler.transform(X_new)
    
    prediction = model.predict(X_new_scaled)
    # Return True if at risk (predicted 0 = Fail)
    return prediction[0] == 0

def run_clustering(df):
    """Cluster students into groups based on behavior (Study Hours and Attendance)."""
    features = ["Study Hours", "Attendance (%)"]
    
    if not all(f in df.columns for f in features):
        return None
        
    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Use 3 clusters for simple grouping (e.g. Low, Medium, High engagement)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_scaled)
    
    df_clustered = df.copy()
    
    # Let's map cluster IDs to a string name based on their average attendance
    df_clustered["Cluster_ID"] = clusters
    cluster_means = df_clustered.groupby("Cluster_ID")["Attendance (%)"].mean().sort_values()
    
    # Mapping logic: lowest mean = "Low Engagement", highest = "Highly Engaged"
    mapping = {
        cluster_means.index[0]: "Low Engagement",
        cluster_means.index[1]: "Average Engagement",
        cluster_means.index[2]: "Highly Engaged"
    }
    
    df_clustered["Student Segment"] = df_clustered["Cluster_ID"].map(mapping)
    return df_clustered
