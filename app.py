from flask import Flask, render_template, jsonify, request
from flask_caching import Cache
from folium import folium
import socket
import os

from tastefusion.utils.center_map import center_map
from tastefusion.utils.get_coords_from_addresstext import get_coords_from_address_text
from tastefusion.utils.get_initial_restaurants import get_initial_restaurants
from tastefusion.utils.get_location_coordinates import get_location_coordinates
from tastefusion.utils.update_map import update_map
from tastefusion.utils.update_restaurants import update_restaurants
from tastefusion.utils.update_tastes import generate_tastes

path_to_data_folder = os.path.join(os.path.dirname(__file__), 'data')

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def __init__(self):
    self.app = Flask(__name__)
    self.configure_routes()
    self.current_restaurant_ids = []


@app.route('/')
def index():
    # Create a folium map centered around the initial location Reno
    m = folium.Map(location=[39.5296, -119.8138], zoom_start=13)

    # Convert the map to HTML string
    map_html = m._repr_html_()
    return render_template('index.html', tastes=[' '] * 14, map_html=map_html)


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
    print(type(taste_votes))
    restaurants_df = cache.get('restaurants_df')
    tastes = cache.get('tastes')
    initial_search = cache.get('initial_search')
    filtered_restaurants_df = cache.get('filtered_restaurants_df')

    if initial_search:
        print('this is the initial search')
        current_restaurant_df = restaurants_df
        cache.set('initial_search', False)
    else:
        print('update current restaurant_df by the filtered one')
        current_restaurant_df = filtered_restaurants_df
        print('length of current_restaurant_df = ' + str(len(current_restaurant_df)))

    # update the restaurant dataframe list based on the current taste votes and the current pool of restaurants.
    filtered_restaurants_df = update_restaurants(taste_votes=taste_votes,
                                                 current_restaurant_df=current_restaurant_df,
                                                 mock=False)
    print('after filtered_restaurans_df, length is ' + str(len(filtered_restaurants_df)))
    cache.set('filtered_restaurants_df', filtered_restaurants_df)

    # retrieve the restaurant location coordinates.
    updated_restaurant_coordinates \
        = get_location_coordinates(restaurant_df=filtered_restaurants_df,
                                   mock=False)

    # generate the updated map_html from folium
    map_html \
        = update_map(restaurant_coordinates=updated_restaurant_coordinates,
                     filtered_restaurants_df=filtered_restaurants_df,
                     mock=False)
    # generate extra tastes tags based on the current list of restaurants
    tastes = generate_tastes(restaurant_df=filtered_restaurants_df,
                             mock=False,
                             existing_taste_votes=taste_votes,
                             initial_search=False)

    # now update the webpage. use only to 14 taste tags
    return jsonify({"tastes": tastes[:14], "map_html": map_html})


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
        search_radius = float(rad)
    else:
        search_radius = 10  # default searching radius is 10 miles.
    center = get_coords_from_address_text(address=address, mock=mock)

    # retrieve the dataframe about the current restaurant pool
    restaurants_df = get_initial_restaurants(center=center,
                                             search_radius=search_radius,
                                             mock=True,
                                             datapath=path_to_data_folder)
    # retrieve the restaurant location coordinates.
    updated_restaurant_coordinates = \
        get_location_coordinates(restaurant_df=restaurants_df,
                                 mock=False)

    # generate the updated map_html from folium
    map_html = update_map(restaurant_coordinates=updated_restaurant_coordinates,
                          mock=False)

    # generate tastes tags based on the current list of restaurants
    tastes = generate_tastes(restaurant_df=restaurants_df, mock=False)

    cache.set('restaurants_df', restaurants_df)
    cache.set('tastes', tastes)
    cache.set('initial_search', True)

    # now update the webpage. use only to 14 taste tags
    return jsonify({"tastes": tastes[:14], "map_html": map_html})


@app.route('/address-input', methods=['POST'])
def address_input():
    # Get the address from the request
    address = request.json.get('address')
    print('address input: ' + address)

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
    print('address input: ' + address)
    print('radius input: ' + radius + ' miles')

    coords = get_coords_from_address_text(address=address, mock=False)

    # Process the address to get updated map HTML (pseudo-logic here, replace with actual logic)
    map_html = center_map(coords=coords, radius=radius)
    print('ready for map update')
    return jsonify({"map_html": map_html})


def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return port


if __name__ == '__main__':
    port = find_free_port()
    app.run(debug=True, port=port)
