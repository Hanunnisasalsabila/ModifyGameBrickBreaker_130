import tkinter as tk
import random

class BrickBreakerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Aesthetic Brick Breaker")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="#f4f1de")  # Background krem
        self.canvas.pack()

        # Game variables
        self.ball_speed_x = 3
        self.ball_speed_y = -3
        self.score = 0
        self.combo = 0
        self.combo_text_id = None
        self.game_over = False

        # Paddle
        self.paddle = self.canvas.create_rectangle(350, 550, 450, 570, fill="#81b29a")  # Paddle hijau pastel

        # Ball and face
        self.ball = self.canvas.create_oval(390, 290, 410, 310, fill="#f2cc8f")  # Bola kuning pastel
        self.ball_face = self.create_ball_face()

        # Bricks
        self.bricks = []
        self.create_bricks()

        # Power-ups
        self.power_ups = []

        # Score display
        self.score_text = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="#3d405b", font=("Arial", 14))

        # Controls
        self.root.bind("<Left>", self.move_paddle_left)
        self.root.bind("<Right>", self.move_paddle_right)
        self.root.bind("<space>", self.restart_game)

        # Game loop
        self.update_game()

    def create_bricks(self):
        self.bricks.clear()
        brick_colors = ["#e07a5f", "#81b29a", "#f2cc8f", "#3d405b", "#e6beae"]  # Warna pastel
        for i in range(5):  # Rows
            for j in range(10):  # Columns
                x1 = 80 * j + 10
                y1 = 40 * i + 10
                x2 = x1 + 70
                y2 = y1 + 30
                color = random.choice(brick_colors)
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#f4f1de")
                self.bricks.append(brick)

    def create_ball_face(self):
        """Create the face on the ball."""
        return {
            "left_eye": self.canvas.create_oval(395, 295, 400, 300, fill="#3d405b"),  # Mata kiri
            "right_eye": self.canvas.create_oval(405, 295, 410, 300, fill="#3d405b"),  # Mata kanan
            "mouth": self.canvas.create_arc(395, 305, 405, 315, start=0, extent=-180, style="arc", outline="#3d405b")  # Mulut
        }

    def update_ball_face(self):
        """Update the position of the face components to match the ball."""
        ball_coords = self.canvas.coords(self.ball)
        ball_center_x = (ball_coords[0] + ball_coords[2]) / 2
        ball_center_y = (ball_coords[1] + ball_coords[3]) / 2

        self.canvas.coords(self.ball_face["left_eye"], ball_center_x - 5, ball_center_y - 5,
                           ball_center_x - 2, ball_center_y - 2)
        self.canvas.coords(self.ball_face["right_eye"], ball_center_x + 2, ball_center_y - 5,
                           ball_center_x + 5, ball_center_y - 2)
        self.canvas.coords(self.ball_face["mouth"], ball_center_x - 5, ball_center_y + 2,
                           ball_center_x + 5, ball_center_y + 6)

    def move_paddle_left(self, event):
        if not self.game_over:
            self.canvas.move(self.paddle, -20, 0)

    def move_paddle_right(self, event):
        if not self.game_over:
            self.canvas.move(self.paddle, 20, 0)

    def spawn_power_up(self, x, y):
        """Spawn a power-up at the given coordinates."""
        power_up_type = random.choice(["enlarge", "shrink"])
        color = "#6a4c93" if power_up_type == "enlarge" else "#ef476f"
        power_up = {
            "id": self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color),
            "type": power_up_type,
        }
        self.power_ups.append(power_up)

    def apply_power_up(self, power_up):
        """Apply the effect of the power-up."""
        if power_up["type"] == "enlarge":
            paddle_coords = self.canvas.coords(self.paddle)
            self.canvas.coords(self.paddle, paddle_coords[0] - 20, paddle_coords[1], paddle_coords[2] + 20, paddle_coords[3])
        elif power_up["type"] == "shrink":
            paddle_coords = self.canvas.coords(self.paddle)
            if paddle_coords[2] - paddle_coords[0] > 40:
                self.canvas.coords(self.paddle, paddle_coords[0] + 20, paddle_coords[1], paddle_coords[2] - 20, paddle_coords[3])

    def show_combo_text(self, text, color):
        """Display combo text in the center of the canvas."""
        if self.combo_text_id:
            self.canvas.delete(self.combo_text_id)
        self.combo_text_id = self.canvas.create_text(400, 300, text=text, fill=color, font=("Arial", 24))
        self.root.after(1000, lambda: self.canvas.delete(self.combo_text_id))

    def game_over_screen(self):
        """Display Game Over message and set game_over flag."""
        self.canvas.create_text(400, 300, text="GAME OVER", fill="#e63946", font=("Arial", 32))
        self.canvas.create_text(400, 350, text="Press SPACE to Restart", fill="#3d405b", font=("Arial", 16))
        self.game_over = True

    def restart_game(self, event):
        """Restart the game."""
        if self.game_over:
            self.canvas.delete("all")
            self.score = 0
            self.combo = 0
            self.ball_speed_x = 3
            self.ball_speed_y = -3
            self.game_over = False

            self.paddle = self.canvas.create_rectangle(350, 550, 450, 570, fill="#81b29a")
            self.ball = self.canvas.create_oval(390, 290, 410, 310, fill="#f2cc8f")
            self.ball_face = self.create_ball_face()
            self.create_bricks()
            self.score_text = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="#3d405b", font=("Arial", 14))

            self.update_game()

    def update_game(self):
        if self.game_over:
            return

        # Move ball
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)
        self.update_ball_face()

        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(self.paddle)

        # Wall collision
        if ball_coords[0] <= 0 or ball_coords[2] >= 800:
            self.ball_speed_x = -self.ball_speed_x
            self.combo = 0
        if ball_coords[1] <= 0:
            self.ball_speed_y = -self.ball_speed_y
        if ball_coords[3] >= 600:
            self.game_over_screen()
            return

        # Paddle collision
        if paddle_coords[0] < ball_coords[2] < paddle_coords[2] and paddle_coords[1] < ball_coords[3] < paddle_coords[3]:
            self.ball_speed_y = -self.ball_speed_y
            self.combo = 0

        # Brick collision
        for brick in self.bricks:
            brick_coords = self.canvas.coords(brick)
            if brick_coords[0] < ball_coords[2] < brick_coords[2] and brick_coords[1] < ball_coords[3] < brick_coords[3]:
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_speed_y = -self.ball_speed_y
                self.score += 10
                self.combo += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

                # Combo effects
                if self.combo == 2:
                    self.show_combo_text("Great!", "#81b29a")
                elif self.combo == 3:
                    self.show_combo_text("Excellent!", "#e07a5f")

                # Power-up
                if random.random() < 0.3:
                    self.spawn_power_up((brick_coords[0] + brick_coords[2]) / 2, (brick_coords[1] + brick_coords[3]) / 2)
                break

        # Power-up movement
        for power_up in self.power_ups[:]:
            self.canvas.move(power_up["id"], 0, 4)
            power_up_coords = self.canvas.coords(power_up["id"])

            if paddle_coords[0] < power_up_coords[2] < paddle_coords[2] and paddle_coords[1] < power_up_coords[3] < paddle_coords[3]:
                self.apply_power_up(power_up)
                self.canvas.delete(power_up["id"])
                self.power_ups.remove(power_up)

            elif power_up_coords[3] > 600:
                self.canvas.delete(power_up["id"])
                self.power_ups.remove(power_up)

        self.root.after(16, self.update_game)


# Start game
root = tk.Tk()
game = BrickBreakerGame(root)
root.mainloop()
