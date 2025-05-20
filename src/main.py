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
        self.setup_ui()
        self.update_ui()

    def setup_ui(self):
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
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def update_ui(self):
        for y in range(self.height):
            for x in range(self.width):
                color = self.board.grid[y][x].color
                self.labels[y][x].config(text=color[0].upper(), bg=color)
        self.score_label.config(text=f"Score: {self.score}")
        self.moves_label.config(text=f"Moves left: {self.moves_left}")

    def animate_swap(self, pos1, pos2, callback=None, steps=10, delay=80):
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
                def after_swap():
                    self.board.swap_gems((x0, y0), (x, y))
                    matches = self.board.check_for_matches()
                    if matches:
                        self.score += len(matches) * 10
                        self.board.update_board()
                        self.status_label.config(text=f"Matched {len(matches)} gems!")
                    else:
                        self.board.swap_gems((x0, y0), (x, y))  # swap back
                        self.status_label.config(text="No match. Swap reversed.")
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