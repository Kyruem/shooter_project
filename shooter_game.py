from pygame import *
from random import randint
font.init()

winlosefont = font.Font(None, 50)

winpoints = winlosefont.render("You Win!", True, (0,0,0))
lostpoints = winlosefont.render("You Lose! Git Gud!", True, (0,0,0))

scored = 0
lostpoints = 0

# region screen setup 
WIDTH, HEIGHT = 700, 600
window = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
# endregion screen setup

# region classes
class ImageSprite(sprite.Sprite):
    # constructor function. Runs ONCE every time a new object it's created
    def __init__(self, filename, pos, size):
        super().__init__()
        self.image = image.load(filename)
        self.image = transform.scale(self.image, size)
        self.rect = Rect(pos, size)
        self.initial_pos = pos

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def reset(self):
        self.rect.topleft = self.initial_pos

class PlayerSprite(ImageSprite):
    def update(self):
        keys = key.get_pressed()
        # if keys[K_s]:
        #     self.rect.y += 8
        # if keys[K_w]:
        #     self.rect.y -= 8
        if keys[K_d]:
            self.rect.x += 7
        if keys[K_a]:
            self.rect.x -= 7

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        # if self.rect.top < 0:
        #     self.rect.top = 0
        # if self.rect.bottom > HEIGHT:
        #     self.rect.bottom = HEIGHT
    def shoot(self):
        bullet = BulletSprite(filename="bullet2.png", pos=(0,0), size=(100,100))
        bullet.rect.center = self.rect.midtop
        bullets.add(bullet)
        

    def collision(self, other_sprite):
        col = sprite.collide_rect(self,other_sprite)
        return col

class EnemySprite(ImageSprite):
    def __init__(self, filename, pos, size, speed):
        super().__init__(filename, pos, size)
        self.speed = Vector2(speed)

    def update(self):
        self.rect.topleft += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH-self.rect.width)

class BulletSprite(ImageSprite):
    def update(self):
        self.rect.y -= 6
        if self.rect.bottom < 0:
            self.kill()

# endregion classes

# region sprite
bg = ImageSprite(filename="shooterback.png", pos=(0,0), size=(WIDTH,HEIGHT))
player = PlayerSprite(filename="RogueFalcon.gif", pos=(350, 525), size=(75, 75))
shield = PlayerSprite(filename="Shield.png", pos=(335,500), size=(100,100))
enemys = sprite.Group()
bullets = sprite.Group()

def create_enemy():
    x = randint(0,WIDTH-50)
    y = -50
    speed = randint(3,5)
    enemy = EnemySprite(filename="Homing.png", pos=(x, y), size=(30, 40), speed=(0,speed))
    enemys.add(enemy)
#for i in range(0,75):
 #   enemy = EnemySprite(filename="Homing.png", pos=(enemypos, randint(0, 9) * 10), size=(50, 50))
  #  enemys.append(enemy)

# region loop
for i in range(50):
    create_enemy()

while not event.peek(QUIT):
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_UP:
                player.shoot()
    
    bg.draw(window)
    
    counter = winlosefont.render("Score: " + str(scored), True, (0,0,0))
    window.blit(counter, (0,0))

    lost = winlosefont.render("Lost: " + str(lostpoints), True, (0,0,0))
    window.blit(lost, (0,50))

    shield.draw(window)
    shield.update()
    player.draw(window)
    player.update()
    enemys.draw(window)
    enemys.update()
    bullets.draw(window)
    bullets.update()

    p_collision = sprite.spritecollide(shield, enemys, True)
    for collision in p_collision:
        lostpoints += 1
        create_enemy()

    b_collision = sprite.groupcollide(enemys, bullets, True, True)
    for collision in b_collision:
        scored += 1
        create_enemy()
    # for enemy in enemys:
    #     enemypos = randint(0, 700)
    #     enemy.draw(window)
    #     enemy.update()
    #     if shield.collision(enemy) == True:
    #         enemys.remove(enemy)
    #         enemy = EnemySprite(filename="Homing.png", pos=(enemypos, 0), size=(50, 50))
    #         enemys.append(enemy)
            
    display.update()
    clock.tick(100)
# endregion loop