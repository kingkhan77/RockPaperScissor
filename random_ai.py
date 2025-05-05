import random
from collections import defaultdict
import json

# Define the moves
MOVES = ['rock', 'paper', 'scissors']

# Function to determine the winner
def determine_winner(user_move, ai_move):
    if user_move == ai_move:
        return 'draw'
    elif (user_move == 'rock' and ai_move == 'scissors') or \
         (user_move == 'paper' and ai_move == 'rock') or \
         (user_move == 'scissors' and ai_move == 'paper'):
        return 'user'
    else:
        return 'ai'

# Initialize an empty list to store user moves
user_move_history = []
results = []

# Initialize a Markov Chain model
transition_counts = defaultdict(lambda: defaultdict(int))
previous_move = None

def update_markov_chain(move):
    global previous_move
    if previous_move is not None:
        transition_counts[previous_move][move] += 1
    previous_move = move

def predict_next_move():
    if not user_move_history:
        return random.choice(MOVES)
    
    last_move = user_move_history[-1]
    
    # Ensure the last move exists in transition_counts
    if last_move not in transition_counts:
        return random.choice(MOVES)
    
    next_move_counts = transition_counts[last_move]
    
    if not next_move_counts:
        return random.choice(MOVES)
    
    # Predict the most likely next move
    next_move = max(next_move_counts, key=next_move_counts.get)
    return next_move

def save_model(filename='model.json'):
    with open(filename, 'w') as f:
        json.dump({k: dict(v) for k, v in transition_counts.items()}, f)

def load_model(filename='model.json'):
    global transition_counts
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            transition_counts = defaultdict(lambda: defaultdict(int), 
                                            {k: defaultdict(int, v) for k, v in data.items()})
    except FileNotFoundError:
        pass

def show_statistics():
    total_games = len(user_move_history)
    user_wins = sum(1 for result in results if result == 'user')
    ai_wins = sum(1 for result in results if result == 'ai')
    draws = total_games - user_wins - ai_wins

    print(f"Total games: {total_games}")
    print(f"User wins: {user_wins}")
    print(f"AI wins: {ai_wins}")
    print(f"Draws: {draws}")

def play_game():
    user_move = input("Enter your move (rock, paper, scissors): ").lower()
    while user_move not in MOVES:
        print("Invalid move. Try again.")
        user_move = input("Enter your move (rock, paper, scissors): ").lower()

    # Predict the user's next move
    predicted_user_move = predict_next_move()
    
    # Choose a move that beats the predicted user move
    if predicted_user_move == 'rock':
        ai_move = 'paper'
    elif predicted_user_move == 'paper':
        ai_move = 'scissors'
    else:
        ai_move = 'rock'

    print(f"AI chose: {ai_move}")

    result = determine_winner(user_move, ai_move)
    if result == 'draw':
        print("It's a draw!")
    elif result == 'user':
        print("You win!")
    else:
        print("AI wins!")

    # Store the user's move
    user_move_history.append(user_move)
    results.append(result)

    # Update the Markov Chain with the user's move
    update_markov_chain(user_move)

    return user_move, ai_move, result

def main():
    load_model()
    print("Welcome to Rock-Paper-Scissors!")
    while True:
        play_game()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            show_statistics()
            save_model()
            break

if __name__ == "__main__":
    main()