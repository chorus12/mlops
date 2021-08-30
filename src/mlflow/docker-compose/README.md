# MLflow On-Premise Deployment using Docker Compose
Easily deploy an MLflow tracking server with docker-compose.

MinIO S3 is used as the artifact store and MySQL server is used as the backend store.

## How to run

1. Clone(download) this repository

    ```bash
    git clone https://github.com/chorus12/mlops
    ```
    
2. `cd` into the `docker-compose` directory

3. Build and run the containers with `docker-compose`

    ```bash
    docker-compose build
    docker-compose up -d
    ```
    
4. Access MLflow and minio UI with:
 - `http://<mlflow server>`
 - `http://<mlflow server>:9000`

Important note: pay attention to `<mlflow server>`. If you run locally - it will be just a localhost, otherwise - ip address or actual server name. 

## Containerization

The MLflow tracking server is composed of 4 docker containers:

* MLflow server
* MinIO object storage server
* MySQL database server
* NGINX reverse proxy

## Usage Example
    
You interact with tracking server via mlflow cli tools. So on your client machine you need to install mlflow python package.  
The thing is that mlflow cli and server are the same and come bundled in one package.  

1. Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)

2. Install MLflow with extra dependencies, including scikit-learn

    ```bash
    pip install mlflow
   pip install scikit-learn
    ```
    
3. Set environmental variables (important)

    ```bash
    export MLFLOW_TRACKING_URI=http://<mlflow server>
    export MLFLOW_S3_ENDPOINT_URL=http://<mlflow server>:9000
    ```
4. Set MinIO credentials
    
    ```bash
    cat > ~/.aws/credentials <<EOF
    [default]
    aws_access_key_id=minio
    aws_secret_access_key=mimino123
    EOF
    ```
If you change the `aws_secret_access_key` in `.env` file - make appropriate change in `credentials` file.

5. Train a sample MLflow model

    ```bash
    mlflow run https://github.com/plaguedoctor39/mlflowproject-test -P depth=5
    ```
    
    * Note: To fix ModuleNotFoundError: No module named 'boto3'
    
        ```bash
        #Switch to the conda env
        conda env list
        conda activate mlflow-3eee9bd7a0713cf80a17bc0a4d659bc9c549efac #replace with your own generated mlflow-environment
        pip install boto3
        ```
    * Or you can try running:  
    ```bash
    mlflow run https://github.com/plaguedoctor39/mlflowproject-test -P depth=5 --no-conda
    ```
    if you have all dependencies in current environment.
 
 6. Serve the model (replace with your model's actual path)
    ```bash
    mlflow models serve -m S3://mlflow/0/98bdf6ec158145908af39f86156c347f/artifacts/model -p 1234
    ```
    * Note: model is served locally on client. 
 
 7. You can check the input with this command
    ```bash
    curl -X POST -H "Content-Type:application/json" --data '[{"Pregnancies": 6, "Glucose": 148, "BloodPressure": 72, "SkinThickness": 35, "Insulin": 0, "BMI": 33.6, "DiabetesPedigreeFunction": 0.627, "Age": 50}]' http://127.0.0.1:1234/invocations
    ```
