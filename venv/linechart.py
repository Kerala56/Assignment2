import json
import matplotlib.pyplot as plt
from db_config import get_redis_connection

def visualize_odds_line_chart(redis_connection):
    home_win_odds = []
    away_win_odds = []
    draw_odds = []

    # Define a counter to keep track of match number or time
    match_counter = 0

    # Iterate through each key in Redis
    for key in redis_connection.scan_iter("data*"):
        # Get the JSON object stored at the key
        json_obj = redis_connection.execute_command('JSON.GET', key)
        
        # Extract the odds for different outcomes from the JSON object
        odds = json.loads(json_obj).get('odds', None)
        if odds:
            match_counter += 1
            home_win_odds.append((match_counter, odds.get('1', None)))
            away_win_odds.append((match_counter, odds.get('2', None)))
            draw_odds.append((match_counter, odds.get('X', None)))

    # Create line chart for each type of odds
    plt.figure(figsize=(10, 6))
    plt.plot(*zip(*home_win_odds), marker='o', color='blue', label='Home Win')
    plt.plot(*zip(*away_win_odds), marker='o', color='orange', label='Away Win')
    plt.plot(*zip(*draw_odds), marker='o', color='red', label='Draw')
    plt.xlabel('Match Number')
    plt.ylabel('Odds')
    plt.title('Line Chart of Odds')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    # Call get_redis_connection to obtain a Redis connection object
    redis_connection = get_redis_connection()

    # Call the function with the Redis connection
    visualize_odds_line_chart(redis_connection)

if __name__ == "__main__":
    main()
