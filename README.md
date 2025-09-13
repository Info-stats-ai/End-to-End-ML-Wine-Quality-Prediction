### End-to-End ML: Wine Quality Prediction

A modular, production-style ML pipeline to predict wine quality using the UCI Wine Quality (red) dataset. The project includes data pipelines, model training and evaluation, a Flask web app for inference, and Docker support.

## Features
- **Data ingestion**: Download and extract dataset
- **Data validation**: Basic checks and status reporting
- **Data transformation**: Split, preprocess, and feature engineer
- **Model training**: Train scikit-learn model with saved artifact
- **Model evaluation**: Metrics persisted to `artifacts/model_evaluation/metrics.json`
- **Inference API/UI**: Flask app with `/predict` and simple HTML forms
- **Config-driven**: All paths and settings in `config/config.yaml`
- **Dockerized**: Container build and run supported

## Project Structure
```text
datascienceproject/
  app.py                  # Flask app (train + predict endpoints)
  main.py                 # Orchestrates all pipeline stages
  config/config.yaml      # Pipeline configuration
  params.yaml             # (Optional) model hyperparameters
  schema.yaml             # Input schema description
  src/datascience/        # Code: components, configs, pipelines, utils
  artifacts/              # Auto-generated artifacts (data, model, metrics)
  templates/              # HTML templates for the web UI
  requirements.txt        # Python dependencies
  Dockerfile              # Container build file
```

## Quickstart
### 1) Environment setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2) Configure
Edit `config/config.yaml` if needed (download URL, artifact locations, etc.). Key sections include `data_ingestion`, `data_validation`, `data_transformation`, `model_trainer`, and `model_evaluation`.

Optionally adjust `params.yaml` and `schema.yaml` to tune hyperparameters and data schema.

### 3) Train the pipeline
```bash
python main.py
```
This will run stages in order: Data Ingestion → Data Validation → Data Transformation → Model Trainer → Model Evaluation.

Artifacts of interest:
- Trained model: `artifacts/model_trainer/model.joblib`
- Metrics: `artifacts/model_evaluation/metrics.json`
- Logs: `logs/logging.log`

### 4) Run the web app (inference)
```bash
python app.py
```
Open `http://localhost:8080` to access the UI. You can also trigger training from the app at `/train`.

Sample API call for prediction (form data):
```bash
curl -X POST http://localhost:8080/predict \
  -d fixed_acidity=7.4 \
  -d volatile_acidity=0.70 \
  -d citric_acid=0.00 \
  -d residual_sugar=1.9 \
  -d chlorides=0.076 \
  -d free_sulfur_dioxide=11 \
  -d total_sulfur_dioxide=34 \
  -d density=0.9978 \
  -d pH=3.51 \
  -d sulphates=0.56 \
  -d alcohol=9.4
```

## Docker
Build and run the containerized app (serves the Flask UI):
```bash
docker build -t wine-quality-app .
docker run --rm -p 8080:8080 wine-quality-app
```

## Configuration Reference
- `config/config.yaml`
  - `data_ingestion.source_URL`: Dataset ZIP URL
  - `data_ingestion.unzip_dir`: Extract location
  - `data_validation.STATUS_FILE`: Validation status output
  - `data_transformation.data_path`: Raw CSV for transformation
  - `model_trainer.*`: Train/test paths and model name
  - `model_evaluation.metric_file_name`: Metrics output path
- `params.yaml`: Model hyperparameters (if used by trainer)
- `schema.yaml`: Expected columns and basic constraints

## Notes
- Dataset used: Wine Quality (red). By default, it is downloaded automatically from the configured URL.
- For experiment tracking, you can integrate MLflow (mentioned in requirements). Metrics are also written to JSON for easy inspection.

## License
See `LICENSE` for details.

## Acknowledgements
- UCI Machine Learning Repository – Wine Quality Dataset

## Dataset and Schema
This project uses the Wine Quality (red) dataset. The schema is defined in `schema.yaml` and enforced during validation.

- **Target column**: `quality` (integer)
- **Feature columns** (all numeric floats):
  - `fixed acidity`, `volatile acidity`, `citric acid`, `residual sugar`, `chlorides`, `free sulfur dioxide`, `total sulfur dioxide`, `density`, `pH`, `sulphates`, `alcohol`

Ensure incoming data matches these names exactly; column mismatches will fail validation.

## Pipeline Stages (What each does and produces)
### 1) Data Ingestion
- Downloads ZIP from `config.data_ingestion.source_URL` to `config.data_ingestion.local_data_file`.
- Extracts into `config.data_ingestion.unzip_dir`.
- Expected extracted CSV: `artifacts/data_ingestion/winequality-red.csv`.

### 2) Data Validation
- Reads extracted CSV and compares columns to `schema.yaml:COLUMNS`.
- Writes validation status to `artifacts/data_validation/status.txt`.

### 3) Data Transformation
- Performs a random train/test split using `sklearn.model_selection.train_test_split`.
- Outputs `train.csv` and `test.csv` under `artifacts/data_transformation/`.
- Note: No scaler/encoder is applied by default; add inside `components/data_transformation.py` if needed.

### 4) Model Training
- Algorithm: `ElasticNet` (scikit-learn).
- Hyperparameters read from `params.yaml → ElasticNet` (defaults: `alpha=0.2`, `l1_ratio=0.1`).
- Target configured via `schema.yaml → TARGET_COLUMN.name` (`quality`).
- Saves trained model to `artifacts/model_trainer/model.joblib`.

### 5) Model Evaluation
- Computes `RMSE`, `MAE`, `R2` on test set and stores results in `artifacts/model_evaluation/metrics.json`.
- Optionally logs params/metrics/model to MLflow using `ModelEvaluationConfig.mlflow_uri`.

## Artifacts Layout
```text
artifacts/
  data_ingestion/
    data.zip
    winequality-red.csv
  data_validation/
    status.txt
  data_transformation/
    train.csv
    test.csv
  model_trainer/
    model.joblib
  model_evaluation/
    metrics.json
```

## API and Prediction Contract
The Flask app expects 11 numeric fields in a form POST to `/predict`:

- `fixed_acidity`, `volatile_acidity`, `citric_acid`, `residual_sugar`, `chlorides`, `free_sulfur_dioxide`, `total_sulfur_dioxide`, `density`, `pH`, `sulphates`, `alcohol`

Order is handled in the app, but names must match exactly. The app loads the trained model from `artifacts/model_trainer/model.joblib`. Train at least once before predicting.

Endpoints:
- `GET /` → Home page
- `GET /train` → Triggers `python main.py` to run full pipeline
- `POST /predict` → Returns prediction rendered in `templates/results.html`

## Customization Guide
- **Change hyperparameters**: edit `params.yaml → ElasticNet`.
- **Add preprocessing**: implement in `src/datascience/components/data_transformation.py` and persist any fitted transformers (e.g., via `joblib`).
- **Control split**: modify `train_test_split` arguments (e.g., `test_size`, `random_state`) in `data_transformation.py` for reproducibility.
- **Swap model**: update `components/model_trainer.py` and `ModelTrainerConfig` to use a different estimator; reflect params in `params.yaml`.
- **Extend validation**: add checks (nulls, ranges, dtypes) in `components/data_validation.py`.

## MLflow and Experiment Tracking
The evaluation step supports MLflow logging.

- Default tracking URI is set in `ConfigurationManager.get_model_evaluation_config()`.
- To use a remote MLflow server, set credentials/URI appropriately (e.g., environment variables) and ensure network access.
- Logged items: parameters (`alpha`, `l1_ratio`), metrics (`rmse`, `mae`, `r2`), and the model artifact.

## Troubleshooting
- **Download fails**: Check `config.data_ingestion.source_URL`, network connectivity, and that GitHub raw link is reachable.
- **Validation status false**: Confirm CSV column names match `schema.yaml` exactly (including spaces and case).
- **Model not found**: Run training (`python main.py` or `/train`) to create `model.joblib` before calling `/predict`.
- **Port already in use**: Change the port in `app.py` or free `8080`.
- **Non-deterministic results**: Set `random_state` in `train_test_split` and the estimator for reproducibility.

## Development Tips
- Run notebooks in `research/` for quick experimentation before integrating into components.
- Keep configuration in YAMLs; avoid hardcoded paths in code.
- Write small, composable functions inside components; prefer pure functions for easier testing.
