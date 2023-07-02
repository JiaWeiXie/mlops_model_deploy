from sklearn import datasets

dataset = datasets.load_breast_cancer(as_frame=True)

print(dataset.data.iloc[0].to_list())