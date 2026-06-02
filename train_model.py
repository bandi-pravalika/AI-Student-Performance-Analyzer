"""Standalone model training script."""
import pickle
import json
from pathlib import Path
from src.data.generator import generate_synthetic_data
from src.ml.models.model import EnsembleModel
from src.ml.preprocessing.pipeline import PreprocessingPipeline
from src.ml.features.engineer import FeatureEngineer
from src.ml.evaluation.metrics import ModelEvaluator
from sklearn.model_selection import train_test_split
from src.core.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def train_and_save_model(n_samples: int = 500, output_path: str = "ml_models/v1"):
    """
    Train ensemble model and save artifacts.
    
    Args:
        n_samples: Number of samples to generate
        output_path: Path to save model artifacts
    """
    
    logger.info("Starting model training pipeline...")
    
    # Create output directory
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # 1. Generate data
    logger.info(f"Generating {n_samples} synthetic samples...")
    df = generate_synthetic_data(n_samples=n_samples)
    
    # 2. Split data
    X = df[['Study_Hours', 'Attendance', 'Prev_Score', 'Test_Prep']]
    y = df['Final_Score']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.TEST_SIZE, random_state=config.RANDOM_SEED
    )
    logger.info(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    # 3. Feature engineering
    logger.info("Applying feature engineering...")
    feature_engineer = FeatureEngineer()
    X_train_engineered = feature_engineer.engineer_features(X_train)
    X_test_engineered = feature_engineer.engineer_features(X_test)
    
    # 4. Preprocessing
    logger.info("Preprocessing features...")
    preprocessor = PreprocessingPipeline(scaling_method=config.FEATURE_SCALING)
    X_train_scaled = preprocessor.fit_transform(X_train_engineered)
    X_test_scaled = preprocessor.transform(X_test_engineered)
    
    # 5. Train ensemble model
    logger.info("Training ensemble model...")
    model = EnsembleModel()
    model.train(X_train_scaled, y_train)
    
    # 6. Evaluate
    logger.info("Evaluating model...")
    metrics = model.evaluate(X_test_scaled, y_test)
    logger.info(f"Evaluation metrics: {metrics}")
    
    # 7. Save artifacts
    logger.info("Saving model artifacts...")
    
    # Save models
    for name, m in model.models.items():
        model_path = Path(output_path) / f"{name}_model.pkl"
        m.save(str(model_path))
    
    # Save preprocessor
    preprocessor_path = Path(output_path) / "preprocessor.pkl"
    with open(preprocessor_path, 'wb') as f:
        pickle.dump(preprocessor, f)
    
    # Save feature engineer
    feature_path = Path(output_path) / "feature_engineer.pkl"
    with open(feature_path, 'wb') as f:
        pickle.dump(feature_engineer, f)
    
    # Save metadata
    metadata = {
        'model_type': 'ensemble',
        'n_samples_trained': n_samples,
        'train_size': len(X_train),
        'test_size': len(X_test),
        'metrics': metrics,
        'feature_names': feature_engineer.get_all_features(),
        'weights': model.weights,
        'scaling_method': config.FEATURE_SCALING
    }
    
    metadata_path = Path(output_path) / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Model artifacts saved to {output_path}")
    logger.info("Training complete!")
    
    return model, preprocessor, feature_engineer, metrics


if __name__ == "__main__":
    train_and_save_model()
