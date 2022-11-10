from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

def predict_single(vehicle, model):
    vehicle = pd.DataFrame(vehicle, index=[0])
    y_pred = model.predict(vehicle)
    return y_pred


with open('co2_model.bin', 'rb') as f_in:
    model = pickle.load((f_in))

app = Flask('co2_emission')

@app.route('/predict', methods=['POST'])
def predict():
    vehicle = request.get_json()

    prediction = predict_single(vehicle, model)

    result = {
              'CO2 emission (g/km)': float(prediction)
             }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)