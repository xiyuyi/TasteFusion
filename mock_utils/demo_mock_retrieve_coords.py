from mock_utils.mock_get_location_coordinates import mock_retrieve_coords

san_francisco_coords = [37.7749, -122.4194]
random_coords = [mock_retrieve_coords(*san_francisco_coords, 20) for _ in range(10)]

print(random_coords)
