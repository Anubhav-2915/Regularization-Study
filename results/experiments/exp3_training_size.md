# exp3_training_size: Regularization vs training-set size
_Saved: 2026-10-13T01:26:39_

## Dataset
- **name:** sklearn load_diabetes
- **n_train_pool:** 353
- **n_test:** 89

## Preprocessing
None applied

## Random seed(s)
- **split:** 42
- **subsampling_and_cv_seeds:** 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19

## Models and hyperparameters
- **LinearRegression:** default
- **Ridge:** alpha_grid=0.001, 0.01, 0.1, 1, 10, 100, 1000
- **Lasso:** alpha_grid=0.001, 0.01, 0.1, 1, 10, 100, 1000; max_iter=100000

## Train/test protocol
Fixed test set; 100% = all 353 training rows; fractions [0.1, 0.25, 0.5, 0.75, 1.0]; nested random subsets per seed

## Cross-validation protocol
Alpha chosen per training subset by GridSearchCV, 5-fold shuffled KFold (random_state = seed), lowest mean CV RMSE; test set never used

## Metrics
| model | fraction | n_train | test_RMSE_mean | test_RMSE_std | test_R2_mean | test_R2_std | median_alpha | mean_zero_coefs |
|---|---|---|---|---|---|---|---|---|
| Lasso | 0.1000 | 35 | 61.8625 | 6.1846 | 0.2708 | 0.1540 | 0.1000 | 4.1000 |
| Lasso | 0.2500 | 88 | 55.8719 | 2.1538 | 0.4100 | 0.0460 | 0.1000 | 2.5500 |
| Lasso | 0.5000 | 176 | 54.7627 | 1.3009 | 0.4337 | 0.0269 | 0.0100 | 1.4000 |
| Lasso | 0.7500 | 265 | 53.8309 | 0.5048 | 0.4530 | 0.0103 | 0.0100 | 0.7000 |
| Lasso | 1.0000 | 353 | 53.7353 | 0.0852 | 0.4550 | 0.0017 | 0.0055 | 0.0000 |
| LinearRegression | 0.1000 | 35 | 65.5019 | 6.5673 | 0.1825 | 0.1701 | None | 0.0000 |
| LinearRegression | 0.2500 | 88 | 57.0559 | 2.1904 | 0.3847 | 0.0477 | None | 0.0000 |
| LinearRegression | 0.5000 | 176 | 55.1520 | 1.2058 | 0.4256 | 0.0250 | None | 0.0000 |
| LinearRegression | 0.7500 | 265 | 54.1121 | 0.4900 | 0.4473 | 0.0100 | None | 0.0000 |
| LinearRegression | 1.0000 | 353 | 53.8534 | 0.0000 | 0.4526 | 0.0000 | None | 0.0000 |
| Ridge | 0.1000 | 35 | 59.4624 | 3.7933 | 0.3301 | 0.0880 | 0.0100 | 0.0000 |
| Ridge | 0.2500 | 88 | 55.8158 | 1.5659 | 0.4115 | 0.0333 | 0.0100 | 0.0000 |
| Ridge | 0.5000 | 176 | 54.8429 | 1.1257 | 0.4321 | 0.0233 | 0.0100 | 0.0000 |
| Ridge | 0.7500 | 265 | 53.8833 | 0.4989 | 0.4520 | 0.0102 | 0.0100 | 0.0000 |
| Ridge | 1.0000 | 353 | 53.6588 | 0.1527 | 0.4565 | 0.0031 | 0.0100 | 0.0000 |

## Saved tables
- results/tables/training_size_raw.csv
- results/tables/training_size_summary.csv
- results/tables/regularization_gain.csv

## Saved figures
- results/figures/size_vs_test_rmse.png
- results/figures/regularization_gain_vs_size.png

## Observation
Regularization helped most when training data was scarce and its benefit shrank as data grew, while remaining small but consistently positive at larger sizes. Linear regression was least stable at small sizes.

## Environment
python=3.14.2; platform=Windows-11-10.0.26200-SP0; numpy=2.5.3; pandas=3.0.6; sklearn=1.9.1; scipy=1.18.1; matplotlib=3.11.2
