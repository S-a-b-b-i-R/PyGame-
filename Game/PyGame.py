import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))

pygame.display.set_caption("Billy the Kid")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()


maintrack = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

mark = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitBox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitBox = (self.x + 17, self.y + 11, 29, 52)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 1)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitBox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitBox[0], self.hitBox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitBox[0], self.hitBox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitBox = (self.x + 17, self.y + 2, 31, 57)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')
        pass

def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(mark), 1, (255, 0, 0))
    win.blit(text, (365, 10))
    Billy.draw(win)
    Goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# mainloop
font = pygame.font.SysFont("comicsans", 30, True)
Billy = player(200, 410, 64, 64)
Goblin = enemy(100, 410, 64, 64, 300)
shotLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if Goblin.visible:
        if Billy.hitBox[1] < Goblin.hitBox[1] + Goblin.hitBox[3] and Billy.hitBox[1] + Billy.hitBox[3] > Goblin.hitBox[1]:
            if Billy.hitBox[0] + Billy.hitBox[2] > Goblin.hitBox[0] and Billy.hitBox[0] < Goblin.hitBox[0] + Goblin.hitBox[
                2]:
                Billy.hit()
                mark -= 5

    if shotLoop > 0:
        shotLoop += 1
    if shotLoop > 3:
        shotLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < Goblin.hitBox[1] + Goblin.hitBox[3] and bullet.y + bullet.radius > Goblin.hitBox[1]:
            if bullet.x + bullet.radius > Goblin.hitBox[0] and bullet.x - bullet.radius < Goblin.hitBox[0] +Goblin.hitBox[2]:
                Goblin.hit()
                mark += 1
                bullets.pop(bullets.index(bullet))
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shotLoop == 0:
        if Billy.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(
                projectile(round(Billy.x + Billy.width // 2), round(Billy.y + Billy.height // 2), 6, (0, 0, 0), facing))
        shotLoop = 1

    if keys[pygame.K_LEFT] and Billy.x > Billy.vel:
        Billy.x -= Billy.vel
        Billy.left = True
        Billy.right = False
        Billy.standing = False
    elif keys[pygame.K_RIGHT] and Billy.x < 500 - Billy.width - Billy.vel:
        Billy.x += Billy.vel
        Billy.right = True
        Billy.left = False
        Billy.standing = False
    else:
        Billy.standing = True
        Billy.walkCount = 0

    if not Billy.isJump:
        if keys[pygame.K_UP]:
            Billy.isJump = True
            Billy.right = False
            Billy.left = False
            Billy.walkCount = 0
    else:
        if Billy.jumpCount >= -10:
            neg = 1
            if Billy.jumpCount < 0:
                neg = -1
            Billy.y -= (Billy.jumpCount ** 2) * 0.5 * neg
            Billy.jumpCount -= 1
        else:
            Billy.isJump = False
            Billy.jumpCount = 10

    redrawGameWindow()

pygame.quit()
