import folium

from tastefusion.utils.get_zoom_from_radius import get_zoom_from_radius


def center_map(coords: list = None, radius=None):
    """ this function creates an interactive folium map that is centered around the coords """
    if radius is None:
        zoom = 12
    else:
        zoom = get_zoom_from_radius(radius)
    m = folium.Map(location=coords, zoom_start=zoom)
    folium.Marker(
        location=coords,
        icon=folium.Icon(),
    ).add_to(m)
    # Convert the map to HTML string
    map_html = m._repr_html_()
    return map_html
