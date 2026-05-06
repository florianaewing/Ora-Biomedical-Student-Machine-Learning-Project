# Machine Learning for Predicting Lifespan-Extending Chemical Compounds

A reproduction and extension of [Barardo et al. (2017)](https://www.aging-us.com/article/101374/text) using entirely open-source tools and publicly available data.

**Result: AUC 0.837 — exceeding the paper's reported AUC of 0.800.**

Developed as part of an internship/research collaboration with **Ora Biomedical Inc.** at North Seattle College (Computer Science & Data Science, graduating June 2026).

---

## Overview

Identifying chemical compounds that extend healthy lifespan is a central goal of longevity research, but experimental screening of large compound libraries in whole organisms is expensive and slow. This project trains a machine learning classifier to predict whether a compound extends lifespan in *C. elegans* (the roundworm), enabling computational pre-screening of candidate compounds before experimental validation.

*C. elegans* is the primary model organism used due to its short lifespan (~3 weeks), well-characterised genetics, and the availability of large compound screening datasets.

---

## Key Results

| Feature Set | AUC (Ours) | AUC (Paper) | Accuracy | Sensitivity | Specificity | MCC |
|---|---|---|---|---|---|---|
| Chemical only | 0.810 | 0.730 | 0.852 | 0.287 | 0.968 | 0.362 |
| GO terms only | 0.711 | 0.740 | 0.613 | 0.858 | 0.563 | 0.316 |
| **Combined** | **0.837** | **0.800** | **0.865** | **0.332** | **0.974** | **0.429** |

Evaluated via nested 10-fold stratified cross-validation.

### Compound Screening

The final model was applied to screen 15 candidate longevity compounds:

| Compound | P(lifespan extension) | Prediction | Notes |
|---|---|---|---|
| Quercetin | 0.920 | ✅ Positive | Confirmed *C. elegans* lifespan extender |
| Resveratrol | 0.832 | ✅ Positive | Confirmed *C. elegans* lifespan extender |
| Metformin | 0.825 | ✅ Positive | Confirmed *C. elegans* lifespan extender |
| Berberine | 0.776 | ✅ Positive | AMPK activator, extends lifespan in worms |
| Curcumin | 0.732 | ✅ Positive | Confirmed *C. elegans* lifespan extender |
| Aspirin | 0.692 | ✅ Positive | COX inhibitor; moderate evidence in *C. elegans* |
| Fisetin | 0.682 | ✅ Positive | Flavonoid senolytic; lifespan extension confirmed |
| Rapamycin | 0.679 | ✅ Positive | mTOR inhibitor; confirmed lifespan extender |
| Spermidine | 0.664 | ✅ Positive | Polyamine; confirmed lifespan extender |
| Nicotinamide riboside | 0.537 | ✅ Positive | NAD⁺ precursor; mixed evidence across organisms |
| Lithium chloride | 0.426 | ❌ Negative | GSK-3 inhibitor; inconsistent *C. elegans* evidence |
| Acarbose | 0.120 | ❌ Negative | Extends mouse but not worm lifespan |
| Navitoclax | 0.046 | ❌ Negative | Senolytic; mechanism diverges from training set |
| Canagliflozin | 0.040 | ❌ Negative | Renal mechanism; limited *C. elegans* data |
| Dasatinib | 0.038 | ❌ Negative | Tyrosine kinase inhibitor senolytic |

The model correctly classified all 9 experimentally confirmed *C. elegans* lifespan extenders as positive.

---

## Methods

### Dataset

- **2,521 compounds** total: 428 positive (17.0%), 2,093 negative (83.0%) — matching the paper's ~5:1 negative-to-positive ratio
- **Positives**: DrugAge Build 4 — *C. elegans* entries with `avg_lifespan_change_percent > 0`
- **Negatives**: DrugAge *C. elegans* entries with `avg_lifespan_change_percent ≤ 0` + approved small molecules from ChEMBL (Phase 4) not present in the positive set
- SMILES strings sourced from PubChem; deduplicated by SMILES and compound name

### Feature Engineering

**Chemical descriptors (179 features)**
- Computed using RDKit: 217 two-dimensional molecular descriptors covering electronic, steric, and hydrophobic properties
- Near-constant descriptors (>98% identical values) removed; missing values imputed with column medians

**GO term features (380 features)**
- Protein targets retrieved via ChEMBL mechanism-of-action endpoint
- Targets annotated with Gene Ontology (GO) terms from ChEMBL target component cross-references
- Covers GO Biological Process, Molecular Function, and Cellular Component
- 51% of compounds had at least one GO term annotation

> Note: The original paper used STITCH v4 for drug-target interactions, which has been deprecated since 2015. ChEMBL provides equivalent curated data via a maintained REST API.

### Model

- **Random Forest** (scikit-learn): 500 trees, sqrt feature subsampling, `class_weight='balanced'`
- **Nested 10-fold stratified cross-validation** for unbiased performance estimation
- **Boruta feature selection**: 100 iterations — identified 23 confirmed predictive features from 559

### Boruta-Confirmed Features (23 of 559)

| Feature | Type | Interpretation |
|---|---|---|
| membrane, plasma membrane | GO term | Targets membrane-associated proteins |
| protein binding | GO term | Targets hub proteins in signalling |
| qed | Chemical | Drug-likeness estimate |
| MolWt / HeavyAtomMolWt | Chemical | Molecular size |
| BalabanJ | Chemical | Molecular connectivity / topology |
| Chi0v, Chi1v | Chemical | Valence connectivity indices |
| Kappa1, Kappa2, Kappa3 | Chemical | Molecular shape |
| LabuteASA | Chemical | Solvent-accessible surface area |
| BCUT2D_MWHI/CHGLO | Chemical | Eigenvalue descriptors (mass and charge) |
| SMR_VSA, SlogP_VSA, EState_VSA | Chemical | Surface area by logP / charge |

---

## Repo Structure

```
├── notebooks/          # Jupyter notebooks: EDA, feature engineering, model training, evaluation
├── pyApp/              # Python application code
├── Machine learning for predicting lifespan-extending chemical compounds.pdf   # Original Barardo et al. (2017) paper
└── README.md
```

---

## Tech Stack

- **Python**: scikit-learn, NumPy, Pandas, RDKit
- **Data sources**: DrugAge Build 4, ChEMBL REST API, PubChem
- **Feature selection**: Boruta
- **Evaluation**: Nested stratified cross-validation, ROC-AUC, MCC

---

## References

- Barardo D, et al. (2017). Machine learning for predicting lifespan-extending chemical compounds. *Aging (Albany NY)*, 9(6), 1721–1737.
- Freshney A, et al. (2024). DrugAge Build 4. Human Ageing Genomic Resources.
- Gaulton A, et al. (2017). The ChEMBL database in 2017. *Nucleic Acids Research*, 45(D1), D945–D954.
- Landrum G, et al. (2023). RDKit: Open-source cheminformatics.
- Kursa MB, Rudnicki WR. (2010). Feature selection with the Boruta package. *Journal of Statistical Software*, 36(11), 1–13.
- Pedregosa F, et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
