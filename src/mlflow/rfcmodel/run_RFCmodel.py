import os
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import boto3
from tqdm import tqdm
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)


if __name__ == '__main__':
    mlflow.set_tracking_uri(
        "http://localhost:5000"
    )

    test_size_value = 0.25

    dataset = pd.read_csv('diabetes.csv', sep=',')

    dataset.columns.difference(['Outcome'])
    x_train, x_test, y_train, y_test = train_test_split(dataset.loc[:, dataset.columns.difference(['Outcome'])],
                                                        dataset.loc[:, 'Outcome'].values, test_size=test_size_value,
                                                        shuffle=True)

    n_estimators_range = np.arange(100, 500, 100)
    max_depth_range = np.arange(1, 25, 8)
    max_features_range = ["sqrt", None, "log2"]

    experiment_id = mlflow.set_experiment(experiment_name='rfcmodel_training-experiment')

    for n_estimators in tqdm(n_estimators_range):
        for max_depth in tqdm(max_depth_range, leave=False):
            for max_features in tqdm(max_features_range, leave=False):
                with mlflow.start_run(experiment_id=experiment_id):
                    model = RandomForestClassifier(
                        n_estimators=n_estimators,
                        max_depth=max_depth,
                        max_features=max_features,
                        n_jobs=3,
                    )

                    model.fit(x_train, y_train)
                    y_pred = model.predict(x_test)

                    accuracy = accuracy_score(y_test, y_pred)
                    precision = precision_score(y_test, y_pred)
                    recall = recall_score(y_test, y_pred)
                    f1 = f1_score(y_test, y_pred)
                    auc = roc_auc_score(y_test, y_pred)

                    mlflow.log_param("n_estimators", n_estimators)
                    mlflow.log_param("max_depth", max_depth)
                    mlflow.log_param("max_features", max_features)

                    mlflow.log_metric("accuracy", accuracy)
                    mlflow.log_metric("precision", precision)
                    mlflow.log_metric("recall", recall)
                    mlflow.log_metric("f1", f1)
                    mlflow.log_metric("auc", auc)

                    mlflow.sklearn.log_model(model, "rfcmodel")
