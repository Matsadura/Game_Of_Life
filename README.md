# Conway's Game of Life
![](https://raw.githubusercontent.com/Matsadura/Game_Of_Life/refs/heads/dev/assets/images/logo-with-background.png)
## Description

![](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzdwdGdyNTd1eDloM3hycnhmZjV1OHR2ejJsMTRkeWliaDFkN3Y2dCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LO50zBkNczE6vtQXuS/giphy.gif)
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
   pip install -r requirements.txt

### Optional: Using a Virtual Environment
If you prefer to use a virtual environment for isolated package management:

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:

   1. On Windows:
      ```
      venv\Scripts\activate
      ```

   2. On macOS and Linux:
      ```
      source venv/bin/activate
      ```
3. Install the required packages in the virtual environment:
   ```
   pip install -r requirements.txt
   ```
4. When you're done, you can deactivate the virtual environment:
   ```
   deactivate
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
