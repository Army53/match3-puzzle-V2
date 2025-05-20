"""
Main entry point for the Match-3 Puzzle Game.
"""
from game.board import Board
import tkinter as tk

class Match3GameGUI: 
    def __init__(self, root, width=8, height=8, max_moves=20):
        self.root = root
        self.board = Board(width, height)
        self.width = width
        self.height = height
        self.max_moves = max_moves
        self.moves_left = max_moves
        self.score = 0
        self.selected = None
        self.labels = [[None for _ in range(width)] for _ in range(height)]
        self.status_label = None
        self.score_label = None
        self.moves_label = None
        self.remove_initial_matches()  # Ensure board is valid before UI
        self.setup_ui()
        self.update_ui()

    def remove_initial_matches(self):
        # Remove all matches before the game starts
        while True:
            matches = self.board.check_for_matches()
            if not matches:
                break
            self.board.update_board()

    def setup_ui(self):
        self.show_letters = tk.BooleanVar(value=True)
        self.move_history = []  # For undo functionality
        self.automatic_mode = False
        board_frame = tk.Frame(self.root)
        board_frame.grid(row=0, column=0, columnspan=self.width, pady=10)
        for y in range(self.height):
            for x in range(self.width):
                label = tk.Label(board_frame, text='', width=4, height=2, borderwidth=1, relief="solid", font=("Arial", 16))
                label.grid(row=y, column=x, padx=2, pady=2)
                label.bind("<Button-1>", lambda e, y=y, x=x: self.on_click(y, x))
                self.labels[y][x] = label
        info_frame = tk.Frame(self.root)
        info_frame.grid(row=1, column=0, columnspan=self.width, pady=10)
        self.score_label = tk.Label(info_frame, text=f"Score: {self.score}")
        self.score_label.pack(side=tk.LEFT, padx=10)
        self.moves_label = tk.Label(info_frame, text=f"Moves left: {self.moves_left}")
        self.moves_label.pack(side=tk.LEFT, padx=10)
        self.status_label = tk.Label(info_frame, text="Select a gem to start.")
        self.status_label.pack(side=tk.LEFT, padx=10)
        self.letters_checkbox = tk.Checkbutton(
            info_frame, text="Show Letters on Gems", variable=self.show_letters, command=self.update_ui
        )
        self.letters_checkbox.pack(side=tk.LEFT, padx=10)
        # Add Reset and Undo buttons
        self.reset_button = tk.Button(info_frame, text="Reset Puzzle", command=self.reset_puzzle)
        self.reset_button.pack(side=tk.LEFT, padx=10)
        self.undo_button = tk.Button(info_frame, text="Undo", command=self.undo_move)
        self.undo_button.pack(side=tk.LEFT, padx=10)
        # Add Automatic Mode button
        self.auto_button = tk.Button(info_frame, text="Automatic Mode: OFF", command=self.toggle_automatic_mode)
        self.auto_button.pack(side=tk.LEFT, padx=10)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def toggle_automatic_mode(self):
        self.automatic_mode = not self.automatic_mode
        self.auto_button.config(text=f"Automatic Mode: {'ON' if self.automatic_mode else 'OFF'}")
        if self.automatic_mode:
            self.status_label.config(text="Automatic mode enabled.")
            self.root.after(500, self.automatic_play)
        else:
            self.status_label.config(text="Automatic mode disabled.")

    def update_ui(self):
        for y in range(self.height):
            for x in range(self.width):
                color = self.board.grid[y][x].color
                text = color[0].upper() if self.show_letters.get() else ''
                self.labels[y][x].config(text=text, bg=color)
        self.score_label.config(text=f"Score: {self.score}")
        self.moves_label.config(text=f"Moves left: {self.moves_left}")

    def animate_swap(self, pos1, pos2, callback=None, steps=30, delay=100):
        y1, x1 = pos1
        y2, x2 = pos2
        label1 = self.labels[y1][x1]
        label2 = self.labels[y2][x2]
        color1 = label1.cget('bg')
        color2 = label2.cget('bg')
        text1 = label1.cget('text')
        text2 = label2.cget('text')

        def step_animation(step):
            # Fade out
            if step < steps // 2:
                fade = 255 - int(255 * (step + 1) / (steps // 2))
                fade_hex = f'#{fade:02x}{fade:02x}{fade:02x}'
                label1.config(bg=fade_hex)
                label2.config(bg=fade_hex)
                self.root.after(delay, lambda: step_animation(step + 1))
            # Swap and fade in
            elif step == steps // 2:
                label1.config(text=text2, bg=color2)
                label2.config(text=text1, bg=color1)
                self.root.after(delay, lambda: step_animation(step + 1))
            elif step < steps:
                fade = int(255 * (step - steps // 2 + 1) / (steps // 2))
                fade_hex1 = color2 if step == steps - 1 else f'#{fade:02x}{fade:02x}{fade:02x}'
                fade_hex2 = color1 if step == steps - 1 else f'#{fade:02x}{fade:02x}{fade:02x}'
                label1.config(bg=fade_hex1)
                label2.config(bg=fade_hex2)
                self.root.after(delay, lambda: step_animation(step + 1))
            else:
                if callback:
                    callback()

        step_animation(0)

    def animate_fall(self, columns_to_update, callback=None, steps=40, delay=150):
        # columns_to_update: list of x indices where gems fall
        # For each column, animate the fall of gems
        # We'll animate by updating the label backgrounds step by step
        def step_animation(step):
            for x in columns_to_update:
                for y in range(self.height-1, -1, -1):
                    label = self.labels[y][x]
                    if label.cget('bg') == 'white':
                        # Animate empty slot as white
                        fade = 255 - int(255 * (step + 1) / steps)
                        fade_hex = f'#{fade:02x}{fade:02x}{fade:02x}'
                        label.config(bg=fade_hex)
            if step < steps:
                self.root.after(delay, lambda: step_animation(step + 1))
            else:
                if callback:
                    callback()

        step_animation(0)

    def update_board_with_animation(self):
        # Remove matches and let gems fall down, fill new gems, with animation
        def do_update():
            while True:
                matches = self.board.check_for_matches()
                if not matches:
                    break
                # Mark matched gems as white for animation
                for y, x in matches:
                    self.labels[y][x].config(bg='white', text='')
                self.root.update()
                columns_to_update = list(set(x for y, x in matches))
                self.animate_fall(columns_to_update, callback=None)
                self.board.update_board()
                self.update_ui()
        self.root.after(200, do_update)

    def reset_puzzle(self):
        self.board = Board(self.width, self.height)
        self.score = 0
        self.moves_left = self.max_moves
        self.selected = None
        self.move_history = []
        self.remove_initial_matches()
        self.update_ui()
        self.status_label.config(text="Puzzle reset!")

    def undo_move(self):
        if not self.move_history:
            self.status_label.config(text="Nothing to undo.")
            return
        state = self.move_history.pop()
        self.board.grid = [[cell for cell in row] for row in state['grid']]
        self.score = state['score']
        self.moves_left = state['moves_left']
        self.selected = None
        self.update_ui()
        self.status_label.config(text="Move undone.")

    def automatic_play(self):
        if not self.automatic_mode or self.moves_left <= 0:
            return
        # Find a valid move (adjacent swap that results in a match)
        for y in range(self.height):
            for x in range(self.width):
                for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < self.height and 0 <= nx < self.width:
                        # Try swap
                        self.board.swap_gems((x, y), (nx, ny))
                        matches = self.board.check_for_matches()
                        self.board.swap_gems((x, y), (nx, ny))  # swap back
                        if matches:
                            self.selected = (y, x)
                            def after_swap():
                                self.board.swap_gems((x, y), (nx, ny))
                                matches2 = self.board.check_for_matches()
                                if matches2:
                                    self.score += len(matches2) * 10
                                    self.update_board_with_animation()
                                    self.status_label.config(text=f"Auto: Matched {len(matches2)} gems!")
                                else:
                                    self.board.swap_gems((x, y), (nx, ny))
                                    self.status_label.config(text="Auto: No match. Swap reversed.")
                                self.moves_left -= 1
                                self.update_ui()
                                if self.automatic_mode and self.moves_left > 0:
                                    self.root.after(800, self.automatic_play)
                            self.animate_swap((y, x), (ny, nx), callback=after_swap)
                            return
        # If no valid move found
        self.status_label.config(text="Automatic mode: No valid moves left.")
        self.automatic_mode = False
        self.auto_button.config(text="Automatic Mode: OFF")

    def on_click(self, y, x):
        if self.moves_left <= 0:
            self.status_label.config(text="No moves left! Game over.")
            return
        if self.selected is None:
            self.selected = (y, x)
            self.status_label.config(text=f"Selected ({y},{x})")
        else:
            y0, x0 = self.selected
            if abs(y0 - y) + abs(x0 - x) == 1:
                # Save state for undo
                self.move_history.append({
                    'grid': [[cell for cell in row] for row in self.board.grid],
                    'score': self.score,
                    'moves_left': self.moves_left
                })
                def after_swap():
                    self.board.swap_gems((x0, y0), (x, y))
                    matches = self.board.check_for_matches()
                    if matches:
                        self.score += len(matches) * 10
                        self.update_board_with_animation()
                        self.status_label.config(text=f"Matched {len(matches)} gems!")
                    else:
                        self.board.swap_gems((x0, y0), (x, y))  # swap back
                        self.status_label.config(text="No match. Swap reversed.")
                        self.move_history.pop()  # Remove this move from history if no match
                    self.moves_left -= 1
                    self.update_ui()
                # Animate swap visually, then do logic
                self.animate_swap((y0, x0), (y, x), callback=after_swap)
            else:
                self.status_label.config(text="Select an adjacent gem.")
            self.selected = None

if __name__ == "__main__":
    def start_game():
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())
            if width < 3 or height < 3:
                raise ValueError
        except ValueError:
            error_label.config(text="Please enter valid integers (>=3) for grid size.")
            return
        root.destroy()
        game_root = tk.Tk()
        game_root.title("Match-3 Puzzle Game")
        app = Match3GameGUI(game_root, width=width, height=height, max_moves=20)
        game_root.mainloop()

    root = tk.Tk()
    root.title("Match-3 Puzzle Setup")
    tk.Label(root, text="Enter grid width (>=3):").grid(row=0, column=0)
    width_entry = tk.Entry(root)
    width_entry.insert(0, "8")
    width_entry.grid(row=0, column=1)
    tk.Label(root, text="Enter grid height (>=3):").grid(row=1, column=0)
    height_entry = tk.Entry(root)
    height_entry.insert(0, "8")
    height_entry.grid(row=1, column=1)
    start_button = tk.Button(root, text="Start Game", command=start_game)
    start_button.grid(row=2, column=0, columnspan=2)
    error_label = tk.Label(root, text="", fg="red")
    error_label.grid(row=3, column=0, columnspan=2)
    root.mainloop()