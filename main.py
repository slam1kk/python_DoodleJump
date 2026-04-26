import tkinter as tk
import random
from PIL import Image, ImageTk

#Global Variables
player = None
platforms, springs = [], []
difficultyGapX, difficultyGapY = 0, 0
verticalVelocity, horizontalVelocity = 0, 0
score = 0
keys = {"left": False, "right": False}
isPaused, isRunning = False, False
highestY = 0

#Window Settings
root = tk.Tk()

root.title("Python Doodle Jump")
root.minsize(500, 800)
root.attributes("-fullscreen", True)
root.update()

scrWidth, scrHeight = root.winfo_width(), root.winfo_height()

canvas = tk.Canvas(root, width=scrWidth, height=scrHeight)
canvas.pack(fill="both", expand=True)

root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

#Graphics
img_background = ImageTk.PhotoImage(Image.open("background.png").resize((scrWidth, scrHeight)))
img_player = ImageTk.PhotoImage(Image.open("doodler.png").resize((42, 46)))
img_defaultPlatform = ImageTk.PhotoImage(Image.open("default_platform.png").resize((76, 18)))
#img_spring = ImageTk.PhotoImage(Image.open("spring.png").resize((40, 40)))

canvas.create_image(0, 0, image=img_background, anchor="nw", tags="bg")

#Functions & Procedures
def create_platform(x, y, springChance):
    platWidth = max(30, 60 - (score // 5000) * 5)
    plat = canvas.create_image(x, y, image=img_defaultPlatform, anchor="nw", tags="gameObject")
    platforms.append(plat)

    if springChance > 0.9:
        spring_pos = random.randint(0, platWidth - 10)
        spring = canvas.create_rectangle(x + spring_pos, y - 10, x + spring_pos + 10, y, fill="gray", tags="gameObject")
        springs.append(spring)

def show_mainMenu():
    global isRunning
    isRunning = False
    root.minsize(500, 800)
    root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())
    canvas.delete("gameObject")
    canvas.create_text(scrWidth / 2, scrHeight / 4, text="DOODLE JUMP", fill="black", font=("Arial", 40, "bold"), tags=("gameObject", "logo"))
    
    btn_start = tk.Button(root, text="Start Game", font=("Arial", 17), bg="lightgreen", command=start_game)
    canvas.create_window(scrWidth / 2, scrHeight / 4 + 150, window=btn_start, tags=("gameObject", "start"))
    btn_exit = tk.Button(root, text="Exit", font=("Arial", 14), bg="indianred1", command=root.quit)
    canvas.create_window(scrWidth / 2, scrHeight / 4 + 240, window=btn_exit, tags=("gameObject", "exit"))

def start_game():
    global player, score, verticalVelocity, horizontalVelocity, platforms, springs, scoreCounter, isRunning, isPaused, difficultyGapX, difficultyGapY, highestY

    canvas.delete("gameObject")
    platforms, springs = [], []
    score = 0
    verticalVelocity, horizontalVelocity = 0, 0
    difficultyGapX, difficultyGapY = 500, 100
    isRunning, isPaused = True, False
    root.minsize(scrWidth, scrHeight)
    root.maxsize(scrWidth, scrHeight)
    
    player = canvas.create_image(scrWidth / 2, scrHeight - 200, image=img_player, anchor="nw", tags="gameObject")
    scoreCounter = canvas.create_text(10, 20, text="Score:", fill="black", font=("Arial", 15), anchor="w", tags="gameObject")

    create_platform(scrWidth / 2, scrHeight - 70, 0)
    highestY = scrHeight - 40
    currX = 0
    while highestY > 0:
        rightMostX = -200
        lowestInLayerY = scrHeight
        while rightMostX < scrWidth - 400:
            currX = random.randint(rightMostX + 200, rightMostX + difficultyGapX)
            currY = random.randint(highestY - difficultyGapY, highestY - 40)
            create_platform(currX, currY, 0)
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
    root.minsize(500, 700)
    root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())
    canvas.delete("gameObject")

    canvas.create_text(scrWidth / 2, scrHeight / 4, text="GAME OVER", fill="red", font=("Arial", 30), tags=("gameObject", "gameOver"))
    canvas.create_text(scrWidth / 2, scrHeight / 4 + 60, text=f"Final Score: {score}", fill="black", font=("Arial", 20), tags=("gameObject", "finalScore"))

    btn_restart = tk.Button(root, text="Play Again", font=("Arial", 14), bg="lightgreen", command=start_game)
    canvas.create_window(scrWidth / 2, scrHeight / 4 + 150, window=btn_restart, tags=("gameObject", "restart"))
    btn_mainMenu = tk.Button(root, text="Main Menu", font=("Arial", 14), bg="indianred1", command=show_mainMenu)
    canvas.create_window(scrWidth / 2, scrHeight / 4 + 200, window=btn_mainMenu, tags=("gameObject", "gameOverMainMenu"))

def press_left(event): keys["left"] = True
def release_left(event): keys["left"] = False
def press_right(event): keys["right"] = True
def release_right(event): keys["right"] = False

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
    canvas.coords("restart", scrWidth / 2, scrHeight / 4 + 150)
    canvas.coords("gameOverMainMenu", scrWidth / 2, scrHeight / 4 + 200)

root.bind("<Configure>", on_resize)
root.bind("<KeyPress-Left>", press_left)
root.bind("<KeyRelease-Left>", release_left)
root.bind("<KeyPress-Right>", press_right)
root.bind("<KeyRelease-Right>", release_right)
root.bind("<Escape>", toggle_pause)

def gameLoop():
    global verticalVelocity, horizontalVelocity, score, isRunning, difficultyGapY, highestY

    if not isRunning: return

    playerPos = canvas.coords(player)
    playerPos.append(playerPos[0] + 40)
    playerPos.append(playerPos[1] + 40)

    if isPaused: show_pauseMenu()

    #Player Movement
    verticalVelocity += 0.6
    canvas.move(player, horizontalVelocity, verticalVelocity)
    
    if keys["left"] and horizontalVelocity > -5:
        horizontalVelocity -= 1.2
    if keys["right"] and horizontalVelocity < 5:
        horizontalVelocity += 1.2
    if not (keys["left"] or keys["right"]):
        horizontalVelocity *= 0.9


    #Screen Borders
    if playerPos[0] + 20 > scrWidth: canvas.move(player, -scrWidth, 0)
    if playerPos[0] + 20 < 0: canvas.move(player, scrWidth, 0)


    #Screen Scroll
    if playerPos[1] <= scrHeight / 2:
        shift = scrHeight / 2 - playerPos[1]
        canvas.move(player, 0, shift)
        for plat in platforms: canvas.move(plat, 0, shift)
        for spring in springs: canvas.move(spring, 0, shift)

        score += int(shift)
        highestY += int(shift)
        canvas.itemconfig(scoreCounter, text=f"Score: {score}")


    #Generating
    for i, plat in enumerate(platforms):
        platPos = canvas.coords(plat)
        if platPos[1] > scrHeight:
            canvas.delete(plat)
            platforms.pop(i)

    for i, s in enumerate(springs):
        springPos = canvas.coords(s)
        if springPos[1] > scrHeight:
            canvas.delete(s)
            springs.pop(i)

    difficultyGapY = min(190, 100 + (score // 2000) * 15)
    difficultyGapX = min(1300, 500 + (score // 2000) * 50)

    while highestY > 0:
        rightMostX = -200
        lowestInLayerY = scrHeight
        while rightMostX < scrWidth - 80:
            currX = random.randint(rightMostX + 200, rightMostX + difficultyGapX)
            currY = random.randint(highestY - difficultyGapY, highestY - 40)
            create_platform(currX, currY, random.random())
            lowestInLayerY = min(lowestInLayerY, currY)
            rightMostX = currX
        highestY = lowestInLayerY


    #Spring Collision
    if verticalVelocity > 0:
        for s in springs:
            springPos = canvas.coords(s)
            if (springPos[0] > playerPos[0] and springPos[0] < playerPos[2]) or (springPos[2] > playerPos[0] and springPos[2] < playerPos[2]):
                if springPos[1] - 5 - verticalVelocity <= playerPos[3] <= springPos[1]:
                    verticalVelocity = -30


    #Platform Collision
    if verticalVelocity > 0:
        for plat in platforms:
            platPos = canvas.coords(plat)
            platPos.append(platPos[0] + 76)
            platPos.append(platPos[1] + 18)
            if (playerPos[0] > platPos[0] and playerPos[0] < platPos[2]) or (playerPos[2] > platPos[0] and playerPos[2] < platPos[2]):
                if platPos[1] - 5 - verticalVelocity <= playerPos[3] <= platPos[1]:
                    verticalVelocity = -20


    #Game Over
    if playerPos[1] >= scrHeight:
        show_gameOver()
        return
    

    canvas.tag_raise(scoreCounter)
    root.after(15, gameLoop)

show_mainMenu()
root.mainloop()