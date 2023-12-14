from tastefusion.utils.get_coords_from_addresstext import get_coords_from_address_text
from tastefusion.utils.get_initial_restaurants import get_initial_restaurants

path_to_data_folder = '/Users/xiyuyi/Desktop/TDI_capstone/TasteFusion/tastefusion/data'
center = get_coords_from_address_text(address='Reno', mock=True)
restaurants_df = get_initial_restaurants(center=center,
                                         search_radius=0.8,
                                         mock=True,
                                         datapath=path_to_data_folder)
