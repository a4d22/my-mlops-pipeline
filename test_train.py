import os
import pytest
import pandas as pd
from train import load_and_preprocess_data

def test_data_preprocessing_shapes():
    """Test that the preprocessed data splits have the correct shapes and columns."""
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    
    # The California housing dataset has exactly 8 feature columns
    expected_features = 8
    
    # Assert column dimensions match our expectations
    assert X_train.shape[1] == expected_features, f"Expected {expected_features} features, got {X_train.shape[1]}"
    assert X_test.shape[1] == expected_features
    
    # Assert dataset lengths match up (80% train, 20% test)
    total_rows = X_train.shape[0] + X_test.shape[0]
    assert total_rows == 20640, f"Expected total rows to be 20640, got {total_rows}"

def test_no_null_values():
    """Ensure that no missing values (NaNs) exist in the split datasets."""
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    
    assert X_train.isnull().sum().sum() == 0, "X_train contains missing values!"
    assert X_test.isnull().sum().sum() == 0, "X_test contains missing values!"