import json
import matplotlib.pyplot as plt
from db_config import get_redis_connection

def visualize_outcome_distribution(redis_connection):
    # Initialize a dictionary to store counts of predicted outcomes
    outcome_counts = {'Home Win': 0, 'Away Win': 0, 'Home or Away Team Win': 0, 'Draw': 0}

    # Iterate through each key in Redis
    for key in redis_connection.scan_iter("data*"):
        # Get the JSON object stored at the key
        prediction = redis_connection.execute_command('JSON.GET', key, 'prediction')
        
        # Check if prediction is not None and not an empty string
        if prediction:
            prediction = prediction.strip('"')
            # Increment the count for the predicted outcome
            if prediction == '1':
                outcome_counts['Home Win'] += 1
            elif prediction == '2':
                outcome_counts['Away Win'] += 1
            elif prediction == '12':
                outcome_counts['Home or Away Team Win'] += 1
            elif prediction == '1X':
                outcome_counts['Draw'] += 1

    # Extract counts and labels for the pie chart
    counts = list(outcome_counts.values())
    labels = list(outcome_counts.keys())

    # Create pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Outcome Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

def main():
    # Call get_redis_connection to obtain a Redis connection object
    redis_connection = get_redis_connection()

    # Call the function with the Redis connection
    visualize_outcome_distribution(redis_connection)

if __name__ == "__main__":
    main()