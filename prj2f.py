import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7
CELL_SIZE = 80
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
current_player = 1
game_over = False
game_mode = None
HEURISTIC = "B"   # change to "C" once B works
# the Main window
root = tk.Tk()
root.title("Puissance 4")
root.resizable(False, False)
# Game mode selection
menu = tk.Frame(root)
menu.pack(pady=20)

tk.Label(menu, text="Choose Game Mode",
         font=("Arial", 18, "bold")).pack(pady=10)

tk.Button(menu, text="Human vs Human",
          command=lambda: choose_mode("H-H")).pack(pady=5)

tk.Button(menu, text="Human vs Computer",
          command=lambda: choose_mode("H-C")).pack(pady=5)
# Colors
COLORS = { 0: "white",1: "red",2: "yellow"}
# l'interface
title = tk.Label(root,text="PUISSANCE 4", font=("Arial", 24, "bold"))
title.pack(pady=10)
status = tk.Label(root,text="Joueur 1 - Rouge",font=("Arial", 16, "bold"))
status.pack(pady=5)
canvas = tk.Canvas(root, width=COLS * CELL_SIZE,height=ROWS * CELL_SIZE,bg="blue")
canvas.pack(padx=10, pady=10)

def choose_mode(mode):
    global game_mode
    game_mode = mode
    menu.destroy()
    if game_mode == "H-H":
        status.config(text="Joueur 1 - Rouge")
    else:
        status.config(text="Vous jouez - Rouge")

def draw_board():
    canvas.delete("all")#deletes the visual circle only
    for r in range(ROWS):
        for c in range(COLS):
            x1 = c * CELL_SIZE + 5
            y1 = r * CELL_SIZE + 5
            x2 = x1 + CELL_SIZE - 10
            y2 = y1 + CELL_SIZE - 10
            color = COLORS[board[r][c]]
#x2-x1=y2-y1(width = hight) so the oval becomes a circle with 70px hight and width
            canvas.create_oval(x1, y1, x2, y2,fill=color,outline="black",width=2 )

def check_winner(player, row, col):
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal
        (1, -1)   # Other diagonal
    ]
    for dr, dc in directions:
        count = 1
        # Check both sides of the placed piece
        for sign in [1, -1]:
            for i in range(1, 4):
                nr = row + i * dr * sign
                nc = col + i * dc * sign
                if (0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] == player):
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def get_windows(board):
    windows = []
    # Horizontal: 24 windows
    for r in range(ROWS):
        for c in range(COLS - 3):
            windows.append([(r, c+i) for i in range(4)])

    # Vertical: 21 windows
    for r in range(ROWS - 3):
        for c in range(COLS):
            windows.append([(r+i, c) for i in range(4)])

    # Diagonal down-right: 12 windows
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            windows.append([(r+i, c+i) for i in range(4)])

    # Diagonal up-right: 12 windows
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            windows.append([(r-i, c+i) for i in range(4)])
    return windows

def check_winning_board(board, player):
    for window in get_windows(board):
        if all(board[r][c] == player for r, c in window):
            return True
    return False

def computer_play():
    global current_player, game_over
    if game_over:
        return
    # Get columns that are not full
    available_cols = [c for c in range(COLS) if board[0][c] == 0]
    if not available_cols:
        return
    # Choose the best column
    col = find_best_move_alpha_beta(board, 3, HEURISTIC)
    if col is None:
        return
    # Place the computer's piece
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = 2
            break
    draw_board()
    # Check if computer wins
    if check_winner(2, row, col):
        game_over = True
        status.config(text="Ordinateur gagne !")
        messagebox.showinfo("Fin du jeu", "L'ordinateur a gagné !")
        return
    # Check draw
    if all(board[0][c] != 0 for c in range(COLS)):
        game_over = True
        status.config(text="Match nul !")
        messagebox.showinfo("Fin du jeu", "Match nul !")
        return
    # Return turn to human
    current_player = 1
    status.config(text="Vous jouez - Rouge")

def evaluate_B(board):
    score = 0
    for window in get_windows(board):
        values = [board[r][c] for r, c in window]
        x = values.count(2)
        o = values.count(1)
        empty = values.count(0)
        # X scores
        if x == 3 and empty == 1:
            score += 5
        elif x == 2 and empty == 2:
            score += 2
        # O scores
        elif o == 3 and empty == 1:
            score -= 5
        elif o == 2 and empty == 2:
            score -= 2
    # Central column bonus
    center_col = COLS // 2
    for r in range(ROWS):
        if board[r][center_col] == 2:
            score += 3
        elif board[r][center_col] == 1:
            score -= 3
    return score

def get_landing_row(board, col):#position of the lowest empty cell in a column
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == 0:
            return r
    return None

def simulate_move(board, col, player):
    new_board = [row[:] for row in board]
    row = get_landing_row(new_board, col)
    if row is not None:
        new_board[row][col] = player
    return new_board

def minimax_alpha_beta(board, depth, maximizing, alpha, beta, heuristic):
    if check_winning_board(board, 2):
        return 100000
    if check_winning_board(board, 1):
        return -100000
    if depth == 0:
        return evaluate_position(board, heuristic)
    available_cols = [col for col in range(COLS)if get_landing_row(board, col) is not None]
    if not available_cols:
        return evaluate_position(board, heuristic)
    if maximizing:
        best_score = float('-inf')
        for col in available_cols:
            new_board = simulate_move(board, col, 2)
            score = minimax_alpha_beta(
                new_board, depth - 1, False, alpha, beta, heuristic)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:
        best_score = float('inf')
        for col in available_cols:
            new_board = simulate_move(board, col, 1)
            score = minimax_alpha_beta(
                new_board, depth - 1, True, alpha, beta, heuristic)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score

def find_best_move_alpha_beta(board, depth, heuristic):
    best_score = float('-inf')
    best_col = None
    alpha = float('-inf')
    beta = float('inf')
    for col in range(COLS):
        if get_landing_row(board, col) is not None:
            new_board = simulate_move(board, col, 2)
            score = minimax_alpha_beta(new_board,depth - 1,False,alpha,beta,heuristic)
            if score > best_score:
                best_score = score
                best_col = col
            alpha = max(alpha, best_score)
    return best_col

def find_best_move_alpha_beta(board, depth, heuristic):
    best_score = float('-inf')
    best_col = None
    alpha = float('-inf')
    beta = float('inf')
    for col in range(COLS):
        if get_landing_row(board, col) is not None:
            new_board = simulate_move(board, col, 2)
            score = minimax_alpha_beta(new_board,depth - 1,False,alpha,beta,heuristic)
            if score > best_score:
                best_score = score
                best_col = col
            alpha = max(alpha, best_score)
    return best_col

def evaluate_C(board):
    score = evaluate_B(board)
    threats = set()
    for window in get_windows(board):
        values = [board[r][c] for r, c in window]
        x = values.count(2)
        o = values.count(1)
        empty = values.count(0)
        # Find X threats
        if x == 3 and empty == 1 and o == 0:
            for r, c in window:
                if board[r][c] == 0:
                    if get_landing_row(board, c) != r:
                        threats.add((2, r, c))
        # Find O threats
        elif o == 3 and empty == 1 and x == 0:
            for r, c in window:
                if board[r][c] == 0:
                    if get_landing_row(board, c) != r:
                        threats.add((1, r, c))
    # Apply parity scores
    for player, r, c in threats:
        row_number = ROWS - r
        if player == 2:
            if row_number % 2 == 0:
                score += 50
            else:
                score += 10
        elif player == 1:
            if row_number % 2 == 1:
                score -= 50
            else:
                score -= 10
    return score

def evaluate_position(board, heuristic):
    if heuristic == "B":
        return evaluate_B(board)
    elif heuristic == "C":
        return evaluate_C(board)

def play(event):
    global current_player, game_over
    if game_over:
        return
    if game_mode == "H-C" and current_player == 2:
        return
#event.x is the horizantal position of where the user clicked
    col = event.x // CELL_SIZE
    if col < 0 or col >= COLS:
        return

    # Find the lowest empty position so the player can add his piece or display a message if not
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = current_player
            break
    else:
        messagebox.showwarning( "Colonne pleine","Choisissez une autre colonne.")
        return
    draw_board()

    # Check winner
    if check_winner(current_player,row,col):
        game_over = True
        name = "Rouge" if current_player == 1 else "Jaune"
        status.config(text=f"Joueur {current_player} - {name} gagne !")
        messagebox.showinfo("Fin du jeu",f"Le joueur {name} a gagné !" )
        return
    # Check draw
    if all(board[0][c] != 0 for c in range(COLS)):
        game_over = True
        status.config(text="None of the players has won")
        messagebox.showinfo("Fin du jeu", "Match nul !")
        return
    
    # Change player
    current_player = 3 - current_player

    if game_mode == "H-H":
        name = "Rouge" if current_player == 1 else "Jaune"
        status.config(text=f"Joueur {current_player} - {name}")

    else:
        status.config(text="Ordinateur - Jaune")
        root.after(500, computer_play)#the bot will play after 500millisecond

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
restart_button = tk.Button(root,text="Nouvelle partie",font=("Arial", 13),command=restart)
restart_button.pack(pady=10)
draw_board()
root.mainloop()
