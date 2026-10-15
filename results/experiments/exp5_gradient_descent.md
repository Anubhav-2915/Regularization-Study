# exp5_gradient_descent: Linear regression by gradient descent vs sklearn
_Saved: 2026-10-13T01:30:51_

## Dataset
- **name:** sklearn load_diabetes
- **n_train:** 353
- **n_test:** 89

## Preprocessing
StandardScaler fitted on the training rows only, applied to train and test; target left unscaled

## Random seed(s)
- **train_test_split:** 42

## Models and hyperparameters
- **gradient_descent:** learning_rate=0.1; iterations=10000; init=zeros; loss=MSE
- **sklearn_LinearRegression:** default, same standardized data
- **learning_rates_tested:** 0.001, 0.01, 0.1, 0.2, 0.3

## Train/test protocol
Same 80/20 split as the baseline (random_state=42)

## Cross-validation protocol
not applicable: no hyperparameter selection; learning rate and iterations set by hand

## Metrics
| train_MSE | test_RMSE | test_R2 |
|---|---|---|
| 2868.5497 | 53.8534 | 0.4526 |
| 2868.5497 | 53.8534 | 0.4526 |

## Saved tables
- results/tables/gd_vs_sklearn_coefficients.csv
- results/tables/gd_vs_sklearn_metrics.csv

## Saved figures
- results/figures/gd_loss_curve.png
- results/figures/gd_coef_distance.png
- results/figures/gd_learning_rates.png

## Observation
Gradient descent reached essentially the same solution and test performance as sklearn. Coefficients converged more slowly than the loss because of correlated features, and learning rates above the stability limit diverged.

## Environment
python=3.14.2; platform=Windows-11-10.0.26200-SP0; numpy=2.5.3; pandas=3.0.6; sklearn=1.9.1; scipy=1.18.1; matplotlib=3.11.2
