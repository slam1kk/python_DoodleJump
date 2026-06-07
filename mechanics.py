import random
import config
import math
import winsound

lastLayer, buildingLayer = [], []
maxHeight = 0

# Sounds
def play_sfx(file_name):
    try:
        winsound.PlaySound(file_name, winsound.SND_ASYNC)
    except:
        return

def generating(canvas, img_defPl, img_shattPl, img_movPl, img_spr, img_enR, plats, sprs, ens, scrWid, scrHeight, score):
    global lastLayer, buildingLayer, maxHeight

    difficultyGapX = min(config.MAX_DIFFGAP_X, config.MIN_DIFFGAP_X + (score // 500) * 15)
    difficultyGapY = min(config.MAX_DIFFGAP_Y, config.MIN_DIFFGAP_Y + (score // 500) * 5)

# Delete Plats N Springs
    for i, plat in enumerate(plats):
        platPos = canvas.coords(plat[0])
        if platPos[1] > scrHeight:
            canvas.delete(plat)
            plats.pop(i)

    for i, spr in enumerate(sprs):
        sprPos = canvas.coords(spr)
        if sprPos[1] > scrHeight:
            canvas.delete(spr)
            sprs.pop(i)

# Start Generating
    if not plats:
        currIdx = 0
        lastLayer, buildingLayer = [], []
        platsNum = max(1, math.ceil(scrWid // difficultyGapX))
        create_platform(canvas, scrWid / 2, scrHeight - 100, img_defPl, img_shattPl, img_movPl, img_spr, img_enR, plats, sprs, ens, 1, score, scrWid)
        startY = scrHeight - 120
        for i in range(platsNum):
            x = i * difficultyGapX + random.randint(0, 30)
            x = min(x, scrWid - 76)
            y = random.randint(startY - 80, startY)
            plat = create_platform(canvas, x, y, img_defPl, img_shattPl, img_movPl, img_spr, img_enR, plats, sprs, ens, 1, score, scrWid)
            lastLayer.append(plat)
        lowestInLayer = max(lastLayer, key=lambda p: canvas.coords(p[0])[1])
        maxHeight = int(canvas.coords(lowestInLayer[0])[1] - difficultyGapY)
        return
    
    highestPlat = min(plats, key=lambda p: canvas.coords(p[0])[1])
    highestY = canvas.coords(highestPlat[0])[1]
    if highestY <= config.TARGET_TOP_Y: return

# Calculation of the Number of Plats
    platsInLayer = max(1, math.ceil(scrWid // difficultyGapX))
    currIdx = len(buildingLayer)
    if currIdx >= platsInLayer:
        lastLayer = buildingLayer.copy()
        buildingLayer.clear()
        currIdx = 0
        lowestInLayer = max(lastLayer, key=lambda p: canvas.coords(p[0])[1])
        maxHeight = int(canvas.coords(lowestInLayer[0])[1] - difficultyGapY)

    if currIdx <= len(buildingLayer):
        parentPlat = lastLayer[currIdx]
    else:
        return

# Calculation of new Coords
    newY = random.randint(maxHeight - 70, maxHeight)

    parentX = canvas.coords(parentPlat[0])[0]
    newX = parentX + random.randint(int(-difficultyGapX / 1.5), int(difficultyGapX / 1.5))
    leftLimit = currIdx * difficultyGapX + 10
    rightLimit = (currIdx + 1) * difficultyGapX - 76

    if newX < leftLimit:
        newX = rightLimit
    elif newX > rightLimit:
        if newX > scrWid:
            newX = scrWid - 76
        else:
            newX = leftLimit
    newX = max(leftLimit, min(rightLimit, newX))

    newPlat = create_platform(canvas, newX, newY, img_defPl, img_shattPl, img_movPl, img_spr, img_enR, plats, sprs, ens, random.random(), score, scrWid)
    buildingLayer.append(newPlat)

def create_platform(canvas, x, y, img_defPl, img_shattPl, img_movPl, img_spr, img_en, plats, sprs, ens, sprChance, score, scrWid):
    movingChance = min(config.MAX_ALTPLAT_CHANCE, (score // 2000) * config.STEP_ALTPLAT_CHANCE)
    shattChance = min(config.MAX_ALTPLAT_CHANCE, (score // 2000) * config.STEP_ALTPLAT_CHANCE)
    rand = random.random()

    if rand < movingChance:
        platType = "moving"
        img = img_movPl
        speed = config.MOVING_PLATFORM_SPEED if random.random() > 0.5 else -config.MOVING_PLATFORM_SPEED
    elif rand < movingChance + shattChance:
        platType = "shattered"
        img = img_shattPl
        speed = 0
    else:
        platType = "default"
        img = img_defPl
        speed = 0

    plat = [canvas.create_image(x, y, image=img, anchor="nw", tags="gameObject"), platType, speed]
    plats.append(plat)

# Spawn Springs
    if platType == "default" and sprChance < config.SPRING_CHANCE:
        spr = canvas.create_image(x + random.randint(0, 58), y - 17, image=img_spr, anchor="nw", tags="gameObject")
        sprs.append(spr)

# Spawn Enemies
    if score > 3500 and not ens:
        enChance = min(config.MAX_ENEMY_CHANCE, config.MIN_ENEMY_CHANCE + (score - 3500) // 1000 * 0.01)
        if random.random() < enChance:
            create_enemy(canvas, y, img_en, ens, scrWid)
    return plat

def update_movingPlatforms(canvas, plats, scrWid):
    for i, platData in enumerate(plats):
        platId, platType, speed = platData
        
        if platType == "moving":
            canvas.move(platId, speed, 0)
            pos = canvas.coords(platId)[0]
            if pos <= 0 and speed < 0:
                plats[i][2] = -speed
            elif pos >= scrWid - 92 and speed > 0:
                plats[i][2] = -speed

def check_collisions(canvas, plats, sprs, verticalVelocity, playerPos, player, img_trigSpr):
    if verticalVelocity > 0:
        for i, platData in enumerate(plats):
            platId, platType, speed = platData
            platPos = canvas.coords(platId)
            platPos.append(platPos[0] + 76)
            platPos.append(platPos[1] + 18)
            if (playerPos[0] > platPos[0] and playerPos[0] < platPos[2]) or (playerPos[2] > platPos[0] and playerPos[2] < platPos[2]):
                if platPos[1] - 5 - verticalVelocity <= playerPos[3] <= platPos[1]:
                    canvas.move(player, 0, platPos[1] - playerPos[3])
                    play_sfx("sounds/bounce.wav")
                    if platType == "shattered":
                        canvas.delete(platId)
                        plats.pop(i)
                        play_sfx("sounds/crunch.wav")
                    return config.JUMP_IMPULSE
        
        for s in sprs:
            sprPos = canvas.coords(s)
            sprPos.append(sprPos[0] + 18)
            sprPos.append(sprPos[0] + 18)
            if (sprPos[0] > playerPos[0] and sprPos[0] < playerPos[2]) or (sprPos[2] > playerPos[0] and sprPos[2] < playerPos[2]):
                if sprPos[1] - 5 - verticalVelocity <= playerPos[3] <= sprPos[1]:
                    canvas.itemconfig(s, image=img_trigSpr)
                    canvas.move(s, 0, -18)
                    canvas.move(player, 0, sprPos[1] - playerPos[3])
                    play_sfx("sounds/spring.wav")
                    return config.SPRING_IMPULSE
    
    return verticalVelocity

def create_enemy(canvas, y, img_enemyRight, enemies, scrWidth):
    ex = random.randint(100, scrWidth - 100)
    enemy = canvas.create_image(ex, y, image=img_enemyRight, anchor="nw", tags="gameObject")
    directionX = config.ENEMY_SPEED_X
    directionY = config.ENEMY_SPEED_Y
    timer = random.uniform(0, 10)
    enemies.append([enemy, directionX, directionY, timer])

def update_enemies(canvas, enemies, img_enemyRight, img_enemyLeft, bullets, playerPos, scrWidth, scrHeight, onDeath_callback, verticalVelocity):

# Movement
    for i, (e, dirX, dirY, t),  in enumerate(enemies):
        t = (t + 0.07) % (2 * math.pi)
        enemies[i][3] = t
        shiftY = math.sin(t) * dirY
        canvas.move(e, dirX, shiftY)

        enPos = canvas.coords(e)
        if not enPos: continue
        enPos.append(enPos[0] + 60)
        enPos.append(enPos[1] + 60)
        if enPos[0] <= 0 and dirX < 0:
            enemies[i][1] = -dirX
            canvas.itemconfig(e, image=img_enemyRight)
        elif enPos[2] >= scrWidth and dirX > 0:
            enemies[i][1] = -dirX
            canvas.itemconfig(e, image=img_enemyLeft)

# Bullet Collision
        for b_idx, bullet in enumerate(bullets):
            bPos = canvas.coords(bullet)
            if bPos:
                if bPos[1] - 20 <= enPos[3] <= bPos[1] - 5:
                    if (enPos[0] - 20 < bPos[0] < enPos[2] + 20) or (enPos[0] -20 < bPos[2] < enPos[2] + 20):
                        play_sfx("sounds/enemy.wav")
                        canvas.delete(bullet)
                        bullets.pop(b_idx)
                        canvas.delete(e)
                        enemies.pop(i)

# Player Collision
        xCollision = (enPos[0] < playerPos[0] < enPos[2]) or (enPos [0] < playerPos[2] < enPos[2])
        if xCollision:
            if verticalVelocity > 0 and (enPos[1] - 5 - verticalVelocity <= playerPos[3] <= enPos[1]):
                play_sfx("sounds/enemy.wav")
                canvas.delete(e)
                enemies.pop(i)
                return False, config.JUMP_IMPULSE    

            if enPos[1] <= playerPos[1] <= enPos[3] - 15:
                onDeath_callback()
                return True, verticalVelocity

# Delete Enemies
        if enPos[1] > scrHeight:
            canvas.delete(e)
            enemies.pop(i)
    return False, verticalVelocity
