from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load travel data
travel_data = pd.read_csv('travel_2.csv')


def recommend_cities(state, attractions, climate, ratings):
    state = state.strip().title()  # Convert to title case and remove whitespace
    state_data = travel_data[travel_data['State'] == state]

    # Calculate scores for each city based on user preferences
    state_data['Score'] = attractions * state_data['Attractions'] + climate * state_data['Climate'] + ratings * \
                          state_data['Ratings']

    # Sort cities based on scores in descending order
    state_data = state_data.sort_values(by='Score', ascending=False)

    recommended_cities = state_data['City'].tolist()[:8]  # Return top 5 recommended cities
    return recommended_cities


@app.route('/recommend', methods=['POST'])
def get_recommendations():
    state = request.form['state']
    attractions = float(request.form['attractions'])
    climate = float(request.form['climate'])
    ratings = float(request.form['ratings'])

    recommended_cities = recommend_cities(state, attractions, climate, ratings)

    return jsonify(recommended_cities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
