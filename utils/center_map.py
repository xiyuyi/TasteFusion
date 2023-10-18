import folium


def center_map(coords):
    """ this function creates an interactive folium map that is centered around the coords """
    m = folium.Map(location=coords, zoom_start=12)
    folium.Marker(
        location=coords,
        icon=folium.Icon(),
    ).add_to(m)
    # Convert the map to HTML string
    map_html = m._repr_html_()
    return map_html
