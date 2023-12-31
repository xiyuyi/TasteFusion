from tastefusion.mock_utils.mock_get_location_coordinates import mock_retrieve_coords


def get_coords_from_address_text(address: str = None, mock=True):
    """ This function takse in a string of address, and return the longitude and latitude coordinates as a list"""
    if address == 'Reno':
        coords = [39.5296, -119.8138]
        print('address is now set to Reno, update the coords')
    # elif address == 'Los Angeles':
    #     coords = [34.0522, -118.2437]
    #     print('address is now set to Los Angeles, update the coords')
    # elif address == 'San Francisco':
    #     coords = [37.7749, -122.4194]
    #     print('address is now set to San Francisco, update the coords')
    else:
        print('address not available (Only Reno is available), switched to mock mode with Reno.')
        mock = True

    if mock:
        san_francisco_coords = [37.7749, -122.4194]
        reno_coords = [39.5296, -119.8138]
        coords = mock_retrieve_coords(*reno_coords, 1)

    return coords
