from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import pandas as pd
import pickle

app = Flask(__name__)

model_path = 'model/parking_model.pkl'
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/predict', methods=['POST'])
def predict_single_date():
    data = request.get_json()
    date_str = data.get('date')

    if not date_str:
        return jsonify({'error': 'No date provided'}), 400

    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    hour = date.hour
    day = date.day
    weekday = date.weekday()

    if hour < 8 or hour > 17:
        return jsonify({'error': 'Date hour must be between 8 and 17'}), 400

    features = pd.DataFrame([[day, hour, weekday]], columns=['Day', 'Hour', 'Weekday'])
    prediction = model.predict(features)[0]

    return jsonify({'occupancy': prediction})


@app.route('/predict/interval', methods=['POST'])
def predict_interval():
    data = request.get_json()
    start_str = data.get('start')
    end_str = data.get('end')

    if not start_str or not end_str:
        return jsonify({'error': 'Start date or end date missing'}), 400

    try:
        start_date = datetime.fromisoformat(start_str)
        end_date = datetime.fromisoformat(end_str)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    if start_date > end_date:
        return jsonify({'error': 'Start date must be before end date'}), 400

    if start_date.hour < 8 or end_date.hour > 17:
        return jsonify({'error': 'Date hour must be between 8 and 17'}), 400

    predictions = {}
    current_date = start_date
    while current_date <= end_date:
        prediction = get_predictions_from_date(current_date)
        predictions[current_date.isoformat()] = prediction
        current_date += timedelta(hours=1)

    return jsonify(predictions)


def get_predictions_from_date(date):
    hour = date.hour
    day = date.day
    weekday = date.weekday()

    features = pd.DataFrame([[day, hour, weekday]], columns=['Day', 'Hour', 'Weekday'])
    return model.predict(features)[0]


if __name__ == '__main__':
    app.run()
