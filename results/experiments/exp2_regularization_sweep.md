# exp2_regularization_sweep: Ridge and Lasso across alpha
_Saved: 2026-10-13T01:26:28_

## Dataset
- **name:** sklearn load_diabetes
- **n_samples:** 442

## Preprocessing
None applied (same as baseline)

## Random seed(s)
- **train_test_split:** 42
- **KFold:** 42

## Models and hyperparameters
- **Ridge:** alpha=0.001, 0.01, 0.1, 1, 10, 100, 1000
- **Lasso:** alpha=0.001, 0.01, 0.1, 1, 10, 100, 1000; max_iter=100000
- **LinearRegression:** baseline

## Train/test protocol
Same 80/20 split as the baseline; every model evaluated on the same test set

## Cross-validation protocol
Same 5-fold shuffled KFold (random_state=42) on the training set, same for every model

## Metrics
| model | alpha | cv_RMSE_mean | cv_RMSE_std | test_RMSE | test_R2 | n_zero_coefs |
|---|---|---|---|---|---|---|
| LinearRegression | None | 55.3946 | 2.3615 | 53.8534 | 0.4526 | 0 |
| Ridge | 0.0010 | 55.3784 | 2.3706 | 53.8128 | 0.4534 | 0 |
| Ridge | 0.0100 | 55.4094 | 2.3646 | 53.6870 | 0.4560 | 0 |
| Ridge | 0.1000 | 55.5268 | 2.4785 | 53.4461 | 0.4609 | 0 |
| Ridge | 1.0000 | 60.0214 | 4.3505 | 55.4745 | 0.4192 | 0 |
| Ridge | 10.0000 | 72.6114 | 5.5550 | 66.6630 | 0.1612 | 0 |
| Ridge | 100.0000 | 77.4393 | 5.6342 | 72.3441 | 0.0122 | 0 |
| Ridge | 1000.0000 | 78.0624 | 5.6380 | 73.1316 | -0.0095 | 0 |
| Lasso | 0.0010 | 55.3815 | 2.3676 | 53.8183 | 0.4533 | 0 |
| Lasso | 0.0100 | 55.3634 | 2.3251 | 53.6522 | 0.4567 | 0 |
| Lasso | 0.1000 | 55.5412 | 2.3888 | 52.8980 | 0.4719 | 3 |
| Lasso | 1.0000 | 62.7435 | 4.4760 | 58.3402 | 0.3576 | 7 |
| Lasso | 10.0000 | 78.1336 | 5.6383 | 73.2225 | -0.0120 | 10 |
| Lasso | 100.0000 | 78.1336 | 5.6383 | 73.2225 | -0.0120 | 10 |
| Lasso | 1000.0000 | 78.1336 | 5.6383 | 73.2225 | -0.0120 | 10 |

## Saved tables
- results/tables/regularized_results.csv
- results/tables/all_results.csv
- results/tables/coef_comparison.csv

## Saved figures
- results/figures/alpha_vs_cv_rmse.png
- results/figures/alpha_vs_test_rmse.png
- results/figures/alpha_vs_test_r2.png
- results/figures/coef_paths.png

## Observation
No alpha gave a clear improvement over the baseline. Performance degraded as alpha grew, Ridge shrank coefficients smoothly, and Lasso removed features.

## Environment
python=3.14.2; platform=Windows-11-10.0.26200-SP0; numpy=2.5.3; pandas=3.0.6; sklearn=1.9.1; scipy=1.18.1; matplotlib=3.11.2
