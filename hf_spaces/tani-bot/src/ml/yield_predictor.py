#!/usr/bin/env python3
"""XGBoost Yield Prediction Model for TaniBot"""

import sys
import json
import numpy as np
from pathlib import Path

sys.path.insert(0, '/mnt/data/openclaw/workspace/tani-bot/src')

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')


class YieldPredictor:
    """XGBoost model for crop yield prediction"""
    
    def __init__(self):
        self.model = XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        )
        self.is_trained = False
        
    def load_synthetic_data(self, data_path: str = None) -> dict:
        """Load synthetic Indonesia agricultural dataset"""
        if data_path is None:
            data_path = "/mnt/data/openclaw/workspace/tani-bot/data/synthetic_indonesia_dataset.json"
        
        with open(data_path, 'r') as f:
            return json.load(f)
    
    def prepare_features(self, crops: list, fields: list, history: list, weather: dict) -> tuple:
        """Prepare features for model training"""
        
        # Create feature dataset with consistent column order
        feature_columns = [
            'growing_season_days', 'base_yield', 'rainfall_min', 'rainfall_max',
            'avg_temperature', 'avg_rainfall', 'field_area', 'soil_ph'
        ]
        
        features = []
        targets = []
        
        for record in history:
            # Find crop info
            crop = next((c for c in crops if c['name'] == record['crop_name']), None)
            if not crop:
                continue
                
            # Find field weather data (simplified - use average)
            avg_temp = 27.0  # Tropical average
            avg_rainfall = 150  # Monthly mm
            
            # Create feature vector as list in consistent order
            feature = [
                crop['growing_season_days'],
                crop['base_yield'],
                crop['rainfall_min'],
                crop['rainfall_max'],
                avg_temp,
                avg_rainfall,
                10.0,  # field_area
                6.0    # soil_ph
            ]
            
            features.append(feature)
            targets.append(record['yield_value'])
        
        # Convert to numpy arrays with explicit 2D shape
        features_array = np.array(features, dtype=np.float32)
        targets_array = np.array(targets, dtype=np.float32)
        
        return features_array, targets_array
    
    def train(self, data_path: str = None):
        """Train the yield prediction model"""
        print("Loading synthetic data...")
        dataset = self.load_synthetic_data(data_path)
        
        crops = dataset['crops']
        fields = dataset['fields']
        history = dataset['field_history']
        
        print(f"Processing {len(history)} planting records...")
        features, targets = self.prepare_features(crops, fields, history, {})
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            features, targets, test_size=0.2, random_state=42
        )
        
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        
        # Train model
        print("\nTraining XGBoost model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        mae_train = mean_absolute_error(y_train, y_pred_train)
        mae_test = mean_absolute_error(y_test, y_pred_test)
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        
        print("\n" + "=" * 60)
        print("📊 MODEL EVALUATION")
        print("=" * 60)
        print(f"Training MAE: {mae_train:.2f}")
        print(f"Test MAE: {mae_test:.2f}")
        print(f"Training R²: {r2_train:.3f}")
        print(f"Test R²: {r2_test:.3f}")
        
        return {
            'mae_train': mae_train,
            'mae_test': mae_test,
            'r2_train': r2_train,
            'r2_test': r2_test
        }
    
    def predict(self, crop_name: str, avg_temp: float, avg_rainfall: float, 
                growing_season_days: int, base_yield: float) -> dict:
        """Predict yield for given conditions"""
        if not self.is_trained:
            return {'error': 'Model not trained yet'}
        
        # Create feature vector
        feature = np.array([[
            growing_season_days,
            base_yield,
            100,  # rainfall_min (placeholder)
            250,  # rainfall_max (placeholder)
            avg_temp,
            avg_rainfall,
            10.0,  # field_area
            6.0    # soil_ph
        ]])
        
        prediction = self.model.predict(feature)[0]
        
        return {
            'crop': crop_name,
            'predicted_yield': round(prediction, 2),
            'units': 'ton/hectare',
            'conditions': {
                'temperature': avg_temp,
                'rainfall': avg_rainfall
            }
        }


# Test the model
if __name__ == "__main__":
    print("=" * 60)
    print("🌾 TANI BOT - YIELD PREDICTOR TRAINING")
    print("=" * 60)
    
    predictor = YieldPredictor()
    
    # Train
    results = predictor.train()
    
    # Test predictions
    print("\n" + "=" * 60)
    print("🔮 SAMPLE PREDICTIONS")
    print("=" * 60)
    
    test_cases = [
        ("Rice (Padi)", 27.0, 150, 120, 6.5),
        ("Corn (Jagung)", 28.0, 120, 90, 7.0),
        ("Cassava (Singkong)", 26.0, 180, 180, 25.0),
    ]
    
    for crop, temp, rain, days, base in test_cases:
        result = predictor.predict(crop, temp, rain, days, base)
        print(f"\n{crop}:")
        print(f"  Predicted Yield: {result['predicted_yield']} ton/hectare")
        print(f"  Conditions: {temp}°C, {rain}mm rainfall")
