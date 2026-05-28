import random
import config

def create_platform(canvas, x, y, img_platform, img_spring, platforms, springs, sprChance):
    plat = canvas.create_image(x, y, image=img_platform, anchor="nw", tags="gameObject")
    platforms.append(plat)

    if sprChance < config.SPRING_CHANCE:
        springPos = random.randint(0, 50)
        spring = canvas.create_image(x + springPos, y - 17, image=img_spring, anchor="nw", tags="gameObject")
        springs.append(spring)

def create_enemy(canvas, y, img_enemy, scrWidth, enemies):
    ex = random.randint(50, scrWidth - 50)
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
        if (enPos[0] <= 0 or enPos[2] >= scrWidth):
            enemies[i][1] = -direction
        
        for b_idx, bullet in enumerate(bullets):
            bPos = canvas.coords(bullet)
            if bPos:
                if bPos[1] - 5 <= enPos[3] <= bPos[1]:
                    if (bPos[0] > enPos[0] and bPos[0] < enPos[2]) or (bPos[2] > enPos[0] and bPos[2] < enPos[2]):
                        canvas.delete(bullet)
                        bullets.pop(b_idx)
                        canvas.delete(e)
                        enemies.pop(i)
                        break
                        
        if verticalVelocity < 0:               
            if (playerPos[0] > enPos[0] and playerPos[0] < enPos[2]) or (playerPos[2] > enPos[0] and playerPos[2] < enPos[2]):
                if enPos[3] <= playerPos[1]:
                    on_death_callback()
                    return True
        else:        
            if (playerPos[0] > enPos[0] and playerPos[0] < enPos[2]) or (playerPos[2] > enPos[0] and playerPos[2] < enPos[2]):
                if enPos[1] - 5 - verticalVelocity <= playerPos[3] <= enPos[1]:
                    return config.JUMP_IMPULSE

        if enPos[1] > scrHeight:
            canvas.delete(e)
            enemies.pop(i)
    return False
