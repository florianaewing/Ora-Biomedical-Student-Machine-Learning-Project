# Machine Learning for Predicting Lifespan-Extending Chemical Compounds

## Project Overview

This project applies machine learning to predict whether a chemical compound extends organism lifespan. Using curated biological and chemical data, we train a binary classifier to distinguish lifespan-extending compounds from non-extending ones.

- **Task**: Binary classification (lifespan extension: Yes / No)
- **Primary Model**: Random Forest Classifier
- **Domain**: Computational biology / drug discovery / aging research

---

## Objectives

- Build a supervised machine learning model to predict lifespan-extending compounds.
- Engineer biologically meaningful and chemical features.
- Evaluate model performance using standard classification metrics.

---

## Dataset

### Primary Dataset: DrugAge

- **Source**: DrugAge Database  
  https://genomics.senescence.info/drugs/
- **Description**:  
  A curated dataset of chemical compounds annotated with their effects on organism lifespan.
- **Labels**:
  - `1`: Lifespan increased
  - `0`: Lifespan not increased

The dataset is used to extract:
- Compound identifiers
- Lifespan outcome labels

---

## Feature Engineering

### 1. Biological Features (Initial Focus)

- **Gene Ontology (GO) terms** for proteins targeted by each compound
- **Source**: Drug–Gene Interaction Database (DGIdb)  
  https://dgidb.org/downloads
- **Approach**:
  - Map compounds to target genes/proteins
  - Encode associated GO terms as features (e.g., binary or frequency-based vectors)

### 2. Chemical Features (Optional / Extended)

- **Chemical descriptors** derived from molecular structures (e.g., SMILES)
- Examples:
  - Physicochemical properties
  - Molecular fingerprints
- Tools such as RDKit can be used for descriptor computation

---

## Data Preprocessing

- Feature cleaning and normalization (as needed)
- Handling missing values
- Encoding categorical features

### Dataset Split

- **Training set**: 70–80%
- **Validation/Test set**: 20–30%

A held-out test set should be reserved for final evaluation.

---

## Model Selection

- **Baseline Model**: Random Forest Classifier (as used in the reference article)
- **Optional Comparisons**:
  - Support Vector Machines (SVM)
  - Gradient Boosting (e.g., XGBoost, LightGBM)

---

## Model Training

- Train the classifier on the training split
- Tune hyperparameters if necessary (e.g., number of trees, max depth)

---

## Evaluation Metrics

Model performance is evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC–AUC (for probabilistic outputs)

### Reporting

- Report metrics on:
  - Training set
  - Validation set
  - Final held-out test set

---

## Expected Outcomes

- A trained model capable of predicting lifespan-extending compounds
- Insights into which biological pathways or chemical properties are associated with lifespan extension
- A reproducible pipeline for future experimentation and model comparison

---

## Future Extensions

- Incorporate additional biological annotations
- Explore deep learning models
- Perform cross-species generalization analysis
- Interpret model predictions using feature importance or SHAP values
