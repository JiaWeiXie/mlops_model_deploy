import os

import bentoml
import mlflow

os.environ.setdefault("MLFLOW_S3_ENDPOINT_URL", "http://localhost:9000")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "mladmin")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "MLadminPassword")

mlflow.set_tracking_uri("http://localhost:5050")
mlflow.set_experiment("logi_clf")

model_uri = 'runs:/345ddd1b8e3240f79b6819e8c194b31a/sklearn-model'
logi_clf_model = mlflow.sklearn.load_model(model_uri)
model_tmp_path = f"/tmp/{logi_clf_model}"
mlflow.sklearn.save_model(logi_clf_model, model_tmp_path)
new_model = bentoml.mlflow.import_model("logi_clf_model", model_uri=model_tmp_path)
# saved_model = bentoml.sklearn.save_model("iris_clf", clf)