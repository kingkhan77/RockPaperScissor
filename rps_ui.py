import random
import tkinter as tk
from tkinter import messagebox
from random_ai import determine_winner, predict_next_move, update_markov_chain, load_model, save_model, show_statistics, user_move_history, results

# random_ai.py

def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'tie'
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        return 'user'
    else:
        return 'computer'

def play_game(user_move):
    # Predict the user's next move
    predicted_user_move = predict_next_move()
    
    # Choose a move that beats the predicted user move
    if predicted_user_move == 'rock':
        ai_move = 'paper'
    elif predicted_user_move == 'paper':
        ai_move = 'scissors'
    else:
        ai_move = 'rock'

    result = determine_winner(user_move, ai_move)
    if result == 'draw':
        result_text = "It's a draw!"
    elif result == 'user':
        result_text = "You win!"
    else:
        result_text = "AI wins!"

    # Store the user's move
    user_move_history.append(user_move)
    results.append(result)

    # Update the Markov Chain with the user's move
    update_markov_chain(user_move)

    # Update the UI
    result_label.config(text=f"AI chose: {ai_move}\n{result_text}")

def on_move_button_click(move):
    play_game(move)

def on_show_statistics():
    show_statistics()

def on_exit():
    save_model()
    root.destroy()

# Load the model
load_model()

# Create the main window
root = tk.Tk()
root.title("Rock-Paper-Scissors")

# Create and place the buttons
rock_button = tk.Button(root, text="Rock", command=lambda: on_move_button_click('rock'))
rock_button.pack(side=tk.LEFT, padx=10, pady=10)

paper_button = tk.Button(root, text="Paper", command=lambda: on_move_button_click('paper'))
paper_button.pack(side=tk.LEFT, padx=10, pady=10)

scissors_button = tk.Button(root, text="Scissors", command=lambda: on_move_button_click('scissors'))
scissors_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create and place the result label
result_label = tk.Label(root, text="Make your move!")
result_label.pack(pady=10)

# Create and place the statistics button
stats_button = tk.Button(root, text="Show Statistics", command=on_show_statistics)
stats_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create and place the exit button
exit_button = tk.Button(root, text="Exit", command=on_exit)
exit_button.pack(side=tk.LEFT, padx=10, pady=10)

# Start the main event loop
root.mainloop()