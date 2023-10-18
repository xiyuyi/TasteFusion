import random


def mock_retrieve_coords(center_lat, center_lon, max_distance_in_miles):
    # todo bug: the miles conversion seems to be wrong.
    one_degree_of_latitude_in_miles = 69.0
    one_degree_of_longitude_in_miles = 55.2428  # This value varies depending on latitude but is roughly accurate near San Francisco

    random_distance_from_center_in_miles_lat = random.uniform(-max_distance_in_miles, max_distance_in_miles)
    random_distance_from_center_in_miles_lon = random.uniform(-max_distance_in_miles, max_distance_in_miles)

    random_lat = center_lat + (random_distance_from_center_in_miles_lat / one_degree_of_latitude_in_miles)
    random_lon = center_lon + (random_distance_from_center_in_miles_lon / one_degree_of_longitude_in_miles)

    return [random_lat, random_lon]


