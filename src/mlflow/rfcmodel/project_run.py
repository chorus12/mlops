import os
import sys

import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
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

    depth = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1] % 1 == 0) else 1
    with mlflow.start_run():
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=depth,
            max_features='log2',
            n_jobs=3,
        )

        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred)

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("max_features", 'log2')

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("auc", auc)

        mlflow.sklearn.log_model(model, "rfcmodel")
