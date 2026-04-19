import tkinter as tk
import random

root = tk.Tk()
root.title("Doodle Jump")

canvas = tk.Canvas(root, width=400, height=600, bg="lightblue")
canvas.pack()

#Global Variables
player = None
platforms = []
springs = []
difficulty_gap = 40
score = 0
vertical_velocity = 0
horizontal_velocity = 0

keys = {"left": False, "right": False}

is_paused = False
game_running = False

def create_platform(x, y):
    width = max(30, 60 - (score // 5000) * 5)
    plat = canvas.create_rectangle(x, y, x + width, y + 10, fill="green", outline="black")
    platforms.append(plat)

    if random.random() < 0.1:
        spring_pos = random.randint(0, width - 10)
        spring = canvas.create_rectangle(x + spring_pos, y - 10, x + spring_pos + 10, y, fill="gray")
        springs.append(spring)

def show_main_menu():
    global game_running
    game_running = False
    canvas.delete("all")

    canvas.create_text(200, 200, text="DOODLE JUMP", fill="black", font=("Arial", 40, "bold"))
    
    btn_start = tk.Button(root, text="Start Game", font=("Arial", 17), bg="lightgreen", command=start_game)
    canvas.create_window(200, 300, window=btn_start)
    btn_exit = tk.Button(root, text="Exit", font=("Arial", 14), bg="indianred1", command=root.quit)
    canvas.create_window(200, 390, window=btn_exit)

def start_game():
    global player, score, vertical_velocity, horizontal_velocity, platforms, springs, score_counter, game_running, is_paused

    canvas.delete("all")
    platforms = []
    springs = []
    score = 0
    vertical_velocity, horizontal_velocity = 0, 0
    game_running = True
    is_paused = False

    player = canvas.create_rectangle(185, 500, 215, 530, fill="lightgreen", outline="black")
    score_counter = canvas.create_text(10, 20, text="Score: 0", fill="black", font=("Arial", 15), anchor="w")

    create_platform(180, 570)
    for _ in range(10):
        highest_y = min([canvas.coords(p)[1] for p in platforms])
        create_platform(random.randint(0, 340), highest_y - random.randint(difficulty_gap - 15, difficulty_gap))
    game_loop()

def show_pause_menu():
    global game_running, is_paused
    game_running = False
    is_paused = True

    canvas.create_text(200, 200, text="Pause", fill="black", font=("Arial", 40), tags="pause")
    canvas.create_text(200, 260, text=f"Current Score: {score}", fill="black", font=("Arial", 17), tags="pause")

    btn_resume = tk.Button(root, text="Resume", font=("Arial", 17), bg="lightgreen", command=resume_game)
    canvas.create_window(200, 340, window=btn_resume, tags="pause")
    btn_main_menu = tk.Button(root, text="Main Menu", font=("Arial", 14), bg="indianred1", command=show_main_menu)
    canvas.create_window(200, 390, window=btn_main_menu, tags="pause")

def resume_game():
    global game_running, is_paused
    canvas.delete("pause")
    game_running = True
    is_paused = False

    game_loop()

def show_game_over():
    global game_running
    game_running = False
    canvas.delete("all")

    canvas.create_text(200, 200, text="GAME OVER", fill="red", font=("Arial", 30))
    canvas.create_text(200, 260, text=f"Final Score: {score}", fill="black", font=("Arial", 20))

    btn_restart = tk.Button(root, text="Play Again", font=("Arial", 14), bg="lightgreen", command=start_game)
    canvas.create_window(200, 330, window=btn_restart)
    btn_main_menu = tk.Button(root, text="Main Menu", font=("Arial", 14), bg="indianred1", command=show_main_menu)
    canvas.create_window(200, 390, window=btn_main_menu)

def press_left(event): keys["left"] = True
def release_left(event): keys["left"] = False
def press_right(event): keys["right"] = True
def release_right(event): keys["right"] = False

def toggle_pause(event):
    if game_running: show_pause_menu()
    elif is_paused: resume_game()

root.bind("<KeyPress-Left>", press_left)
root.bind("<KeyRelease-Left>", release_left)
root.bind("<KeyPress-Right>", press_right)
root.bind("<KeyRelease-Right>", release_right)
root.bind("<Escape>", toggle_pause)

def game_loop():
    global vertical_velocity, horizontal_velocity, score, game_running, difficulty_gap

    if not game_running: return

    p_pos = canvas.coords(player)

    if is_paused: show_pause_menu()

    #Player Movement
    vertical_velocity += 0.5
    canvas.move(player, horizontal_velocity, vertical_velocity)
    
    if keys["left"] and horizontal_velocity > -4:
        horizontal_velocity -= 1
    if keys["right"] and horizontal_velocity < 4:
        horizontal_velocity += 1
    if not (keys["left"] or keys["right"]):
        horizontal_velocity *= 0.9


    #Screen Borders
    if p_pos[0] > 400: canvas.move(player, -400, 0)
    if p_pos[2] < 0: canvas.move(player, 400, 0)


    #Screen Scroll
    if p_pos[1] <= 300:
        shift = 300 - p_pos[1]
        canvas.move(player, 0, shift)
        for plat in platforms: canvas.move(plat, 0, shift)
        for spring in springs: canvas.move(spring, 0, shift)

        score += int(shift)
        canvas.itemconfig(score_counter, text=f"Score: {score}")


    #Generating
    for i, plat in enumerate(platforms):
        plat_pos = canvas.coords(plat)
        if plat_pos[1] > 600:
            canvas.delete(plat)
            platforms.pop(i)

    difficulty_gap = min(150, 40 + (score // 2000) * 10)
    highest_y = min([canvas.coords(p)[1] for p in platforms])

    if highest_y > 0:
        create_platform(random.randint(0, 340), highest_y - random.randint(difficulty_gap - 15, difficulty_gap))

    for j, s in enumerate(springs):
        s_pos = canvas.coords(s)
        if s_pos[1] > 600:
            canvas.delete(s)
            springs.pop(j)


    #Spring Collision
    if vertical_velocity > 0:
        for s in springs:
            s_pos = canvas.coords(s)
            if (s_pos[0] > p_pos[0] and s_pos[0] < p_pos[2]) or (s_pos[2] > p_pos[0] and s_pos[2] < p_pos[2]):
                if s_pos[1] - 5 - vertical_velocity <= p_pos[3] <= s_pos[1]:
                    vertical_velocity = -25


    #Platform Collision
    if vertical_velocity > 0:
        for plat in platforms:
            plat_pos = canvas.coords(plat)
            if (p_pos[0] > plat_pos[0] and p_pos[0] < plat_pos[2]) or (p_pos[2] > plat_pos[0] and p_pos[2] < plat_pos[2]):
                if plat_pos[1] - 5 - vertical_velocity <= p_pos[3] <= plat_pos[1]:
                    vertical_velocity = -15


    #Game Over
    if p_pos[1] >= 600:
        show_game_over()
        return
    

    canvas.tag_raise(score_counter)
    root.after(15, game_loop)

show_main_menu()
root.mainloop()