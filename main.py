import tkinter as tk
import random
from PIL import Image, ImageTk

import config
import storage
import mechanics

#Global Variables
player = None
platforms, springs, bullets, enemies = [], [], [], []
difficultyGapX, difficultyGapY = 0, 0
verticalVelocity, horizontalVelocity = 0, 0
score = 0
keys = {"left": False, "right": False}
isPaused, isRunning = False, False
highestY = 0
highscore = storage.load_highscore()  

#Window Settings
root = tk.Tk()

root.title("Python Doodle Jump")
root.minsize(config.MIN_WIDTH, config.MIN_HEIGHT)
root.attributes("-fullscreen", True)
root.update()

scrWidth, scrHeight = root.winfo_width(), root.winfo_height()

canvas = tk.Canvas(root, width=scrWidth, height=scrHeight)
canvas.pack(fill="both", expand=True)

root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

#Graphics
img_background = ImageTk.PhotoImage(Image.open("images/background.png").resize((scrWidth, scrHeight)))
img_player = ImageTk.PhotoImage(Image.open("images/doodler.png").resize((42, 46)))
img_enemy = ImageTk.PhotoImage(Image.open("images/enemy.png").resize((62, 60)))
img_defaultPlatform = ImageTk.PhotoImage(Image.open("images/default_platform.png").resize((76, 18)))
img_spring = ImageTk.PhotoImage(Image.open("images/spring.png").resize((18, 18)))

canvas.create_image(0, 0, image=img_background, anchor="nw", tags="bg")

#Functions & Procedures
def show_mainMenu():
    global isRunning
    isRunning = False
    root.minsize(config.MIN_WIDTH, config.MIN_HEIGHT)
    root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())
    canvas.delete("gameObject")
    img_logo = ImageTk.PhotoImage(Image.open("images/logo.png").resize((605, 210)))
    canvas.create_image(scrWidth / 2, scrHeight / 4, image=img_logo, tags=("gameObject", "logo"))
    
    btn_start = tk.Button(root, text="Start Game", font=("Arial", 17), bg="lightgreen", command=start_game)
    canvas.create_window(scrWidth / 2, scrHeight / 4 + 150, window=btn_start, tags=("gameObject", "start"))
    btn_exit = tk.Button(root, text="Exit", font=("Arial", 14), bg="indianred1", command=root.quit)
    canvas.create_window(scrWidth / 2, scrHeight / 4 + 240, window=btn_exit, tags=("gameObject", "exit"))

def start_game():
    global player, score, verticalVelocity, horizontalVelocity, platforms, springs, bullets, enemies, scoreCounter, isRunning, isPaused, difficultyGapX, difficultyGapY, highestY

    canvas.delete("gameObject")
    platforms, springs, bullets, enemies = [], [], [], []
    score = 0
    verticalVelocity, horizontalVelocity = 0, 0
    difficultyGapX, difficultyGapY = config.MIN_DIFFGAP_X, config.MIN_DIFFGAP_Y
    isRunning, isPaused = True, False
    root.minsize(scrWidth, scrHeight)
    root.maxsize(scrWidth, scrHeight)
    
    player = canvas.create_image(scrWidth / 2, scrHeight - 200, image=img_player, anchor="nw", tags="gameObject")
    scoreCounter = canvas.create_text(10, 20, text="Score:", fill="black", font=("Arial", 15), anchor="w", tags="gameObject")

    mechanics.create_platform(canvas, scrWidth / 2, scrHeight - 70, img_defaultPlatform, img_spring, platforms, springs, 1)
    highestY = scrHeight - 40
    currX = 0
    while highestY > 0:
        rightMostX = -200
        lowestInLayerY = scrHeight
        while rightMostX < scrWidth - 400:
            currX = random.randint(rightMostX + 200, rightMostX + difficultyGapX)
            currY = random.randint(highestY - difficultyGapY, highestY - 40)
            mechanics.create_platform(canvas, currX, currY, img_defaultPlatform, img_spring, platforms, springs, 1)
            lowestInLayerY = min(lowestInLayerY, currY)
            rightMostX = currX
        highestY = lowestInLayerY

    gameLoop()

def show_pauseMenu():
    global isRunning, isPaused
    isRunning, isPaused = False, True

    canvas.create_text(scrWidth / 2, scrHeight / 3, text="Pause", fill="black", font=("Arial", 40), tags=("pauseMenu","gameObject", "pause"))
    canvas.create_text(scrWidth / 2, scrHeight / 3 + 60, text=f"Current Score: {score}", fill="black", font=("Arial", 17), tags=("pauseMenu", "gameObject", "currScore"))

    btn_resume = tk.Button(root, text="Resume", font=("Arial", 17), bg="lightgreen", command=resume_game)
    canvas.create_window(scrWidth / 2, scrHeight / 3 + 140, window=btn_resume, tags=("pauseMenu", "gameObject", "resume"))
    btn_mainMenu = tk.Button(root, text="Main Menu", font=("Arial", 14), bg="indianred1", command=show_mainMenu)
    canvas.create_window(scrWidth / 2, scrHeight / 3 + 210, window=btn_mainMenu, tags=("pauseMenu", "gameObject", "pauseMainMenu"))

def resume_game():
    global isRunning, isPaused
    isRunning, isPaused = True, False
    canvas.delete("pauseMenu")
    gameLoop()

def show_gameOver():
    global isRunning
    isRunning = False

    storage.save_highscore(score)
    highscore = storage.load_highscore()
    root.minsize(config.MIN_WIDTH, config.MIN_HEIGHT)
    root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())
    canvas.delete("gameObject")

    canvas.create_text(scrWidth / 2, scrHeight / 4, text="GAME OVER", fill="red", font=("Arial", 30), tags=("gameObject", "gameOver"))
    canvas.create_text(scrWidth / 2, scrHeight / 4 + 60, text=f"Final Score: {score}", fill="black", font=("Arial", 20), tags=("gameObject", "finalScore"))
    canvas.create_text(scrWidth / 2, scrHeight / 4 + 100, text=f"High Score: {highscore}", fill="black", font=("Arial", 20), tags=("gameObject", "highScore"))

    btn_restart = tk.Button(root, text="Play Again", font=("Arial", 14), bg="lightgreen", command=start_game)
    canvas.create_window(scrWidth / 2, scrHeight / 4 + 170, window=btn_restart, tags=("gameObject", "restart"))
    btn_mainMenu = tk.Button(root, text="Main Menu", font=("Arial", 14), bg="indianred1", command=show_mainMenu)
    canvas.create_window(scrWidth / 2, scrHeight / 4 + 240, window=btn_mainMenu, tags=("gameObject", "gameOverMainMenu"))

def press_left(event): keys["left"] = True
def release_left(event): keys["left"] = False
def press_right(event): keys["right"] = True
def release_right(event): keys["right"] = False

def shoot(event):
    global isRunning, isPaused
    if not isRunning or isPaused: return
    playerPos = canvas.coords(player)
    px, py = playerPos[0], playerPos[1]

    bullet = canvas.create_oval(px + 15, py - 14, px + 25, py - 4, fill="gray", tags="gameObject")
    bullets.append(bullet)

def toggle_pause(event):
    if isRunning: show_pauseMenu()
    elif isPaused: resume_game()

def on_resize(event):
    global scrWidth, scrHeight
    scrWidth, scrHeight = root.winfo_width(), root.winfo_height()
    canvas.coords("logo", scrWidth / 2, scrHeight / 4)
    canvas.coords("start", scrWidth / 2, scrHeight / 4 + 150)
    canvas.coords("exit", scrWidth / 2, scrHeight / 4 + 240)

    canvas.coords("pause", scrWidth / 2, scrHeight / 3)
    canvas.coords("currScore", scrWidth / 2, scrHeight / 3 + 60)
    canvas.coords("resume", scrWidth / 2, scrHeight / 3 + 140)
    canvas.coords("pauseMainMenu", scrWidth / 2, scrHeight / 3 + 210)

    canvas.coords("gameOver", scrWidth / 2, scrHeight / 4)
    canvas.coords("finalScore", scrWidth / 2, scrHeight / 4 + 60)
    canvas.coords("highScore", scrWidth / 2, scrHeight / 4 + 100)
    canvas.coords("restart", scrWidth / 2, scrHeight / 4 + 170)
    canvas.coords("gameOverMainMenu", scrWidth / 2, scrHeight / 4 + 240)

root.bind("<Configure>", on_resize)
root.bind("<KeyPress-Left>", press_left)
root.bind("<KeyRelease-Left>", release_left)
root.bind("<KeyPress-Right>", press_right)
root.bind("<KeyRelease-Right>", release_right)
root.bind("<Escape>", toggle_pause)
root.bind("<space>", shoot)

def gameLoop():
    global verticalVelocity, horizontalVelocity, score, isRunning, difficultyGapY, highestY

    if not isRunning: return

    playerPos = canvas.coords(player)
    playerPos.append(playerPos[0] + 40)
    playerPos.append(playerPos[1] + 40)

    if isPaused: show_pauseMenu()

    #Player Movement
    verticalVelocity += config.GRAVITY
    canvas.move(player, horizontalVelocity, verticalVelocity)
    
    if keys["left"] and horizontalVelocity > -config.MAX_HOR_SPEED:
        horizontalVelocity -= config.HOR_SPEED
    if keys["right"] and horizontalVelocity < config.MAX_HOR_SPEED:
        horizontalVelocity += config.HOR_SPEED
    if not (keys["left"] or keys["right"]):
        horizontalVelocity *= config.SLOWDOWN


    #Bullet Movement
    for i, bullet in enumerate(bullets):
        canvas.move(bullet, 0, config.BULLET_SPEED)
        bulletPos = canvas.coords(bullet)
        if bulletPos [1] < 0:
            canvas.delete(bullet)
            bullets.pop(i)

    #Screen Borders
    if playerPos[0] + 20 > scrWidth: canvas.move(player, -scrWidth, 0)
    if playerPos[0] + 20 < 0: canvas.move(player, scrWidth, 0)


    #Screen Scroll
    if playerPos[1] <= scrHeight / 2:
        shift = scrHeight / 2 - playerPos[1]
        canvas.move(player, 0, shift)
        for object in platforms + springs + bullets + enemies: canvas.move(object, 0, shift)

        score += int(shift / 2)
        highestY += int(shift)
        canvas.itemconfig(scoreCounter, text=f"Score: {score}")


    #Generating
    for i, plat in enumerate(platforms):
        platPos = canvas.coords(plat)
        if platPos[1] > scrHeight:
            canvas.delete(plat)
            platforms.pop(i)

    for i, spr in enumerate(springs):
        sprPos = canvas.coords(spr)
        if sprPos[1] > scrHeight:
            canvas.delete(spr)
            springs.pop(i)

    difficultyGapY = min(config.MAX_DIFFGAP_Y, config.MIN_DIFFGAP_Y + (score // 2000) * 15)
    difficultyGapX = min(config.MAX_DIFFGAP_X, config.MIN_DIFFGAP_X + (score // 2000) * 50)

    while highestY > 0:
        rightMostX = -200
        lowestInLayerY = scrHeight
        while rightMostX < scrWidth - 80:
            currX = random.randint(rightMostX + 200, rightMostX + difficultyGapX)
            currY = random.randint(highestY - difficultyGapY, highestY - 40)
            mechanics.create_platform(canvas, currX, currY, img_defaultPlatform, img_spring, platforms, springs, random.random())
            lowestInLayerY = min(lowestInLayerY, currY)
            rightMostX = currX
        highestY = lowestInLayerY

    verticalVelocity = mechanics.check_collisions(canvas, platforms, springs, verticalVelocity, playerPos)

    isDead = mechanics.update_enemies(canvas, enemies, bullets, playerPos, scrWidth, scrHeight, show_gameOver, verticalVelocity)

    #Game Over
    if isDead: return

    if playerPos[1] >= scrHeight:
        show_gameOver()
        return
    
    canvas.tag_raise(scoreCounter)
    root.after(15, gameLoop)

show_mainMenu()
root.mainloop()