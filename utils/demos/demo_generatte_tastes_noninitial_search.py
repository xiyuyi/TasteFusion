from tastefusion.utils.update_restaurants import update_restaurants
from tastefusion.utils.get_coords_from_addresstext import get_coords_from_address_text
from tastefusion.utils.get_initial_restaurants import get_initial_restaurants
from tastefusion.utils.update_tastes import generate_tastes

path_to_data_folder = '/Users/xiyuyi/Desktop/TDI_capstone/TasteFusion/tastefusion/data'
center = get_coords_from_address_text(address='Reno', mock=True)
restaurants_df = get_initial_restaurants(center=center,
                                         search_radius=0.8,
                                         mock=True,
                                         datapath=path_to_data_folder)

taste_votes = {'Casual Dining': '1', 'American': '4', 'Family Style': '7', 'Bar & Pub': '0', 'Breakfast & Brunch': '5', 'Sandwiches & Wraps': '0', 'Seafood': '1', 'Fast Food': '0', 'Vegetarian': '4', 'Coffee & Tea': '6', 'Fine Dining': '0', 'Bakery & Pastry': '8', 'Mexican': '0', 'Italian': '2'}


updated_restaurants_df = \
    update_restaurants( taste_votes=taste_votes,
                        current_restaurant_df=restaurants_df,
                        mock=False)
new_taste_tags = \
    generate_tastes(restaurant_df=updated_restaurants_df,
                    mock=False,
                    existing_taste_votes=taste_votes,
                    initial_search=False)
