import os
import bentoml
import mlflow


# 從環境變數取得 MLflow 相關設定參數
MLFLOW_TRACKING_URL = os.getenv("MLFLOW_TRACKING_URL")
MLFLOW_MODEL_URI = os.getenv("MLFLOW_MODEL_URI")
# 設定 MLflow tracking server 網址
mlflow.set_tracking_uri(MLFLOW_TRACKING_URL)
# 載入遠端儲存的模型
logi_clf_model = mlflow.sklearn.load_model(MLFLOW_MODEL_URI)
print(f"Loaded sklearn model: {logi_clf_model}.")
# 宣告模型暫存路徑
model_tmp_path = f"/tmp/{logi_clf_model}"
# 儲存模型到暫存路徑
mlflow.sklearn.save_model(logi_clf_model, model_tmp_path)
print(f"Saved sklearn model to local.")
# 從暫存路徑匯入模型到 BentoML 工作目錄
bentoml_model = bentoml.mlflow.import_model("logi_clf_model", model_uri=model_tmp_path)
print(f"Import sklearn model to bentoml model: {bentoml_model}.")
# saved_model = bentoml.sklearn.save_model("iris_clf", clf)