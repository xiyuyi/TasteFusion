from flask import Flask, render_template, jsonify, request
from folium import folium

from utils.center_map import center_map
from utils.get_coords_from_addresstext import get_coords_from_address_text
from utils.get_initial_restaurants import get_initial_restaurants
from utils.get_location_coordinates import get_location_coordinates
from utils.update_map import update_map
from utils.update_restaurants import update_restaurants
from utils.update_tastes import generate_tastes

app = Flask(__name__)


@app.route('/')
def index():
    # Create a folium map centered around the initial location San Francisco
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

    # Convert the map to HTML string
    map_html = m._repr_html_()
    return render_template('index.html', tastes=[' ']*10, map_html=map_html)


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
    # Get the taste data from the request payload
    tastes_data = request.json.get('tastes', [])

    # Separate the taste labels and votes for further processing
    taste_votes = {taste['label']: taste['value'] for taste in tastes_data}

    # get current restaurant ids.
    mock = True
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


@app.route('/search-start', methods=['POST'])
def search_button_clicked():
    """
    When the search button is clicked. what happens?

    The program will fetch the following info:
        1. location center
        2. location pool
        3. fetch restaurant info from database
    The program will calculate the following:
        1. get a ranked list of restaurants in the area
        2. Generate taste tags and initialize the taste buttons.
        3. update the map html

    :return:
    """
    print('Search button clicked!')
    # get current tastes.
    # get current restaurant ids.
    mock = True
    # Get the address and the radius from the request
    address = request.json.get('address')
    rad = request.json.get('radius')
    if rad:
        search_radius = int(rad)
    else:
        search_radius = 10  # default searching radius is 10 miles.
    center = get_coords_from_address_text(address=address, mock=False)

    # update the restaurant ids list based on the current taste votes and the current pool of restaurants.
    restaurant_ids = get_initial_restaurants(center=center,
                                             search_radius=search_radius,
                                             mock=mock)

    # retrieve the restaurant location coordinates.
    updated_restaurant_coordinates = \
        get_location_coordinates(restaurant_ids=restaurant_ids,
                                 mock=mock)

    # generate the updated map_html from folium
    map_html = update_map(restaurant_coordinates=updated_restaurant_coordinates,
                          mock=False)

    # generate tastes tags based on the current list of restaurants
    tastes = generate_tastes(restaurant_ids=restaurant_ids, mock=mock)
    return jsonify({"tastes": tastes, "map_html": map_html})


@app.route('/address-input', methods=['POST'])
def address_input():
    # Get the address from the request
    address = request.json.get('address')
    print('address input: '+address)

    coords = get_coords_from_address_text(address=address, mock=False)

    # Process the address to get updated map HTML (pseudo-logic here, replace with actual logic)
    map_html = center_map(coords)
    print('ready for map update')
    return jsonify({"map_html": map_html})


@app.route('/radius-input', methods=['POST'])
def radius_input():
    print('radius input route...')
    # Get the address and the radius from the request
    address = request.json.get('address')
    radius = request.json.get('radius')
    print('address input: '+address)
    print('radius input: '+radius+' miles')

    coords = get_coords_from_address_text(address=address, mock=False)

    # Process the address to get updated map HTML (pseudo-logic here, replace with actual logic)
    map_html = center_map(coords=coords, radius=radius)
    print('ready for map update')
    return jsonify({"map_html": map_html})


if __name__ == '__main__':
    app.run(debug=True)
