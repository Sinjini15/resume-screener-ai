# src/model_training.py
from pathlib import Path
from utils.feature_utils import load_training_data, engineer_features
from utils.data_utils import load_resumes
from utils.feature_utils import engineer_features
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import matplotlib.pyplot as plt


def train_model(X, y):
    """
    Trains a CatBoost Regressor and returns the trained model.
    """

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize CatBoost
    model = CatBoostRegressor(
        iterations=800,
        depth=2,
        learning_rate=0.075,
        loss_function='RMSE',
        verbose=100
    )

    # Fit model
    model.fit(X_train, y_train, cat_features=['education_level'] if 'education_level' in X.columns else None)

    # Predict and evaluate
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    print(f"Test RMSE: {rmse:.5f}")

    return model

def save_model(model):
    """
    Saves the trained model.
    """
    models_dir = Path(__file__).resolve().parents[1] / 'models'
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / 'catboost_resume_matcher.pkl'
    joblib.dump(model, model_path)
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    df = load_training_data()
    
    X, y = engineer_features(df)
    model = train_model(X, y)

    save_model(model)
    
    

    # After training your CatBoost model
    feature_importances = model.get_feature_importance()
    feature_names = X.columns

    # Print in order
    for name, importance in sorted(zip(feature_names, feature_importances), key=lambda x: x[1], reverse=True):
        print(f"{name}: {importance:.2f}")

    # Optional: plot
    plt.figure(figsize=(10, 5))
    plt.barh(feature_names, feature_importances)
    plt.xlabel('Importance')
    plt.title('Feature Importance from CatBoost')
    plt.gca().invert_yaxis()
    plt.show()
    plt.savefig('./feature_importance.png')
