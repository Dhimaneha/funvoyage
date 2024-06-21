from flask import Flask, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)


df = pd.read_csv('Description.csv')


def get_city_description(city):
    city_data = df[df['city'] == city]
    if len(city_data) == 0:
        return "City not found in the dataset."
    else:
        return city_data['description'].values[0]

with open('get_city_description.pkl', 'wb') as f:
    pickle.dump(get_city_description, f)

@app.route('/recommend', methods=['POST'])
def predict():
    city_name = request.form.get('city')
    if city_name is None:
        return jsonify({'error': 'City name is required.'}), 400

    with open('get_city_description.pkl', 'rb') as f:
        get_description = pickle.load(f)

    description = get_description(city_name)
    return jsonify({'description': description})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
