# Conway's Game of Life

## Description
This project is an implementation of John Conway's Game of Life using Python and the customtkinter library. The Game of Life is a cellular automaton simulation where cells on a grid evolve over time based on a set of rules.

## Features
- Interactive grid to set initial cell states
- Start, pause, and reset functionality
- Adjustable simulation speed
- Customizable grid size
- Modern UI using customtkinter
- Save and load game state

## Requirements
- Python 3.7+
- customtkinter

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/Matsadura/Game_Of_Life.git
   ```
2. Navigate to the project directory:
   ```
   cd Game_Of_Life
   ```
3. Install the required packages:
   ```
   pip install customtkinter
   ```

## Usage
Run the main script to start the application:
```
python app.py
```

## How to Play
1. Click on cells to set their initial state (alive or dead).
2. Click the "Start" button to begin the simulation.
3. Use the "Pause" button to stop the simulation at any time.
4. Click "Reset" to clear the grid and start over.
5. Adjust the simulation speed using the slider.

## Rules of the Game
1. Any live cell with fewer than two live neighbours dies (underpopulation).
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies (overpopulation).
4. Any dead cell with exactly three live neighbours becomes a live cell (reproduction).

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Authors
- [Ali JBARI](https://github.com/ila36IX)
- [Badr ANNABI](https://github.com/Badr-Annabi)
- [Karim ASSIHOUT](https://github.com/ashtkarim)
- [Oumaima NAANAA](https://github.com/naanaa59)
- [Radouane ABOUNOUAS](https://github.com/RadouaneAbn)
- [Zidane ZAOUI](https://github.com/matsadura)
