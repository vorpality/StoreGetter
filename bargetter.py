import requests
import pandas as pd

API_KEY = ''


def get_bars(location):
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': 'bars in Athens',
        'key': API_KEY
    }
    bars = []

    while True:
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get('results', [])
        bars.extend(results)

        next_page_token = data.get('next_page_token')
        if not next_page_token:
            break

        # Wait for a few seconds to allow the next_page_token to become valid
        import time
        time.sleep(5)

        params = {
            'pagetoken': next_page_token,
            'key': API_KEY
        }

    return bars


def main():
    location = 'Athens'  # You can specify a more specific location if needed
    bars = get_bars(location)

    bar_data = []
    for bar in bars:
        place_id = bar['place_id']
        details = get_bar_details(place_id)
        if details:
            name = details.get('name', '')
            address = details.get('formatted_address', '')
            rating = details.get('rating', '')
            bar_data.append({'Name': name, 'Address': address, 'Rating': rating})

    df = pd.DataFrame(bar_data)

    csv_filename = 'bars_in_athens.csv'
    df.to_csv(csv_filename, index=False)
    print(f"CSV file '{csv_filename}' created successfully!")


def get_bar_details(place_id):
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_address,rating',
        'key': API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        result = data.get('result')
        return result
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")

    return None


if __name__ == '__main__':
    main()
