import tkinter as tk
import random

# Define constants
WIDTH = 60
HEIGHT = 50
CELL_SIZE = 20
FOOD_COLORS = ['red', 'green', 'yellow', 'orange']
RUINS_COLOR = 'white'
EMPTY_COLOR = 'black'

# Direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Define skin configurations
PLAYER_1_SKINS = [
    {"name": "Red", "colors": ["red"]},
    {"name": "Green", "colors": ["green"]},
    {"name": "Blue", "colors": ["blue"]},
    {"name": "Yellow", "colors": ["yellow"]},
    {"name": "Orange", "colors": ["orange"]},
    {"name": "Purple", "colors": ["purple"]},
    {"name": "Cyan", "colors": ["cyan"]},
    {"name": "Magenta", "colors": ["magenta"]},
]

PLAYER_2_SKINS = [
    {"name": "Pink", "colors": ["pink"]},
    {"name": "Lime", "colors": ["lime"]},
    {"name": "Sky Blue", "colors": ["sky blue"]},
    {"name": "Gold", "colors": ["gold"]},
    {"name": "Brown", "colors": ["brown"]},
    {"name": "Turquoise", "colors": ["turquoise"]},
    {"name": "Gray", "colors": ["gray"]},
    {"name": "Violet", "colors": ["violet"]},
]


class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake Duel")
        self.attributes('-topmost', True)  # Make the window always on top
        self.lift()  # Bring the window to the front

        self.ruins = []  # Initialize ruins attribute as an empty list

        self.selected_skin_index_1 = 0
        self.selected_skin_index_2 = 0
        self.selected_skin_1 = PLAYER_1_SKINS[self.selected_skin_index_1]
        self.selected_skin_2 = PLAYER_2_SKINS[self.selected_skin_index_2]

        self.fruit_color = random.choice(FOOD_COLORS)  # Initialize fruit color

        self.create_menu()

    def create_menu(self):
        # Determine screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the geometry of the main window to full screen
        self.geometry(f"{screen_width}x{screen_height}+0+0")

        # Set background color of the main window
        self.configure(bg="black")

        self.menu_frame = tk.Frame(self, bg='black')
        self.menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the menu frame

        # Game title
        game_title_label = tk.Label(self.menu_frame, text="Snake Duel", font=("Comic Sans MS", 44,"bold", "italic"), fg="red",
                                    bg="black")
        game_title_label.pack(pady=20)

        # Function to set the color of the OptionMenu text
        def set_color(var, color):
            var.set(color)
            # Change font color to match the selected color
            if var == player_1_color_var:
                player_1_color_option_menu.config(fg=color)
            elif var == player_2_color_var:
                player_2_color_option_menu.config(fg=color)

        # Player 1 color selection
        player_1_label = tk.Label(self.menu_frame, text="Player 1 snake color:", font=("Comic Sans MS", 18),
                                  fg="white", bg="black")
        player_1_label.pack()

        player_1_color_var = tk.StringVar(self.menu_frame)
        player_1_color_var.set(self.selected_skin_1["name"])
        player_1_color_option_menu = tk.OptionMenu(self.menu_frame, player_1_color_var,
                                                   *[skin["name"] for skin in PLAYER_1_SKINS],
                                                   command=lambda color: set_color(player_1_color_var, color))
        player_1_color_option_menu.config(font=("Comic Sans MS", 16, "bold"), bg="black", fg="white")
        player_1_color_option_menu.pack()

        # Player 2 color selection
        player_2_label = tk.Label(self.menu_frame, text="Player 2 snake color:", font=("Comic Sans MS", 18),
                                  fg="white", bg="black")
        player_2_label.pack()

        player_2_color_var = tk.StringVar(self.menu_frame)
        player_2_color_var.set(self.selected_skin_2["name"])
        player_2_color_option_menu = tk.OptionMenu(self.menu_frame, player_2_color_var,
                                                   *[skin["name"] for skin in PLAYER_2_SKINS],
                                                   command=lambda color: set_color(player_2_color_var, color))
        player_2_color_option_menu.config(font=("Comic Sans MS", 16, "bold"), bg="black", fg="white")
        player_2_color_option_menu.pack()

        # Start button
        start_button = tk.Button(self.menu_frame, text="Start Game", font=("Helvetica", 22, "bold"), bg="red", fg="white",
                                 command=lambda: self.start_game(player_1_color_var.get(), player_2_color_var.get()))
        start_button.pack(pady=20)

    def set_color(self, color_var, color):
        color_var.set(color)
        color_var.get()

    def start_game(self, selected_color_1, selected_color_2):
        self.menu_frame.destroy()  # Destroy the menu frame

        # Set selected skins based on chosen colors
        self.selected_skin_1 = next(skin for skin in PLAYER_1_SKINS if skin["name"] == selected_color_1)
        self.selected_skin_2 = next(skin for skin in PLAYER_2_SKINS if skin["name"] == selected_color_2)

        # Create a frame for the stats bar
        self.stats_frame = tk.Frame(self, bg='black')
        self.stats_frame.pack(fill=tk.X)

        # Player 1 score label
        self.player_1_score_label = tk.Label(self.stats_frame, text="Player 1 Score: 0", font=("Helvetica", 18),
                                             fg=self.selected_skin_1["colors"][0], bg="black")
        self.player_1_score_label.pack(side=tk.LEFT, padx=380)

        # Player 2 score label
        self.player_2_score_label = tk.Label(self.stats_frame, text="Player 2 Score: 0", font=("Helvetica", 18),
                                             fg=self.selected_skin_2["colors"][0], bg="black")
        self.player_2_score_label.pack(side=tk.RIGHT, padx=380)

        # Create the game canvas
        self.canvas = tk.Canvas(self, width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, bg='black')
        self.canvas.pack()

        # Adjust the grid size
        self.grid_width = WIDTH
        self.grid_height = HEIGHT - 2  # Subtract 2 to leave space for the stats bar

        # Adjust initial positions of players
        self.snake_1 = [(self.grid_width // 4, self.grid_height // 2)]  # Player 1 starts at one quarter of the grid
        self.snake_2 = [
            (3 * self.grid_width // 4, self.grid_height // 2)]  # Player 2 starts at three quarters of the grid

        # Call the remaining game initialization code
        self.direction_1 = RIGHT
        self.direction_2 = LEFT
        self.food = self.place_food()
        self.score_1 = 0
        self.score_2 = 0
        self.paused = False
        self.bind('<KeyPress>', self.on_key_press)
        self.place_ruins()  # Place ruins when the game starts
        self.draw()  # Draw initial state
        self.move_interval_1 = 8  # Initially move every 80 milliseconds
        self.move_interval_2 = 8
        self.ticks_since_last_move_1 = 0
        self.ticks_since_last_move_2 = 0
        self.update_loop()  # Start the game loop

        # Schedule the fruit color change every second
        self.change_fruit_color()

    def update_loop(self):
        self.move_snake()
        self.draw()
        self.ticks_since_last_move_1 += 1
        self.ticks_since_last_move_2 += 1
        self.after(10, self.update_loop)  # Update every 10 milliseconds

    def change_fruit_color(self):
        self.fruit_color = random.choice(FOOD_COLORS)
        self.after(1000, self.change_fruit_color)  # Schedule the next color change after 1 second
    def place_food(self):

        while True:
            food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if food not in self.snake_1 and food not in self.snake_2:
                return food

    def place_ruins(self):
        max_ruins = (self.grid_width * self.grid_height) // 2  # Maximum number of ruins allowed
        additional_ruins = min(5, (max_ruins - len(self.ruins)))  # Add 5 ruins or until reaching the maximum allowed

        for _ in range(additional_ruins):
            ruin = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
            if (
                    ruin not in self.snake_1 and ruin not in self.snake_2 and ruin != self.food and
                    ruin not in self.ruins
            ):
                self.ruins.append(ruin)


    def draw_ruin(self, ruin):
        x, y = ruin
        self.canvas.create_rectangle(
            x * CELL_SIZE, y * CELL_SIZE,
            (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
            fill=RUINS_COLOR, outline='black'
        )

    def generate_ruin(self):
        while True:
            ruin = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if (
                ruin not in self.snake_1 and ruin not in self.snake_2 and ruin != self.food and ruin not in self.ruins
                and min(abs(ruin[0] - player[0]) + abs(ruin[1] - player[1]) for player in self.snake_1 + self.snake_2) > 5
            ):
                return ruin

    def move_snake(self):
        if not self.paused:
            if self.ticks_since_last_move_1 >= self.move_interval_1:
                self.move_snake_1()
                self.ticks_since_last_move_1 = 0
            if self.ticks_since_last_move_2 >= self.move_interval_2:
                self.move_snake_2()
                self.ticks_since_last_move_2 = 0
            self.check_collision()

    def move_snake_1(self):
        head = self.snake_1[0]
        new_head = (head[0] + self.direction_1[0], head[1] + self.direction_1[1])
        self.snake_1.insert(0, new_head)
        if new_head == self.food:
            self.score_1 += 1
            self.food = self.place_food()
            self.move_interval_1 -= 1  # Speed up snake 1 by 2 milliseconds
            self.after(500, self.place_ruins)  # Delayed placement of ruins after 1000 milliseconds (1 second)
        else:
            self.snake_1.pop()

    def move_snake_2(self):
        head = self.snake_2[0]
        new_head = (head[0] + self.direction_2[0], head[1] + self.direction_2[1])
        self.snake_2.insert(0, new_head)
        if new_head == self.food:
            self.score_2 += 1
            self.food = self.place_food()
            self.move_interval_2 -= 1  # Speed up snake 2 by 1 millisecond
            self.after(500, self.place_ruins)  # Delayed placement of ruins after 1000 milliseconds (1 second)
        else:
            self.snake_2.pop()

    def check_collision(self):
        if (
            self.snake_1[0] in self.snake_2[1:] or self.snake_1[0][0] < 0 or
            self.snake_1[0][0] >= WIDTH or self.snake_1[0][1] < 0 or
            self.snake_1[0][1] >= HEIGHT or self.snake_1[0] in self.snake_1[1:] or
            self.snake_1[0] in self.ruins
        ):
            self.game_over()
        elif (
            self.snake_2[0] in self.snake_1[1:] or self.snake_2[0][0] < 0 or
            self.snake_2[0][0] >= WIDTH or self.snake_2[0][1] < 0 or
            self.snake_2[0][1] >= HEIGHT or self.snake_2[0] in self.snake_2[1:] or
            self.snake_2[0] in self.ruins
        ):
            self.game_over()

    def apply_skins(self):
        for segment in self.snake_1:
            x, y = segment
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=self.selected_skin_1["colors"][0], outline='black'
            )
        for segment in self.snake_2:
            x, y = segment
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=self.selected_skin_2["colors"][0], outline='black'
            )

    def draw(self):
        self.canvas.delete(tk.ALL)  # Clear the canvas

        # Draw snakes
        for segment in self.snake_1:
            x, y = segment
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=self.selected_skin_1["colors"][0], outline='black'
            )
        for segment in self.snake_2:
            x, y = segment
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=self.selected_skin_2["colors"][0], outline='black'
            )

        # Draw food
        x, y = self.food
        self.canvas.create_oval(
            x * CELL_SIZE, y * CELL_SIZE,
            (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
            fill=self.fruit_color, outline='black'
        )

        # Draw ruins as squares
        for ruin in self.ruins:
            x, y = ruin
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                fill=RUINS_COLOR, outline='black'
            )

        # Display scores
        self.player_1_score_label.config(text=f"Player 1 Score: {self.score_1}")
        self.player_2_score_label.config(text=f"Player 2 Score: {self.score_2}")

    def update(self):
        self.change_fruit_color()
        self.ticks_since_last_move_1 += 1
        self.ticks_since_last_move_2 += 1
        self.after(10, self.update)  # Update every 10 milliseconds

    def on_key_press(self, event):
        key = event.keysym
        if key == 'Up' and self.direction_1 != DOWN:
            self.direction_1 = UP
        elif key == 'Down' and self.direction_1 != UP:
            self.direction_1 = DOWN
        elif key == 'Left' and self.direction_1 != RIGHT:
            self.direction_1 = LEFT
        elif key == 'Right' and self.direction_1 != LEFT:
            self.direction_1 = RIGHT
        elif key == 'w' and self.direction_2 != DOWN:
            self.direction_2 = UP
        elif key == 's' and self.direction_2 != UP:
            self.direction_2 = DOWN
        elif key == 'a' and self.direction_2 != RIGHT:
            self.direction_2 = LEFT
        elif key == 'd' and self.direction_2 != LEFT:
            self.direction_2 = RIGHT
        elif key == 'p':
            self.paused = not self.paused
        elif key == 'r':
            self.replay()

    def replay(self):
        if hasattr(self, "canvas"):
            self.canvas.destroy()
        self.destroy()  # Destroy the game window
        SnakeGame()  # Create a new game window

    def game_over(self):
        self.paused = True
        game_over_label = tk.Label(self, text="GAME OVER", font=("Helvetica", 40, "bold"), fg="white", bg="black")
        game_over_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        score_label = tk.Label(self, text=f"Player 1 Score: {self.score_1}\nPlayer 2 Score: {self.score_2}",
                               font=("Helvetica", 16), fg="white", bg="black")
        score_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)


if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
