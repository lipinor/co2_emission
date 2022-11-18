# CO2 Emission Prediction
## Project Description
Since 1995, the Government of Canada provides model-specific fuel consumption ratings and estimated carbon dioxide (CO2) emissions for new light-duty vehicles for retail sale in the country. This data can be obtained in the canadian government [website](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64). 

This project aims to create a model capable of predicting a vehicle's estimated CO2 emission in units of g/km, based on the properties provided in the dataset. The data used ranges from the years of 2018 to 2022.

## Instructions
The co2_emission.ipynb file contains: 
- Data preparation and data clearning
- EDA, feature importance analysis
- Model selection process and parameter tuning

### Installing dependencies
To reproduce this project on your system, you need to download the code and install the dependencies using pipenv. 

If you don't have pipenv installed, you can just install it using the following command:
```
pip install pipenv
```
With pipenv, you can create a virtual environment with the needed packages installed using the following command while in the project folder:
```
pipenv install
```
When all the dependencies are installed, the virtual environment can be activated with:
```
pipenv shell
```
Then, you can run the train.py to create a file contaning the saved model:
```
python train.py
```
To host the service locally, just run the predict.py file:
```
python predict.py
```
### Making a prediction
Finally, you can use the model to make a prediction by creating a script/notebook with the example code below. Pay attention for the type of each sample. The co2_prediction.ipynb contains this code, and the serving.png image shows an screenshot of an interaction with the model:
```python
import requests

vehicle = {
    'model year': '2022', # string
    'make': 'Ford', # string
    'vehicle class': 'SUV: Standard', # string
    'engine size (l)': 2.3, # float
    'cylinders': '4', # string
    'transmission': 'AS10', # string 
    'fuel type': 'X', # string
    'fuel consumption comb (l/100 km)': 11.5, # float 
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=vehicle)
result = response.json()
print(result)
```

The co2_emission.ipynb contains information about the possible entries for each feature. You can also find this same info in the canadian government [website](https://open.canada.ca/data/en/dataset/98f1a129-f628-4ce4-b24d-6f16bf24dd64). 

### Deployment using Docker
You can deploy this file using docker. First, you need to create a docker image using the Dockerfile. This can be done by running this command in the project folder:
```
docker build -t co2_emission .
```
Now, just use the command below and the model will be served in your local host, and you can make a prediction in the same way as explained above. 
```
docker run -it -p 9696:9696 co2_prediction:latest
```
