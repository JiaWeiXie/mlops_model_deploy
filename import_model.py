import os

import bentoml
import mlflow


MLFLOW_TRACKING_URL = os.getenv("MLFLOW_TRACKING_URL")
MLFLOW_MODEL_URI = os.getenv("MLFLOW_MODEL_URI")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URL)

logi_clf_model = mlflow.sklearn.load_model(MLFLOW_MODEL_URI)

print(f"Loaded sklearn model: {logi_clf_model}.")
model_tmp_path = f"/tmp/{logi_clf_model}"
mlflow.sklearn.save_model(logi_clf_model, model_tmp_path)
print(f"Saved sklearn model to local.")
bentoml_model = bentoml.mlflow.import_model("logi_clf_model", model_uri=model_tmp_path)
print(f"Import sklearn model to bentoml model: {bentoml_model}.")
# saved_model = bentoml.sklearn.save_model("iris_clf", clf)