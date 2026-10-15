# exp1_baseline: EDA and LinearRegression baseline
_Saved: 2026-10-13T01:26:07_

## Dataset
- **name:** sklearn load_diabetes
- **n_samples:** 442
- **n_features:** 10

## Preprocessing
None applied (sklearn's features are already mean-centered and scaled)

## Random seed(s)
- **train_test_split:** 42
- **KFold:** 42

## Models and hyperparameters
- **LinearRegression:** default settings

## Train/test protocol
80/20 split, random_state=42; test set held out

## Cross-validation protocol
5-fold shuffled KFold, random_state=42, on the training set only

## Metrics
| model | alpha | test_MSE | test_RMSE | test_R2 | cv_RMSE_mean | cv_RMSE_std |
|---|---|---|---|---|---|---|
| LinearRegression | None | 2900.1936 | 53.8534 | 0.4526 | 55.3946 | 2.3615 |

## Saved tables
- results/tables/baseline_coefficients.csv
- results/tables/results_table.csv

## Saved figures
- results/figures/target_distribution.png
- results/figures/correlation_matrix.png
- results/figures/baseline_actual_vs_predicted.png

## WARNING: files listed but not found
- figures/correlation_matrix.png

## Observation
CV and test errors agree, so the baseline is stable. Several coefficients (notably the correlated s1/s2 pair) are large and of opposite sign, consistent with multicollinearity.

## Environment
python=3.14.2; platform=Windows-11-10.0.26200-SP0; numpy=2.5.3; pandas=3.0.6; sklearn=1.9.1; scipy=1.18.1; matplotlib=3.11.2
