#!/usr/bin/env sh

echo "Deploying Production model name=Diabetes_RFCmodel"

# Set enviorment variable for the tracking URL where the Model Registry is
export MLFLOW_TRACKING_URI=http://localhost:5000
# Serve the production model from the model registry
mlflow models serve --model-uri models:/Diabetes_RFCmodel/production --no-conda
