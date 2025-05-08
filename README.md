# 🎮 AI-Based Rock Paper Scissors Game

An interactive Rock-Paper-Scissors game that combines classical AI with modern web and machine learning technologies. Playable using both button clicks and real-time hand gesture recognition via webcam.

---

## 🚀 Features

* 🤖 AI opponent using a **Markov Chain** prediction model
* 🖱️ Button-based gameplay and ✋ gesture recognition via **TensorFlow.js**
* 🔊 Real-time **voice feedback** using the SpeechSynthesis API
* 📊 Game **statistics tracking**
* 💾 Persistent AI learning using a local JSON model

---

## 🔧 Project Structure

### 🖥️ Backend (`app.py`)
* Built with **Flask**
* Core API routes:
  - `/` – Main game UI
  - `/play` – Accepts user move, predicts AI move, returns result
  - `/statistics` – Returns overall game stats
  - `/exit` – Saves Markov model to `model.json`

### 🧠 AI Logic (`random_ai.py`)
* Implements:
  - Move prediction with a Markov Chain
  - Game rules and winner determination
  - Persistent model updates and statistics generation

### 🌐 Frontend (`templates/index.html`, `static/js/router.js`)
* **Tailwind CSS** UI with responsive design
* Real-time webcam access for gesture input
* Integration of **TensorFlow.js Handpose** for gesture classification
* Dynamic updates for results and statistics
* **Voice narration** of game results

---

## 🧰 Technologies Used

| Function           | Tool/Library                                      |
|--------------------|---------------------------------------------------|
| Backend Server     | Flask (Python)                                    |
| AI Model           | Markov Chain (JSON-based persistence)             |
| Frontend Styling   | Tailwind CSS                                      |
| Gesture Detection  | TensorFlow.js Handpose                            |
| ML in Browser      | TensorFlow.js (Core + WebGL backend)              |
| Voice Feedback     | Browser SpeechSynthesis API                       |

---

## 📦 Installation


### Clone the repository
```
git clone https://github.com/yourusername/rock-paper-scissors-ai.git
cd rock-paper-scissors-ai
```
### Set up virtual environment (optional but recommended)
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run the app
```
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## 🎯 How to Play

1. Choose your move using:

   * Click buttons (Rock, Paper, Scissors), or
   * Use your hand gesture via webcam
2. The AI will predict and counter your move based on prior rounds.
3. Results, statistics, and voice feedback are displayed instantly.

---

## 📈 Future Improvements

* Multiplayer mode (co-op or competitive)
* Adaptive difficulty adjustment
* Gesture-only mode
* Augmented Reality (AR) gameplay
* Social sharing, leaderboards, and achievements

---

## 📝 License

MIT License – feel free to fork, improve, and share!

---

## 🙌 Credits

Created as a minor project using **Flask**, **TensorFlow\.js**, and **Markov Chains**.

