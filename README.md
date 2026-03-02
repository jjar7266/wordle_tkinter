[![Sponsor](https://img.shields.io/badge/Sponsor-❤️-red)](https://github.com/sponsors/jjar7266)

<a href="https://buymeacoffee.com/jjar7266" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174">
</a>

<h1 align="center">🟩🟨 Wordle (Tkinter Edition) Clone 🟨🟩</h1>
<p align="center">
  <i>A polished, modern Wordle clone built entirely in Python + Tkinter</i><br>
  <b>Clean Architecture • Fully Commented • Easy to Extend</b>
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Tkinter-GUI-green" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
  <img src="https://img.shields.io/badge/Status-Active%20Development-brightgreen" />
</p>

---

## 🎮 Overview

A fully playable **Wordle clone** built from scratch using **Python + Tkinter**.
This project focuses on clean architecture, readable code, and a modern UI.
Every class is documented and structured for learning, extending, and experimenting.

This is part of a personal journey to master GUI architecture, game loops, and clean OOP design in Python.

---

## ✨ Features

- 🟩 Full Wordle gameplay (6 guesses, 5‑letter words)
- 🎨 Modern on‑screen keyboard with Wordle‑style coloring
- 🧠 Accurate evaluation engine (correct, misplaced, wrong)
- 🧱 Clean OOP architecture with fully commented classes
- 🔤 Word list filtering + random answer selection
- 🖼️ Tile grid with dynamic coloring
- 🧩 Debug‑friendly design
- 🪟 Cross‑platform (Windows/macOS/Linux)

---

## 🧠 Architecture Overview

The project is intentionally structured into clear, single‑responsibility classes:

### **WordSelector**
Loads the word list, filters valid 5‑letter words, and selects a random answer.

### **WordEngine**
Evaluates guesses and returns statuses:
`correct`, `misplaced`, `wrong`.

### **TileGrid**
Draws the 6×5 board and colors tiles based on evaluation.

### **Keyboard**
Displays the on‑screen keyboard and updates key colors with priority rules.

### **WordleGame**
Main controller that ties everything together:
input handling, game state, evaluation, UI updates, win/loss detection.

---

## 🔧 How It Works

- The controller manages the game loop
- The engine evaluates guesses
- The UI components update independently
- The architecture is modular and easy to extend

---

## 📁 Project Structure

    wordle_tkinter/
    │
    ├── main.py          # Full game implementation
    ├── wordlist.txt     # Valid 5-letter words
    ├── README.md        # Project documentation
    └── .venv/           # Virtual environment (optional)

---

## ▶️ Running the Game

```bash
python main.py

python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt   # optional
python main.py

🗺️ Roadmap
• 	Game Over popup
• 	Play Again / Quit buttons
• 	Restart logic
• 	Disable keyboard after game ends
• 	Optional: dark tile theme
• 	Optional: tile flip animation
• 	Optional: stats screen
• 	Optional: daily mode

📝 Changelog
v0.3 — Core Game Loop Complete
• 	Full gameplay implemented
• 	Keyboard + tile coloring
• 	Clean OOP architecture
• 	Debug tools added
• 	README added
v0.2 — UI + Input
• 	On‑screen keyboard
• 	Tile grid
• 	Input handling
v0.1 — Project Setup
• 	Repo created
• 	Word list added
• 	Basic Tkinter window

📄 License
This project is licensed under the MIT License.

🙌 Author
Jose Ruiz — Coral Springs, FL
Passionate about clean code, UI polish, and building things from scratch.
