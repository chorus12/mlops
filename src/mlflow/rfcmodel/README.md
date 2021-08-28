Setup environment
----------------------------------

1. ```git clone https://github.com/chorus12/mlops ```
2. `cd src/mlflow/rfcmodel`
3. Install MLflow and the required Python modules within your [conda activated environment](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) or [pipenv environment](https://pypi.org/project/pipenv) if using it
    * `pip install -r requirements.txt` or `pip3 install -r requirements.txt`

Stage 1 - Train and Track the model
-------------------

1. `python run_RFCmodel.py`
2. launch `mlflow ui`
3. Got to `http://127.0.0.1:5000`
4. Pick the best model, register with Model Registry as `Diabetes_RFCmodel`
5. Choose second best model and create version 2 in the Model Registry
   * Transition the best model into `Production`
   * Transition the second best model into `Staging`

Stage 2 - Deploy and make predictions
-------------------
 
Let's take our production model from our Model Registry and [deploy and serve models](https://www.mlflow.org/docs/latest/models.html#deploy-mlflow-models) locally as a REST endpoint to a server launched by MLflow CLI. 

1. From the same directory run:
    * ```./deploy_model.sh``` 
    This launches a gunicorn server serving at the localhost `127.0.0.1:5000`. Now you can score locally
    on the deployed produciton model as a REST point.
 
2. From another terminal send a POST request with our JSON payload
    * ```python make_predictions.py```
