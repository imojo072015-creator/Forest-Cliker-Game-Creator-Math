import tkinter as tk
import json
import os
import random

WIDTH = 1230
HEIGHT = 768

SAVE_FILE = "save.json"

# ---------------- SAVE ----------------
def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {"points": 0, "per_click": 1, "upgrade_cost": 10}

data = load_game()

points = data["points"]
per_click = data["per_click"]
upgrade_cost = data["upgrade_cost"]

def save_game():
    with open(SAVE_FILE, "w") as f:
        json.dump({
            "points": points,
            "per_click": per_click,
            "upgrade_cost": upgrade_cost
        }, f)

# ---------------- GAME ----------------
def click():
    global points
    points += per_click
    draw_ui()

def upgrade():
    global points, per_click, upgrade_cost
    if points >= upgrade_cost:
        points -= upgrade_cost
        per_click += 1
        upgrade_cost += 10
        draw_ui()

# ---------------- ANIMATION DATA ----------------
clouds = []
cloud_speed = []

for _ in range(6):
    clouds.append([random.randint(0, WIDTH), random.randint(50, 200)])
    cloud_speed.append(random.randint(1, 3))

def update_clouds():
    for i in range(len(clouds)):
        clouds[i][0] += cloud_speed[i]

        if clouds[i][0] > WIDTH + 100:
            clouds[i][0] = -100
            clouds[i][1] = random.randint(50, 200)

# ---------------- BACKGROUND ----------------
def draw_background():
    # céu
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT//2, fill="#87CEEB", outline="")

    # chão
    canvas.create_rectangle(0, HEIGHT//2, WIDTH, HEIGHT, fill="#2e8b57", outline="")

    # nuvens animadas ☁️
    for x, y in clouds:
        canvas.create_oval(x, y, x+80, y+40, fill="white", outline="")
        canvas.create_oval(x+20, y-10, x+100, y+30, fill="white", outline="")

    # árvores (leve variação pra parecer vivo)
    for _ in range(18):
        x = random.randint(0, WIDTH)
        y = random.randint(HEIGHT//2 - 40, HEIGHT)

        green = random.choice(["#1f7a1f", "#237f23", "#2a8f2a"])

        canvas.create_rectangle(x, y, x+10, y+40, fill="#6b3e1e", outline="")
        canvas.create_oval(x-15, y-30, x+25, y+20, fill=green, outline="")

# ---------------- UI ----------------
def draw_ui():
    canvas.delete("all")
    draw_background()

    canvas.create_text(WIDTH//2, 120,
        text="🌳 FOREST CLICKER",
        font=("Arial", 32, "bold"),
        fill="white")

    canvas.create_text(WIDTH//2, 260,
        text=f"Pontos: {points}",
        font=("Arial", 28),
        fill="white")

    canvas.create_text(WIDTH//2, 330,
        text=f"Por clique: {per_click}",
        font=("Arial", 18),
        fill="#00ffcc")

    canvas.create_text(WIDTH//2, 380,
        text=f"Upgrade: {upgrade_cost}",
        font=("Arial", 18),
        fill="#ffcc00")

    canvas.create_text(WIDTH//2, HEIGHT-25,
        text="🎮 Criado por Math",
        font=("Arial", 10, "bold"),
        fill="#00ffcc")

# ---------------- LOOP ANIMATION ----------------
def game_loop():
    update_clouds()
    draw_ui()
    root.after(80, game_loop)

# ---------------- LOADING ----------------
loading = 0
dots = 0

def loading_screen():
    global loading, dots

    canvas.delete("all")

    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#0b0f1a")

    canvas.create_text(WIDTH//2, 220,
        text="🌳 FOREST CLICKER",
        font=("Arial", 36, "bold"),
        fill="#00ffcc")

    dot_text = "." * (dots % 4)

    canvas.create_text(WIDTH//2, 300,
        text=f"Carregando{dot_text}",
        font=("Arial", 20),
        fill="white")

    bar_w = 600
    x1 = (WIDTH - bar_w) // 2
    y1 = 380
    x2 = x1 + bar_w
    y2 = 410

    canvas.create_rectangle(x1, y1, x2, y2, outline="white")
    fill = x1 + (bar_w * loading // 100)
    canvas.create_rectangle(x1, y1, fill, y2, fill="#00ffcc")

    loading += 3
    dots += 1

    if loading <= 100:
        root.after(40, loading_screen)
    else:
        start_game()

# ---------------- GAME START ----------------
def start_game():
    global click_btn, upgrade_btn

    click_btn = tk.Button(root, text="CLICAR",
                          font=("Arial", 20),
                          bg="#00ff88",
                          command=click)

    upgrade_btn = tk.Button(root, text="UPGRADE",
                            font=("Arial", 14),
                            bg="#3366ff",
                            fg="white",
                            command=upgrade)

    click_btn.place(x=520, y=450, width=200, height=80)
    upgrade_btn.place(x=540, y=550, width=160, height=60)

    game_loop()

# ---------------- EXIT ----------------
def on_close():
    save_game()
    root.destroy()

# ---------------- MAIN ----------------
root = tk.Tk()
root.title("Forest Clicker Animated")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_close)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0)
canvas.pack()

loading_screen()

root.mainloop()