import numpy as np
import folium

from tastefusion.mock_utils.mock_get_location_coordinates import mock_retrieve_coords


def update_map(restaurant_coordinates:list = None, mock=False):
    """
    This function will update the map_html with new marks
    reflecting the restaurant_coordinates (list of longitudes and latitudes of restaurant pool)


    :param restaurant_coordinates:
    :return:
    """
    # retrieve longitute/lattitute from restaurants based on their ids.
    if mock:
        # in mock mode, it will just randomly shift the map around San Francisco
        san_francisco_coords = [37.7749, -122.4194]
        coords = mock_retrieve_coords(*san_francisco_coords, 3)
        m = folium.Map(location=coords, zoom_start=11)
        # Convert the map to HTML string
        map_html = m._repr_html_()
        return map_html

    """
    when mock is False, this will create a map centered at all the location coordiantes
    makr the locations with Glyphs, and return the new map_html 
    """
    center = list(np.mean(restaurant_coordinates, axis=0))
    m = folium.Map(location=center, zoom_start=15)
    for coord in restaurant_coordinates:
        folium.Marker(
            location=coord,
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)
    map_html = m._repr_html_()
    return map_html
