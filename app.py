from flask import Flask, render_template, jsonify
from folium import folium

from utils.get_location_coordinates import get_location_coordinates
from utils.update_map import update_map
from utils.update_restaurants import update_restaurants
from utils.update_tastes import generate_tastes

app = Flask(__name__)


@app.route('/')
def index():
    # Create a folium map centered around a location
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

    # Convert the map to HTML string
    map_html = m._repr_html_()
    return render_template('index.html', tastes=[], map_html=map_html)


@app.route('/taste-fusion', methods=['POST'])
def taste_fusion_clicked():
    """
    When the taste-fusion button is clicked. what happens?

    The program will take in the following info:
        1. The vote result of the existing tastes
        2. Current pool of restaurants and their information
    The program will calculate the following:
        1. Narrow down the pool of restaurants.
        2. Generate new taste tags and update the taste buttons.
        3. update the map html

    :return:
    """
    print('taste fusion button clicked!')
    # get current tastes.
    # get current restaurant ids.
    mock = True
    taste_votes = []  # todo, should retrieve data from the frontend.
    curr_ids = []  # todo, should retrieve data from the front end.
    # update the restaurant ids list based on the current taste votes and the current pool of restaurants.
    updated_restaurant_ids = update_restaurants(taste_votes=taste_votes,
                                                current_restaurant_ids=curr_ids,
                                                mock=mock)
    # retrieve the restaurant location coordinates.
    updated_restaurant_coordinates = get_location_coordinates(restaurant_ids=updated_restaurant_ids, mock=mock)

    # generate the updated map_html from folium
    map_html = update_map(restaurant_coordinates=updated_restaurant_coordinates, mock=False)

    # generate extra tastes tags based on the current list of restaurants
    tastes = generate_tastes(restaurant_ids=updated_restaurant_ids, mock=mock)
    return jsonify({"tastes": tastes, "map_html": map_html})


if __name__ == '__main__':
    app.run(debug=True)
