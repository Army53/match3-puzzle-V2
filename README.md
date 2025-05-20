# match3-puzzle/match3-puzzle/README.md

# Match-3 Puzzle Game

Welcome to the Match-3 Puzzle Game! This project is a simple implementation of a classic match-3 game where players can swap adjacent colored gems to create matches.

## Features

- Swap adjacent gems to create matches of three or more.
- The game starts with no more than 3 red and 3 green gems on the grid.
- Includes a grid management system to handle gem placement and matching.

## Project Structure

```
match3-puzzle
├── src
│   ├── game
│   │   ├── __init__.py
│   │   ├── board.py
│   │   ├── gem.py
│   │   └── utils.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_board.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd match3-puzzle
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Game

To start the game, run the following command:
```
python src/main.py
```

## Contributing

Feel free to submit issues or pull requests if you would like to contribute to the project!