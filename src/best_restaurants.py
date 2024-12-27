import argparse
import os
import time
from googlemaps import Client

def find_restaurants(api_key, lat, lng, radius, min_rating, max_rating, min_reviews, max_reviews):
    """
    Finds restaurants within a given radius, filtered by rating and review count.

    Args:
        api_key: Your Google Maps API key.
        lat: Latitude of the center point.
        lng: Longitude of the center point.
        radius: Radius of the search area in meters.
        min_rating: Minimum rating of the restaurant.
        max_rating: Maximum rating of the restaurant.
        min_reviews: Minimum number of reviews for the restaurant.
        max_reviews: Maximum number of reviews for the restaurant.

    Returns:
        A list of dictionaries, where each dictionary represents a restaurant 
        and contains its name, rating, and review count.
    """

    gmaps = Client(key=api_key)
    all_restaurants = []
    next_page_token = None

    try:
        while True:
            places_result = gmaps.places_nearby(
                location=(lat, lng), 
                radius=radius, 
                type="restaurant",
                page_token = next_page_token
            )
            all_restaurants.extend(places_result['results'])
            next_page_token = places_result.get('next_page_token')
            time.sleep(2)
            if not next_page_token:
                break
    except Exception as e:
        print(f"Error: {e}")
        return []
    
    print(f"Total restaurants found in specified area: {len(all_restaurants)}")

    filtered_restaurants = []
    for place in all_restaurants:
        place_id = place['place_id']
        try: 
            place_details = gmaps.place(place_id=place_id)['result'] 
        except Exception as e:
            print(f"Error getting details for {place['name']}: {e}")
            continue

        rating = place_details.get('rating')
        reviews_count = place_details.get('user_ratings_total')

        if rating is None or reviews_count is None:
                        continue

        if (
            min_rating <= rating <= max_rating and 
            min_reviews <= reviews_count <= max_reviews
        ):
            filtered_restaurants.append({
                'name': place_details['name'],
                'address': place_details.get('formatted_address', 'Address Unavailable'),
            })

    print(f"{len(filtered_restaurants)} restaurants fit your criteria.")

    return filtered_restaurants


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find restaurants near a location.")
    parser.add_argument("latitude", type=float, help="Latitude of the center point.")
    parser.add_argument("longitude", type=float, help="Longitude of the center point.")
    parser.add_argument("--radius", type=int, default=500, help="Radius of the search area in meters (default: 500)")
    parser.add_argument("--min_rating", type=float, default=0, help="Minimum rating of the restaurant (default: 0)")
    parser.add_argument("--max_rating", type=float, default=5, help="Maximum rating of the restaurant (default: 5)")
    parser.add_argument("--min_reviews", type=int, default=0, help="Minimum number of reviews (default: 0)")
    parser.add_argument("--max_reviews", type=int, default=100000, help="Maximum number of reviews (default: 100,000)")

    args = parser.parse_args()

    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set.")

    try:
        found_restaurants = find_restaurants(
            api_key, 
            args.latitude, 
            args.longitude, 
            args.radius, 
            args.min_rating, 
            args.max_rating, 
            args.min_reviews, 
            args.max_reviews
        )

        if found_restaurants:
            print("Restaurants that meet your criteria:")
            for restaurant in found_restaurants:
                print(f"- {restaurant['name']}: {restaurant['address']}")
        else:
            print("No restaurants found that meet the criteria.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        parser.print_help()