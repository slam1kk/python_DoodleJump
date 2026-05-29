import random
import config
import math

lastLayer, buildingLayer = [], []
maxHeight = 0

def generating(canvas, img_platform, img_spring, img_enemy, platforms, springs, enemies, scrWidth, scrHeight, score):
    global lastLayer, buildingLayer, maxHeight

    difficultyGapX = min(config.MAX_DIFFGAP_X, config.MIN_DIFFGAP_X + (score // 1000) * 25)
    difficultyGapY = min(config.MAX_DIFFGAP_Y, config.MIN_DIFFGAP_Y + (score // 1000) * 10)

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

    if not platforms:
        currIdx = 0
        lastLayer, buildingLayer = [], []
        platsNum = max(1, math.ceil(scrWidth // (difficultyGapX)))
        create_platform(canvas, scrWidth / 2, scrHeight - 100, img_platform, img_spring, img_enemy, platforms, springs, enemies, 1, score, scrWidth)
        startY = scrHeight - 120
        for i in range(platsNum):
            x = i * difficultyGapX + random.randint(0, 30)
            x = min(x, scrWidth - 76)
            y = random.randint(startY - 80, startY)
            plat = create_platform(canvas, x, y, img_platform, img_spring, img_enemy, platforms, springs, enemies, 1, score, scrWidth)
            lastLayer.append(plat)
        lowestInLayer = max(lastLayer, key=lambda p: canvas.coords(p)[1])
        maxHeight = int(canvas.coords(lowestInLayer)[1] - difficultyGapY)
        return
    
    highestPlat = min(platforms, key=lambda p: canvas.coords(p)[1])
    highestY = canvas.coords(highestPlat)[1]
    if highestY <= config.TARGET_TOP_Y: return

    platsInLayer = max(1, math.ceil(scrWidth // (difficultyGapX)))
    currIdx = len(buildingLayer)
    if currIdx >= platsInLayer:
        lastLayer = buildingLayer.copy()
        buildingLayer.clear()
        currIdx = 0
        lowestInLayer = max(lastLayer, key=lambda p: canvas.coords(p)[1])
        maxHeight = int(canvas.coords(lowestInLayer)[1] - difficultyGapY)

    if currIdx <= len(buildingLayer):
        parentPlat = lastLayer[currIdx]
    else:
        return

    parentX = canvas.coords(parentPlat)[0]

    newY = random.randint(maxHeight - 70, maxHeight)
    newX = parentX + random.randint(-difficultyGapX, difficultyGapX)
    if newX < currIdx * difficultyGapX:
        newX += difficultyGapX
    elif newX > (currIdx + 1) * difficultyGapX - 76:
        newX = newX - difficultyGapX + 76
    newX = max(currIdx * difficultyGapX + 10, min((currIdx + 1) * difficultyGapX - 76, newX))

    newPlat = create_platform(canvas, newX, newY, img_platform, img_spring, img_enemy, platforms, springs, enemies, random.random(), score, scrWidth)
    buildingLayer.append(newPlat)

def create_platform(canvas, x, y, img_platform, img_spring, img_enemy, platforms, springs, enemies, sprChance, score, scrWidth):
    plat = canvas.create_image(x, y, image=img_platform, anchor="nw", tags="gameObject")
    platforms.append(plat)

    if sprChance < config.SPRING_CHANCE:
        spr = canvas.create_image(x + random.randint(0, 58), y - 17, image=img_spring, anchor="nw", tags="gameObject")
        springs.append(spr)

    if score > 5000:
        enChance = min(config.MAX_ENEMY_CHANCE, config.MIN_ENEMY_CHANCE + (score - 3000) // 1000 * 0.01)
        if random.random() < enChance:
            create_enemy(canvas, y, img_enemy, enemies, scrWidth)

    return plat
    
def create_enemy(canvas, y, img_enemy, enemies, scrWidth):
    ex = random.randint(100, scrWidth - 100)
    enemy = canvas.create_image(ex, y, image=img_enemy, anchor="nw", tags="gameObject")
    direction = config.ENEMY_SPEED if random.random() < 0.5 else -config.ENEMY_SPEED
    enemies.append([enemy, direction])

def check_collisions(canvas, platforms, springs, verticalVelocity, playerPos):
    if verticalVelocity > 0:
        for p in platforms:
            platPos = canvas.coords(p)
            platPos.append(platPos[0] + 76)
            platPos.append(platPos[1] + 18)
            if (playerPos[0] > platPos[0] and playerPos[0] < platPos[2]) or (playerPos[2] > platPos[0] and playerPos[2] < platPos[2]):
                if platPos[1] - 5 - verticalVelocity <= playerPos[3] <= platPos[1]:
                    return config.JUMP_IMPULSE
        
        for s in springs:
            sprPos = canvas.coords(s)
            sprPos.append(sprPos[0] + 18)
            sprPos.append(sprPos[0] + 18)
            if (sprPos[0] > playerPos[0] and sprPos[0] < playerPos[2]) or (sprPos[2] > playerPos[0] and sprPos[2] < playerPos[2]):
                if sprPos[1] - 5 - verticalVelocity <= playerPos[3] <= sprPos[1]:
                    return config.SPRING_IMPULSE
    
    return verticalVelocity

def update_enemies(canvas, enemies, bullets, playerPos, scrWidth, scrHeight, on_death_callback, verticalVelocity):
    for i, (e, direction) in enumerate(enemies):
        canvas.move(e, direction, 0)
        enPos = canvas.coords(e)
        if not enPos: continue
        enPos.append(enPos[0] + 60)
        enPos.append(enPos[1] + 60)
        # if (enPos[0] <= 0 or enPos[2] >= scrWidth):
        #     enemies[i][1] = -direction
        if enPos[0] <= 0 and direction < 0:
            enemies[i][1] = -direction
        elif enPos[2] >= scrWidth and direction > 0:
            enemies[i][1] = -direction

        for b_idx, bullet in enumerate(bullets):
            bPos = canvas.coords(bullet)
            if bPos:
                if bPos[1] - 20 <= enPos[3] <= bPos[1] - 5:
                    if (enPos[0] < bPos[0] < enPos[2]) or (enPos[0] < bPos[2] < enPos[2]):
                        canvas.delete(bullet)
                        bullets.pop(b_idx)
                        canvas.delete(e)
                        enemies.pop(i)
                        break
                        
        if verticalVelocity < 0:               
            if (enPos[0] < playerPos[0] < enPos[2]) or (enPos [0] < playerPos[2] < enPos[2]):
                if enPos[3] <= playerPos[1] <= enPos[3] + 5:
                    on_death_callback()
                    return True, verticalVelocity
        else:        
            if (enPos[0] < playerPos[0] < enPos[2]) or (enPos [0] < playerPos[2] < enPos[2]):
                if enPos[1] - 5 - verticalVelocity <= playerPos[3] <= enPos[1]:
                    canvas.delete(e)
                    enemies.pop(i)
                    return False, config.JUMP_IMPULSE

        if enPos[1] > scrHeight:
            canvas.delete(e)
            enemies.pop(i)
    return False, verticalVelocity
