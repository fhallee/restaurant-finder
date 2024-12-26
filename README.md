# Find Hidden Gem Restaurants in Your City

This script helps you find highly rated restaurants near a specific location using the Google Maps Places API.

I created this script because I've noticed that some of the best dining experiences often come from restaurants with fewer than 200 reviews but very high ratings (usually above 4.6 stars). This script allows me to quickly identify these "hidden gems" in any neighborhood.

## Requirements
- Python 3
- googlemaps library
   ```bash
   pip install googlemaps
## Usage
1. Get your Google Maps API key from https://console.cloud.google.com/ and save it as an environment variable.
    ```bash
    export GOOGLE_MAPS_API_KEY=your_api_key_here
2. Choose coordinates and a radius for the location you're interested in. You can use a tool like [Map Developers](https://www.mapdevelopers.com/draw-circle-tool.php).
3. Run the script.
    ```bash
    python best_restaurant.py <latitude> <longitude> [optional arguments]
    ```
    **Required Arguments:**
    - ```<latitude>```: The latitude of the location (decimal value).
    - ```<longitude>```: The longitude of the location (decimal value).

    **Optional Arguments:**
    - ```--radius```: (default: 500 meters): Radius of the search area in meters.
    - ```--min_rating```: (default: 0.0): Minimum rating of the restaurant (from 0.0 to 5.0).
    - ```--max_rating```: (default: 5.0): Maximum rating of the restaurant (from 0.0 to 5.0).
    - ```--min_reviews```: (default: 0): Minimum number of reviews.
    - ```--max_reviews```: (default: 100,000): Maximum number of reviews.

## Note/limitations
- The Google Maps Places API has a limit of 60 results per search **before** filtering.
- For best results, specify a search area that you expect to have fewer than 60 restaurants to ensure you capture all relevant results.
