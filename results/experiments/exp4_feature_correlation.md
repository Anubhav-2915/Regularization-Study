# exp4_feature_correlation: Controlled feature-correlation study (synthetic)
_Saved: 2026-10-13T01:32:55_

## Dataset
- **type:** synthetic multivariate normal
- **n_train:** 100
- **n_test:** 2000
- **n_features:** 10
- **noise_sigma:** 5.0
- **true_beta:** 3.0, 2.0, 1.5, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0
- **rho_levels:** 0.0, 0.3, 0.6, 0.9

## Preprocessing
None (features generated with unit variance)

## Random seed(s)
- **train_seeds:** 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49
- **test_seed_offset:** 10000

## Models and hyperparameters
- **LinearRegression:** default
- **RidgeCV:** alphas=0.001, 0.01, 0.1, 1, 10, 100, 1000
- **LassoCV:** alphas=0.001, 0.01, 0.1, 1, 10, 100, 1000; max_iter=100000

## Train/test protocol
Fresh training set and independent large test set per seed and rho; same seeds reused across rho (paired)

## Cross-validation protocol
RidgeCV/LassoCV with 5-fold shuffled KFold (random_state = seed) on training data only

## Metrics
| model | rho | RMSE_mean | RMSE_std | R2_mean | R2_std | coef_error_mean | coef_error_std | coef_norm_mean | median_alpha | mean_zeros | mean_coef_std |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Lasso | 0.0000 | 5.3033 | 0.1714 | 0.3214 | 0.0481 | 1.6060 | 0.4992 | 3.8687 | 0.1000 | 1.7000 | 0.4993 |
| Lasso | 0.3000 | 5.2895 | 0.1368 | 0.4967 | 0.0286 | 1.6703 | 0.3906 | 3.9646 | 0.1000 | 2.0200 | 0.5156 |
| Lasso | 0.6000 | 5.2637 | 0.1320 | 0.6028 | 0.0206 | 2.0013 | 0.4827 | 4.0651 | 0.1000 | 2.4200 | 0.6165 |
| Lasso | 0.9000 | 5.2077 | 0.1229 | 0.6770 | 0.0160 | 3.2625 | 0.9267 | 4.4275 | 0.1000 | 3.9800 | 0.9828 |
| LinearRegression | 0.0000 | 5.3117 | 0.1388 | 0.3197 | 0.0358 | 1.6356 | 0.3624 | 4.3499 | None | 0.0000 | 0.5269 |
| LinearRegression | 0.3000 | 5.3117 | 0.1388 | 0.4925 | 0.0286 | 1.8745 | 0.4249 | 4.4248 | None | 0.0000 | 0.6043 |
| LinearRegression | 0.6000 | 5.3117 | 0.1388 | 0.5954 | 0.0237 | 2.4438 | 0.5560 | 4.6826 | None | 0.0000 | 0.7880 |
| LinearRegression | 0.9000 | 5.3117 | 0.1388 | 0.6638 | 0.0202 | 4.8337 | 1.1075 | 6.2457 | None | 0.0000 | 1.5588 |
| Ridge | 0.0000 | 5.2834 | 0.1330 | 0.3270 | 0.0334 | 1.5517 | 0.3565 | 3.8881 | 10.0000 | 0.0000 | 0.4810 |
| Ridge | 0.3000 | 5.2691 | 0.1279 | 0.5007 | 0.0258 | 1.7057 | 0.3549 | 3.9447 | 10.0000 | 0.0000 | 0.5227 |
| Ridge | 0.6000 | 5.2561 | 0.1211 | 0.6039 | 0.0199 | 2.1026 | 0.4319 | 3.8277 | 10.0000 | 0.0000 | 0.6138 |
| Ridge | 0.9000 | 5.1675 | 0.1030 | 0.6820 | 0.0142 | 2.9203 | 0.6311 | 3.6174 | 10.0000 | 0.0000 | 0.7464 |

## Saved tables
- results/tables/feature_corr_raw.csv
- results/tables/feature_corr_summary.csv

## Saved figures
- results/figures/corr_coef_variability.png
- results/figures/corr_coef_error.png
- results/figures/corr_coef_norm.png
- results/figures/corr_test_rmse.png
- results/figures/corr_test_r2.png

## Observation
OLS coefficients became much less stable as correlation increased while its predictions did not change. Ridge and Lasso reduced the instability, Ridge more than Lasso, at the cost of shrinkage bias, and neither recovered the true sparse structure.

## Environment
python=3.14.2; platform=Windows-11-10.0.26200-SP0; numpy=2.5.3; pandas=3.0.6; sklearn=1.9.1; scipy=1.18.1; matplotlib=3.11.2
