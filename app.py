from flask import Flask, render_template, request, jsonify
from random_ai import determine_winner, predict_next_move, update_markov_chain, load_model, save_model, show_statistics, user_move_history, results

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    user_move = request.json['move']
    predicted_user_move = predict_next_move()
    
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

    user_move_history.append(user_move)
    results.append(result)
    update_markov_chain(user_move)

    return jsonify({'ai_move': ai_move, 'result': result_text})

@app.route('/statistics')
def statistics():
    total_games = len(user_move_history)
    user_wins = sum(1 for result in results if result == 'user')
    ai_wins = sum(1 for result in results if result == 'ai')
    draws = total_games - user_wins - ai_wins

    stats = {
        'total_games': total_games,
        'user_wins': user_wins,
        'ai_wins': ai_wins,
        'draws': draws
    }
    return jsonify(stats)

@app.route('/exit')
def exit():
    save_model()
    return jsonify({'message': 'Model saved and server stopped.'})

if __name__ == '__main__':
    load_model()
    app.run(debug=True)