import numpy as np

import bentoml
from bentoml.io import NumpyNdarray

logi_clf_runner = bentoml.mlflow.get("logi_clf_model:latest").to_runner()

svc = bentoml.Service("logi_clf", runners=[logi_clf_runner])

arr = [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]
input_spec = NumpyNdarray.from_sample(np.array([arr]))

@svc.api(
    input=input_spec,
    output=NumpyNdarray(),
)
def classify(input_series: np.ndarray) -> np.ndarray:
    result = logi_clf_runner.predict.run(input_series)
    return result