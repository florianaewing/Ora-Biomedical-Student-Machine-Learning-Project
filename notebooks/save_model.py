"""
save_model.py — Train and Save Model Weights

Trains the final Random Forest on the full labeled dataset using the
23 Boruta-confirmed features, then saves the model to disk as model.pkl.

This script should be run once from the notebooks/ directory after the
full pipeline (Phases 1-3b) has been completed. The saved model can then
be loaded by predict_lifespan.py for inference on new compounds without
retraining.

Usage:
    python save_model.py

Outputs:
    data/model.pkl   — saved RF model + confirmed feature lists
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

DATA_DIR     = Path("data")
RANDOM_STATE = 42
RF_PARAMS    = {
    "n_estimators":  500,
    "max_features":  "sqrt",
    "class_weight":  "balanced",
    "random_state":  RANDOM_STATE,
    "n_jobs":        -1,
}


def main():
    print("Loading training data...")
    chem   = pd.read_csv(DATA_DIR / "chemical_descriptors.csv")
    go     = pd.read_csv(DATA_DIR / "go_term_features.csv")
    boruta = pd.read_csv(DATA_DIR / "boruta_selected_features.csv")

    confirmed = boruta[boruta["status"] == "confirmed"]["feature"].tolist()

    chem_cols = [c for c in chem.columns if c not in ("compound_name", "smiles", "label")]
    go_cols   = [c for c in go.columns   if c not in ("compound_name", "label")]

    merged = chem[["compound_name", "label"] + chem_cols].merge(
        go[["compound_name"] + go_cols], on="compound_name", how="inner"
    )

    all_cols       = chem_cols + go_cols
    confirmed_here = [f for f in confirmed if f in all_cols]
    confirmed_go   = [f for f in confirmed_here if f in go_cols]
    confirmed_chem = [f for f in confirmed_here if f in chem_cols]

    print(f"  Compounds:          {len(merged)}")
    print(f"  Positive:           {(merged['label']==1).sum()}")
    print(f"  Negative:           {(merged['label']==0).sum()}")
    print(f"  Confirmed chemical: {len(confirmed_chem)}")
    print(f"  Confirmed GO:       {len(confirmed_go)}")

    X = merged[confirmed_here].values.astype(float)
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    X = np.clip(X, -1e15, 1e15)
    y = merged["label"].values

    print(f"\nTraining Random Forest ({RF_PARAMS['n_estimators']} trees)...")
    rf = RandomForestClassifier(**RF_PARAMS)
    rf.fit(X, y)
    print("  Done.")

    model_path = DATA_DIR / "model.pkl"
    joblib.dump({
        "rf":             rf,
        "confirmed_chem": confirmed_chem,
        "confirmed_go":   confirmed_go,
    }, model_path)

    print(f"\n✅ Model saved to: {model_path}")
    print(f"   Use predict_lifespan.py to load and run inference.")


if __name__ == "__main__":
    main()