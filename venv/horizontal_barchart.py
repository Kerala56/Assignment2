import json
import matplotlib.pyplot as plt
from collections import defaultdict
from db_config import get_redis_connection

def visualize_predictions_by_competition(redis_connection):
    # Initialize a dictionary to store counts of predictions by competition
    competition_counts = defaultdict(int)

    # Iterate through each key in Redis
    for key in redis_connection.scan_iter("data*"):
        # Get the JSON object stored at the key
        json_obj = redis_connection.execute_command('JSON.GET', key)
        
        # Parse the JSON object
        data = json.loads(json_obj)
        
        # Extract the competition name from the JSON object
        competition_name = data.get('competition_name', None)
        
        # Increment the count for the competition
        if competition_name:
            competition_counts[competition_name] += 1

    # Extract competition names and counts for plotting
    competitions = list(competition_counts.keys())
    counts = list(competition_counts.values())

    # Create bar chart
    plt.figure(figsize=(12, 8))
    plt.barh(competitions, counts, color='orange')
    plt.xlabel('Number of Predictions')
    plt.ylabel('Competition')
    plt.title('Predictions by Competition')
    plt.gca().invert_yaxis()  # Invert y-axis to display competitions with the highest count at the top
    plt.tight_layout()
    plt.show()

def main():
    # Call get_redis_connection to obtain a Redis connection object
    redis_connection = get_redis_connection()

    # Call the function with the Redis connection
    visualize_predictions_by_competition(redis_connection)

if __name__ == "__main__":
    main()
