import json
import requests
from db_config import get_redis_connection

def main():
    """
    Fetches football predictions data from a RapidAPI endpoint for a specific date and federation,
    then stores each prediction JSON object in Redis.

    Returns:
        None
    """

    # Define the API endpoint and parameters
    url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
    query_params = {
        "market": "classic",
        "iso_date": "2018-12-01",
        "federation": "UEFA"
    }
    headers = {
        "X-RapidAPI-Key": "424606f0bdmsh3921ec1c9bacdd5p18e58bjsn0c51bfa929d1",
        "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
    }

    # Make request to the API
    response = requests.get(url, headers=headers, params=query_params)
    if response.status_code == 200:
        # Extract data from the response JSON
        data_json = response.json().get('data', [])
        
        # Connect to Redis
        redis_connection = get_redis_connection()

        # Store each JSON object in Redis with keys data[0], data[1], ...
        for i, json_obj in enumerate(data_json):
            redis_key = f"data[{i}]"
            redis_connection.execute_command('JSON.SET', redis_key, '.', json.dumps(json_obj))
            print(redis_key, "inserted into redis")

if __name__ == "__main__":
    main()