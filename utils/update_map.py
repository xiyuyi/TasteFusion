import numpy as np
import folium

from tastefusion.mock_utils.mock_get_location_coordinates import mock_retrieve_coords


def update_map(restaurant_coordinates:list = None,
               mock=False,
               filtered_restaurants_df=None):
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
    if filtered_restaurants_df is None:
        m = folium.Map(location=center, zoom_start=15)
        for coord in restaurant_coordinates:
            folium.Marker(
                location=coord,
                icon=folium.Icon(icon="cloud"),
            ).add_to(m)
        map_html = m._repr_html_()
    else:
        m = folium.Map(location=center, zoom_start=15)
        for index, row in filtered_restaurants_df.iterrows():

            lat = row['latitude']
            lon = row['longitude']
            name = row['name']
            rec_foods = row['10 tags for food categories'],
            good_aspects = row['good aspects (2)'],
            print('-------- types --------')
            print(type(name))
            print(type(rec_foods[0]))
            print(len(rec_foods[0]))
            text = f"""
            <div style="font-family: Arial, sans-serif; margin: 10px;">
                <strong>NAME: {name}</strong><br><br>
                <strong>Recommended foods:</strong><br>
                {rec_foods[0][0]}<br>
                {rec_foods[0][1]}<br>
                {rec_foods[0][2]}<br><br>
                <strong>Good aspects:</strong><br>
                {good_aspects[0][1]}
            </div>
            """

            # Now use this HTML string in the Popup
            folium.Marker(
                [lat, lon],
                popup=folium.Popup(text, max_width=300),  # Set the max_width as per your requirement
                tooltip=name  # Tooltip shown on hover
            ).add_to(m)

        map_html = m._repr_html_()
    return map_html
