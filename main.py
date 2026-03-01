import tkinter as tk
import random

root = tk.Tk()
root.title("Doodle Jump")

canvas = tk.Canvas(root, width=400, height=600, bg="lightblue")
canvas.pack()

player = canvas.create_rectangle(185, 500, 215, 530, fill="lightgreen", outline="black")
score_counter = canvas.create_text(10, 20, text="Score: 0", fill="black", font=("Arial", 15), anchor="w", )

vertical_velocity = 0
horizontal_velocity = 0
keys = {"left": False, "right": False}
platforms = []
score = 0

def press_left(event): keys["left"] = True
def release_left(event): keys["left"] = False
def press_right(event): keys["right"] = True
def release_right(event): keys["right"] = False

root.bind("<KeyPress-Left>", press_left)
root.bind("<KeyRelease-Left>", release_left)
root.bind("<KeyPress-Right>", press_right)
root.bind("<KeyRelease-Right>", release_right)

def create_platform(x, y):
    plat = canvas.create_rectangle(x, y, x + 60, y + 10, fill="green", outline="black")
    platforms.append(plat)

def game_loop():
    global vertical_velocity, horizontal_velocity, score

    p_pos = canvas.coords(player)

    #Player movement
    vertical_velocity += 0.5
    canvas.move(player, horizontal_velocity, vertical_velocity)
    
    if p_pos[1] >= 600:
        canvas.create_text(200, 300, text="GAME OVER", fill="red", font=("Arial", 30))
        return

    if keys["left"] and horizontal_velocity > -6:
        horizontal_velocity -= 1.4
    if keys["right"] and horizontal_velocity < 6:
        horizontal_velocity += 1.4
    if not (keys["left"] or keys["right"]):
        horizontal_velocity *= 0.9

    if p_pos[0] > 400:
        canvas.move(player, -400, 0)
    if p_pos[2] < 0:
        canvas.move(player, 400, 0)

    #platform collision
    if vertical_velocity > 0:
        for plat in platforms:
            plat_pos = canvas.coords(plat)
            if (p_pos[0] > plat_pos[0] and p_pos[0] < plat_pos[2]) or (p_pos[2] > plat_pos[0] and p_pos[2] < plat_pos[2]):
                if plat_pos[1] - 5 <= p_pos[3] <= plat_pos[3]:
                    vertical_velocity = -15

    #screen scroll
    if p_pos[1] <= 300:
        shift = 300 - p_pos[1]
        canvas.move(player, 0, shift)
        for plat in platforms:
            canvas.move(plat, 0, shift)
        score += int(shift)
        canvas.itemconfig(score_counter, text=f"Score: {score}")

    #generating
    for i, plat in enumerate(platforms):
        plat_pos = canvas.coords(plat)
        if plat_pos[1] > 600:
            canvas.delete(plat)
            platforms.pop(i)
            create_platform(random.randint(0, 340), random.randint(-20, 0))
    
    canvas.tag_raise(score_counter)
    root.after(10, game_loop)

create_platform(180, 570)
for i in range(10):
    create_platform(random.randint(0,340), i * 50)

game_loop()
root.mainloop()