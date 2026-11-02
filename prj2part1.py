
import tkinter as tk
from tkinter import messagebox

# Game settings
ROWS = 6
COLS = 7
CELL_SIZE = 80

board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
current_player = 1
game_over = False

# Main window
root = tk.Tk()
root.title("Puissance 4")
root.resizable(False, False)

# Colors
COLORS = {
    0: "white",
    1: "red",
    2: "yellow"
}

# Interface
title = tk.Label(
    root,
    text="PUISSANCE 4",
    font=("Arial", 24, "bold")
)
title.pack(pady=10)

status = tk.Label(
    root,
    text="Joueur 1 - Rouge",
    font=("Arial", 16, "bold")
)
status.pack(pady=5)

canvas = tk.Canvas(
    root,
    width=COLS * CELL_SIZE,
    height=ROWS * CELL_SIZE,
    bg="blue",
    highlightthickness=0
)
canvas.pack(padx=10, pady=10)


def draw_board():
    canvas.delete("all")

    for r in range(ROWS):
        for c in range(COLS):
            x1 = c * CELL_SIZE + 5
            y1 = r * CELL_SIZE + 5
            x2 = x1 + CELL_SIZE - 10
            y2 = y1 + CELL_SIZE - 10

            color = COLORS[board[r][c]]

            canvas.create_oval(
                x1, y1, x2, y2,
                fill=color,
                outline="black",
                width=2
            )


def check_winner(player):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal
        (1, -1)   # Other diagonal
    ]

    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != player:
                continue

            for dr, dc in directions:
                count = 0

                for i in range(4):
                    nr = r + i * dr
                    nc = c + i * dc

                    if (0 <= nr < ROWS and
                        0 <= nc < COLS and
                        board[nr][nc] == player):
                        count += 1

                if count == 4:
                    return True

    return False


def play(event):
    global current_player, game_over

    if game_over:
        return

    col = event.x // CELL_SIZE

    if col < 0 or col >= COLS:
        return

    # Find the lowest empty position
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = current_player
            break
    else:
        messagebox.showwarning(
            "Colonne pleine",
            "Choisissez une autre colonne."
        )
        return

    draw_board()

    # Check winner
    if check_winner(current_player):
        game_over = True
        name = "Rouge" if current_player == 1 else "Jaune"

        status.config(text=f"Joueur {current_player} gagne !")

        messagebox.showinfo(
            "Fin du jeu",
            f"Le joueur {name} a gagné !"
        )
        return

    # Check draw
    if all(board[0][c] != 0 for c in range(COLS)):
        game_over = True
        status.config(text="Match nul !")
        messagebox.showinfo("Fin du jeu", "Match nul !")
        return

    # Change player
    current_player = 3 - current_player

    name = "Rouge" if current_player == 1 else "Jaune"
    status.config(text=f"Joueur {current_player} - {name}")


def restart():
    global board, current_player, game_over

    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    current_player = 1
    game_over = False

    status.config(text="Joueur 1 - Rouge")
    draw_board()
    
# Mouse click event
canvas.bind("<Button-1>", play)

# Restart button
restart_button = tk.Button(
    root,
    text="Nouvelle partie",
    font=("Arial", 13),
    command=restart
)
restart_button.pack(pady=10)

draw_board()

root.mainloop()
