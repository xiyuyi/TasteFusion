from mock_utils.mock_get_location_coordinates import mock_retrieve_coords


def get_location_coordinates(restaurant_ids: list, mock=False):
    """
    This function will take the restaurant_ids, and query the database to retrieve the
    longitute,latitude information of these restaurants
    :param mock:
    :param restaurant_ids:
    :return:
    [(longitude, latitude),...]
    """
    coords=[]
    if mock:
        """ In mock mode, we'll randomly generate 20 location coordiantes in San Francisco"""
        san_francisco_coords = [37.7749, -122.4194]
        coords = [mock_retrieve_coords(*san_francisco_coords, 1) for _ in range(10)]
    return coords
