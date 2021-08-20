import requests
import pandas as pd

url = 'http://127.0.0.1:5000/invocations'
headers = {'Content-Type': 'application/json; format=pandas-records'}
dataset = pd.read_csv('diabetes.csv', sep=',')
del dataset['Outcome']
request_data = dataset.to_json(orient='records')
if __name__ == '__main__':
    try:
        response = requests.post(url, request_data, headers=headers)
        print(response.content)
    except Exception as ex:
        raise (ex)
