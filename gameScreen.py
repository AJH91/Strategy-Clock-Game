import pygame
import random
import time
import csv
from button import Button

#Initialize pygame
pygame.init()
FPS = 60

#game window + variables
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
SIDE_MARGIN = 200
ROWS = 17
MAX_COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 16
MAX_LEVELS = 7
screen_scroll = 0
screen = pygame.display.set_mode((SCREEN_WIDTH-SIDE_MARGIN, SCREEN_HEIGHT))
pygame.display.set_caption('Strategy Clock Game')
level = 0
current_score = 0

#loading screen, main menu, images for it all etc
start_game = 4
clockLoadingImg = pygame.image.load("Images/Clock/Clock.png")
clockLoadingImg = pygame.transform.scale(clockLoadingImg, (50,50))
clockNormalImage = pygame.image.load("Images/Clock/Clock.png")
clockNormalImage = pygame.transform.scale(clockNormalImage, (300,300))
newGameImg = pygame.image.load("Images/new.png")
newGameImg = pygame.transform.scale(newGameImg, (50,50))
restartGameImg = pygame.image.load("Images/refresh.png")
restartGameImg = pygame.transform.scale(restartGameImg, (150,150))
exitGameImg = pygame.image.load("Images/exit.png")
exitGameImg = pygame.transform.scale(exitGameImg, (50,50))
mainScreenImg = pygame.image.load("Images/homepage.png")
mainScreenImg = pygame.transform.scale(mainScreenImg, (50,50))
controlsScreenImg = pygame.image.load("Images/monitoring.png")
controlsScreenImg = pygame.transform.scale(controlsScreenImg, (50,50))
blackScreenImg = pygame.image.load("Images/black_screen.png")
blackScreenImg = pygame.transform.scale(blackScreenImg, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Bullet, missiles etc trajectory and groups
playerBulletImg1 = pygame.image.load("Images/beans_shrunk.png") #This bullet image will be used for non-competitive enemies
playerBulletImg2 = pygame.image.load("Images/nuevo-sol.png") #This bullet image will be used for price-competitive enemies
playerBulletImg2 = pygame.transform.scale(playerBulletImg2, (30,30))
playerBulletImg3 = pygame.image.load("Images/floppy-disk.png") #This bullet image will be used for hybrid strategy enemies
playerBulletImg3 = pygame.transform.scale(playerBulletImg3, (30,30))
playerBulletImg4 = pygame.image.load("Images/expensiveCompany.png")

enemyBulletImg1 = pygame.image.load("Images/beans_shrunk.png") #This bullet image will be used for low-price enemies
enemyBulletImg1 = pygame.transform.scale(enemyBulletImg1, (30,30))
enemyBulletImg2 = pygame.image.load("Images/nuevo-sol.png") # This bullet will be used for price-competitive enemies
enemyBulletImg2 = pygame.transform.scale(enemyBulletImg2, (30,30))
enemyBulletImg3 = pygame.image.load("Images/floppy-disk.png") # This image will be used for hybrid strategies
enemyBulletImg3 = pygame.transform.scale(enemyBulletImg3, (30,30))
enemyBulletImg4 = pygame.image.load("Images/expensiveCompany.png") #This bullet image will be used for the differentiated enemies
enemyBulletImg4 = pygame.transform.scale(enemyBulletImg4, (30,30))

#creating spriteGroups
bulletGroup = pygame.sprite.Group()
enemyBulletGroup = pygame.sprite.Group()
enemyGroup0 = pygame.sprite.Group() #non competitive
itemDropsGroup = pygame.sprite.Group()
finishFlagGroup = pygame.sprite.Group()
bulletGroup2 = pygame.sprite.Group() #low price
enemyGroup2 = pygame.sprite.Group()
bulletGroup3 = pygame.sprite.Group() #hybrid
enemyGroup3 = pygame.sprite.Group()
bulletGroup4 = pygame.sprite.Group() #differentiated
enemyGroup4 = pygame.sprite.Group()
bossGroup1 = pygame.sprite.Group()#non competitive
bossGroup2 = pygame.sprite.Group()#low price
bossGroup3 = pygame.sprite.Group()#hybrid
bossGroup4 = pygame.sprite.Group()#differentiated

#define fonts
font = pygame.font.SysFont('arial', 30)
small_font = pygame.font.SysFont('arial', 15)

#loading tile images
img_list = []
for x in range(16):
    img = pygame.image.load(f'Images/Tiles/{x}.png')
    img = pygame.transform.scale(img, (48, 48))
    img_list.append(img)

def drawTextOnScreen(text, font, colourText, x, y):
    image = font.render(text, True, colourText)
    screen.blit(image, (x,y))

def restartLevel():
    enemyGroup0.empty()
    enemyGroup2.empty()
    enemyGroup3.empty()
    enemyGroup4.empty()
    bulletGroup.empty()
    enemyBulletGroup.empty()
    itemDropsGroup.empty()
    finishFlagGroup.empty()
    bulletGroup3.empty()
    bulletGroup4.empty()
    bossGroup1.empty()
    bossGroup2.empty()
    bossGroup3.empty()
    bossGroup4.empty()

    #make another empty tile list
    data = []
    for x in range(ROWS):
        r = [-1] * MAX_COLUMNS
        data.append(r)
    return data

class Player(pygame.sprite.Sprite):
    def __init__(self,x, y, imageToLoad,speed):
        pygame.sprite.Sprite.__init__(self)
        self.img = imageToLoad
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.width = self.rect.width
        self.height = self.rect.height
        self.speed = speed
        #checking to see which direction they are facing on x-axis.
        #1 is equal to right, so character is initialized facing right
        self.x_Axis_direction = 1
        self.X_axis_Flip = False
        self.y_axis_direction = 0
        self.y_axis_direction = False
        #Current direction of player. 12 is facing north, 3 is facing east, 6 is facing south, 9 is facing west
        self.playerDirection = 3
        #how fast they can actually fire their gun, has nothing to do with how fast the bullets move
        self.gunShootingSpeed = 0
        self.ammo = 100
        self.maxAmmo = 250
        self.alive = True
        #health of the player
        self.health = 100
        self.maxHealth = 100

    def getDirection(self):
        return self.playerDirection

    def draw_image(self):
       pygame.draw.rect(screen, "RED", self.rect, 1)
       screen.blit(pygame.transform.flip(self.img,self.X_axis_Flip,False),(self.rect.x, self.rect.y))

    def move(self, moving_left, moving_right, moving_up, moving_down, jumping, falling):

        #movement change based on the x and y axis
        XChange = 0
        YChange= 0
        screen_scroll = 0

        #horizontal movement
        if moving_left:
            XChange = -(self.speed)
            self.X_axis_Flip = True
            self.x_Axis_direction = -1
            self.playerDirection = -9
        if moving_right:
            XChange = self.speed
            self.X_axis_Flip = False
            self.x_Axis_direction = 1
            self.playerDirection = 3
        #vertical movement
        if moving_up:
            YChange = -(self.speed)
            self.playerDirection = 12
            self.rotate_image(self.playerDirection)
        if moving_down:
            YChange = self.speed
            self.playerDirection = 6
            self.rotate_image(self.playerDirection)

        for tile in world.obstacle_list:
            #world obstacle list only consists of the environment objects, which cant be moved through
            #checks collision based on the x axis
            if tile[1].colliderect(self.rect.x + XChange, self.rect.y, self.height, self.width):
                XChange = 0
            #checks collision based on the y axis
            if tile[1].colliderect(self.rect.x + XChange, self.rect.y + YChange, self.height, self.width):
                YChange = 0

        #if the enemy physically hits the player, the player health is reduced
        if pygame.sprite.spritecollide(self, enemyGroup0 or enemyGroup2 or enemyGroup3 or enemyGroup4 or bossGroup1 or bossGroup2 or bossGroup3 or bossGroup4, False):
            self.health -=1

        #moving onto next level section#
        level_complete = False
        if current_score == 3:
            #The user can only progress to the next level if they have killed all the enemies + hit finish line
            if pygame.sprite.spritecollide(self, finishFlagGroup, True):
                   level_complete = True

        self.rect.x += XChange
        self.rect.y += YChange

        if self.rect.left + XChange < 0 or self.rect.right + XChange > SCREEN_WIDTH:
            XChange = 0
            screen_scroll = XChange

        # movement so that the screen will scroll
        if self.rect.right > (SCREEN_WIDTH - SIDE_MARGIN) or self.rect.left < SIDE_MARGIN:
            self.rect.x -= XChange
            screen_scroll = -(XChange)

        return screen_scroll, level_complete

    def rotate_image(self, direction):
        #rotates the image based upon the direction they are "looking" at
        if direction == 12:
            rotated_img = pygame.transform.rotate(self.img, 90)
            screen.blit(rotated_img, (self.rect.x, self.rect.y))
        if direction == 6:
            rotated_img = pygame.transform.rotate(self.img, -90)
            screen.blit(rotated_img, (self.rect.x, self.rect.y))
        if direction == 9:
            rotated_img = pygame.transform.rotate(self.img, -180)
            screen.blit(rotated_img, (self.rect.x, self.rect.y))

    def shoot_gun(self,bulletImg,screen,bulletGroup,attackType):
         if attackType==1:
           if self.gunShootingSpeed == 0 and self.ammo > 0:
                directionBulletSpawn = self.getDirection()
                if directionBulletSpawn == 3:
                    bullet = Bullet(self.rect.x + 60, self.rect.y + 15, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -=1
                if directionBulletSpawn == 6:
                    bullet = Bullet(self.rect.x + 40, self.rect.y + 60, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1
                if directionBulletSpawn == -9:
                    bullet = Bullet(self.rect.x - 15, self.rect.y + 15, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1
                if directionBulletSpawn == 12:
                    bullet = Bullet(self.rect.x + 20, self.rect.y - 15, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1
         if attackType ==2:
             if self.gunShootingSpeed == 0 and self.ammo > 0:
                 directionBulletSpawn = self.getDirection()
                 if directionBulletSpawn == 3:
                     bullet = Bullet(self.rect.x + 60, self.rect.y + 15, self.getDirection(),
                                     bulletImg, screen)
                     bulletGroup2.add(bullet)
                     self.gunShootingSpeed = 40
                     self.ammo -= 1
                 if directionBulletSpawn == 6:
                     bullet = Bullet(self.rect.x + 40, self.rect.y + 60, self.getDirection(),
                                     bulletImg, screen)
                     bulletGroup2.add(bullet)
                     self.gunShootingSpeed = 40
                     self.ammo -= 1
                 if directionBulletSpawn == -9:
                     bullet = Bullet(self.rect.x - 15, self.rect.y + 15, self.getDirection(),
                                     bulletImg, screen)
                     bulletGroup2.add(bullet)
                     self.gunShootingSpeed = 40
                     self.ammo -= 1
                 if directionBulletSpawn == 12:
                     bullet = Bullet(self.rect.x + 20, self.rect.y - 15, self.getDirection(),
                                     bulletImg, screen)
                     bulletGroup2.add(bullet)
                     self.gunShootingSpeed = 40
                     self.ammo -= 1

         if attackType == 3:
            if self.gunShootingSpeed == 0 and self.ammo > 0:
                directionBulletSpawn = self.getDirection()
                if directionBulletSpawn == 3:
                    bullet = Bullet(self.rect.x + 60, self.rect.y + 15, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup3.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1
                if directionBulletSpawn == 6:
                    bullet = Bullet(self.rect.x + 40, self.rect.y + 60, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup2.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1
                if directionBulletSpawn == -9:
                    bullet = Bullet(self.rect.x - 15, self.rect.y + 15, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup3.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1
                if directionBulletSpawn == 12:
                    bullet = Bullet(self.rect.x + 20, self.rect.y - 15, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup3.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1

         if attackType == 4:
            if self.gunShootingSpeed == 0 and self.ammo > 0:
                directionBulletSpawn = self.getDirection()
                if directionBulletSpawn == 3:
                    bullet = Bullet(self.rect.x + 60, self.rect.y + 15, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup4.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1
                if directionBulletSpawn == 6:
                    bullet = Bullet(self.rect.x + 40, self.rect.y + 60, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup4.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1
                if directionBulletSpawn == -9:
                    bullet = Bullet(self.rect.x - 15, self.rect.y + 15, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup4.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1
                if directionBulletSpawn == 12:
                    bullet = Bullet(self.rect.x + 20, self.rect.y - 15, self.getDirection(),
                                    bulletImg, screen)
                    bulletGroup4.add(bullet)
                    self.gunShootingSpeed = 40
                    self.ammo -= 1

    def update(self):
        if self.gunShootingSpeed >0:
            self.gunShootingSpeed -= 1
        self.check_health_level()

    def check_health_level(self):
        if self.health <=0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        for y,row in enumerate(data):
            for x, tile in enumerate(row):
                    if tile == 15:
                        img = img_list[tile]
                        img_rect = img.get_rect()
                        img_rect.center = x * TILE_SIZE, y * TILE_SIZE
                        tile_data = (img, img_rect)
                        self.obstacle_list.append(tile_data)
                    elif tile ==0:
                        enemy = Enemy(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[0], 1, "Non Competitive")
                        enemyGroup0.add(enemy)
                    elif tile == 1:
                        #create boss mob for Non-competitive strategy
                        bossEnemy = Enemy(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[1], 1, "Non Competitive")
                        bossGroup1.add(bossEnemy)
                    elif tile==2:
                        # create normal mob for Differentiated
                        enemy = Enemy(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[2], 1, "Differentiated")
                        enemyGroup2.add(enemy)
                    elif tile == 3:
                        #create boss mob for Differentiated
                        bossEnemy = Enemy(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[3], 1, "Differentiated")
                        bossGroup2.add(bossEnemy)
                    elif tile == 4:
                        # create normal mob for Hybrid Strategy
                        enemy = Enemy(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[4], 1, "Hybrid Strategy")
                        enemyGroup3.add(enemy)
                    elif tile == 5:
                        #create boss mob for Hybrid Strategy
                        bossEnemy = Enemy(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[5], 1, "Hybrid Strategy")
                        bossGroup3.add(bossEnemy)
                    elif tile == 6:
                        #create normal mob for Low Price Strategy
                        enemy = Enemy(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[6], 1, "Low Price")
                        enemyGroup4.add(enemy)
                    elif tile == 7:
                        #create boss mob for Low Price Strategy
                        bossEnemy = Enemy(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[7], 1, "Low Price")
                        bossGroup4.add(bossEnemy)
                    elif tile == 8:
                        #create player class
                        player = Player(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[8], 1)
                        health_Bar = Healthbar(10, 30, player.health, player.maxHealth)
                        ammo_Bar = Ammobar(10, 100, player.ammo, player.maxAmmo)
                        score_Bar = Score(10, 170, current_score, 3)
                    elif tile ==9:
                        #this is the tile for the finish line
                        finishFlagItem = finishFlag(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[9], screen)
                        finishFlagGroup.add(finishFlagItem)
                    elif tile == 10:
                        #create lightning power up class
                        lightningItem = ItemBox(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[10], screen, "Lightning")
                        itemDropsGroup.add(lightningItem)
                    elif tile == 11:
                        #create healthbox
                        healthItem = ItemBox(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[11], screen, "Health Box")
                        itemDropsGroup.add(healthItem)
                    elif tile == 12:
                        #create ammobox
                        ammoItem = ItemBox(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[12], screen, "Ammo Box")
                        itemDropsGroup.add(ammoItem)
                    elif tile == 13:
                        #create nuclearbox
                        nuclearItem = ItemBox(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[13], screen, "Nuclear")
                        itemDropsGroup.add(nuclearItem)
                    elif tile == 14:
                        # create dynamite
                        dynamiteItem = ItemBox(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[14], screen, "Dynamite")
                        itemDropsGroup.add(dynamiteItem)
                    elif tile == 16:
                        finishFlagItem = ItemBox(x * TILE_SIZE / 2, y * TILE_SIZE, img_list[6], screen, "Finish Flag")
                        finishFlagGroup.add(finishFlagItem)

        return player, health_Bar, ammo_Bar, score_Bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], (tile[1], ))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xcoordinate, ycoordinate,direction,image, screen):
        pygame.sprite.Sprite.__init__(self)
        self.velocity = 1
        self.image = image
        self.xcoordinate = xcoordinate
        self.ycoordinate = ycoordinate
        self.rect = self.image.get_rect()
        self.rect.center = (xcoordinate, ycoordinate)
        self.screen = screen
        self.direction = direction
        #rotates the bullet image based upon the direction
        if direction == 6:
            rotated_img = pygame.transform.rotate(self.image, -90)
            self.image = rotated_img
        if direction == -9:
            rotated_img = pygame.transform.rotate(self.image, -180)
            self.image = rotated_img
        if direction == 12:
            rotated_img = pygame.transform.rotate(self.image, 90)
            self.image = rotated_img

    def update(self):
        #which direction the bullets will actually go, when fired
        if self.direction == 12:
            self.rect.y -=  (self.direction * self.velocity)
        elif self.direction == 6:
            self.rect.y += (self.direction * self.velocity)
        else:
            self.rect.x += (self.direction * self.velocity)

        #check if bullet has left screen
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
           self.kill()

        #bullets cant shoot through anything in obstacle list, upon collision it will immediately kill itself.
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #collision detecting, seeing if bullets are hitting anything
        #non competitive mob group
        for enemy in enemyGroup0:
            # this part to change which enemies are susceptible to which attacks
            if pygame.sprite.spritecollide(enemy, bulletGroup, False):
                if enemy.alive:
                    enemy.health -=25
                    self.kill()

        for enemy in enemyGroup2:
            # this part to change which enemies are susceptible to which attacks
            if pygame.sprite.spritecollide(enemy, bulletGroup4, False):
                if enemy.alive:
                    enemy.health -=25
                    self.kill()

        for enemy in enemyGroup3:
            # this part to change which enemies are susceptible to which attacks
            if pygame.sprite.spritecollide(enemy, bulletGroup3, False):
                if enemy.alive:
                    enemy.health -=25
                    self.kill()

        for enemy in enemyGroup4:
            # this part to change which enemies are susceptible to which attacks
            if pygame.sprite.spritecollide(enemy, bulletGroup2, False):
                if enemy.alive:
                    enemy.health -=25
                    self.kill()

        for enemy in bossGroup1:
            # this part to change which enemies are susceptible to which attacks
            if pygame.sprite.spritecollide(enemy, bulletGroup, False):
                if enemy.alive:
                    enemy.health -= 10
                    self.kill()

        for boss in bossGroup2:
            # this part to change which enemies are susceptible to which attacks
            if pygame.sprite.spritecollide(boss, bulletGroup4, False):
                if boss.alive:
                    boss.health -=10
                    self.kill()

        for boss in bossGroup3:
            # this part to change which enemies are susceptible to which attacks
            if pygame.sprite.spritecollide(boss, bulletGroup3, False):
                if boss.alive:
                    boss.health -=10
                    self.kill()

        for boss in bossGroup4:
            # this part to change which enemies are susceptible to which attacks
            if pygame.sprite.spritecollide(boss, bulletGroup2, False):
                if boss.alive:
                    boss.health -=10
                    self.kill()

class enemyBullets(Bullet):
    def __init__(self, xcoordinate, ycoordinate, direction, image, screen):
        super().__init__(xcoordinate,ycoordinate,direction,image,screen)
        if direction == 6:
            rotated_img = pygame.transform.rotate(self.image, 90)
            self.image = rotated_img

    def update(self):
        #which direction the bullets will actually go, when fired
        self.rect.y += (self.direction * self.velocity)
        #check if bullet has left screen
        if self.rect.x < 0 or self.rect.x > 1000 or self.rect.y < 0 or self.rect.y > 800:
           self.kill()
        #collision detecting, seeing if bullets are hitting anything
        if pygame.sprite.spritecollide(player, enemyBulletGroup, False):
                if player.alive:
                    player.health -=25
                    self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

class finishFlag(pygame.sprite.Sprite):
    def __init__(self,x,y,image,screen):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image
        self.screen = screen
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += screen_scroll

class Score():
    def __init__(self, x, y, score, max_score):
        self.x = x
        self.y = y
        self.score = score
        self.max_score = max_score

    def draw(self, new_score):
        self.score = new_score
        ratio = self.score / self.max_score
        pygame.draw.rect(screen, "RED", (self.x, self.y, 200, 20))
        pygame.draw.rect(screen, "GREEN", (self.x, self.y, 200 * ratio, 20))

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, xcoordinate, ycoordinate, image, screen, itemType):
        pygame.sprite.Sprite.__init__(self)
        self.xcoordinate = xcoordinate
        self.ycoordinate = ycoordinate
        self.image = image
        self.screen = screen
        self.itemType = itemType
        self.rect = self.image.get_rect()
        self.rect.center = (xcoordinate, ycoordinate)

    def update(self):
        #Checks if player hits the box
        #All the items which a player could touch should be in here.

        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, player):

           if self.itemType == "Health Box":
               player.health += 25
               if player.health > 100:
                   player.health = 100

           elif self.itemType == "Ammo Box":
               player.ammo +=150
               if player.ammo > player.maxAmmo:
                   player.ammo = player.maxAmmo

           elif self.itemType == "Nuclear":
               player.ammo +=100
               if player.ammo > player.maxAmmo:
                   player.ammo = player.maxAmmo
               player.speed+=1
               player.health-=50
               if player.health <=0:
                   player.health = 0
                   player.alive = False

           elif self.itemType == "Dynamite":
               player.health -=25
               if player.health <=0:
                   player.health = 0
                   player.alive = False

           elif self.itemType == "Lightning":
                player.speed +=1

           self.kill()

class Healthbar():
    def __init__(self, x,y, health, maxHealth):
        self.x = x
        self.y = y
        self.health = health
        self.maxHealth = maxHealth

    def draw(self, new_health):
        self.health = new_health
        ratio = self.health / self.maxHealth
        pygame.draw.rect(screen, "RED", (self.x, self.y, 200, 20))
        pygame.draw.rect(screen, "GREEN", (self.x, self.y, 200 * ratio, 20))

class Ammobar():
    def __init__(self,x,y,ammo, maxAmmo):
        self.x = x
        self.y = y
        self.ammo = ammo
        self.maxAmmo = maxAmmo

    def draw(self, new_ammo):
        self.ammo = new_ammo
        ratio = self.ammo / self.maxAmmo
        pygame.draw.rect(screen, "RED", (self.x, self.y, 200, 20))
        pygame.draw.rect(screen, "GREEN", (self.x, self.y, 200 * ratio, 20))

class Enemy(Player):
    def __init__(self, x, y, imageToLoad, speed, enemyType):
        super().__init__(x, y, imageToLoad, speed)
        self.enemyType = enemyType
        self.enemyDirection = 3

    def getEnemyDirection(self):
        return self.enemyDirection

    def rotateImage(self):
        self.image = pygame.transform.rotate(self.img, 90)

    def enemyLogic(self):
        # Current direction of enemy. 12 is facing north, 3 is facing east, 6 is facing south, 9 is facing west
        enemy_moving_right = False
        enemy_moving_left = False
        enemy_moving_south = False
        enemy_moving_north = False

        if self.alive and player.alive:
            if self.rect.x > SCREEN_WIDTH:
                self.rect.x = SCREEN_WIDTH - 5
                directionNumbers = [6, 9, 12]
                randomSelect = random.randint(0, 2)
                self.enemyDirection = directionNumbers[randomSelect]

            if self.rect.x < 0:
                self.rect.x = 5
                directionNumbers = [3, 9, 12]
                randomSelect = random.randint(0, 2)
                self.enemyDirection = directionNumbers[randomSelect]

            if self.rect.y > SCREEN_HEIGHT:
                self.rect.y = SCREEN_HEIGHT - 50
                directionNumbers = [3, 6, 9]
                randomSelect = random.randint(0, 2)
                self.enemyDirection = directionNumbers[randomSelect]

            if self.rect.y < 0:
                self.rect.y = 50
                directionNumbers = [3, 9, 12]
                randomSelect = random.randint(0, 2)
                self.enemyDirection = directionNumbers[randomSelect]

            if self.enemyDirection == 3:
                enemy_moving_right = True
                enemy_moving_left = False
                enemy_moving_south = False
                enemy_moving_north = False
            if self.enemyDirection == 6:
                enemy_moving_south = True
                enemy_moving_left = False
                enemy_moving_right = False
                enemy_moving_north = False
            if self.enemyDirection == 9:
                enemy_moving_left = True
                enemy_moving_right = False
                enemy_moving_north = False
                enemy_moving_south = False
            if self.enemyDirection == 12:
                enemy_moving_north = True
                enemy_moving_right = False
                enemy_moving_left = False
                enemy_moving_south = False

            self.rect.x +=screen_scroll
            self.move(enemy_moving_left, enemy_moving_right, enemy_moving_north, enemy_moving_south, False, False)

    def move(self, moving_left, moving_right, moving_up, moving_down, jumping, falling):

        #movement change based on the x and y axis
        XChange = 0
        YChange= 0

        #randomly makes the enemy movement faster
        movementSpeedIncrease = random.randint(0,10)
        if movementSpeedIncrease == 1:
            self.speed =2

        #horizontal movement
        if moving_left:
            XChange = -(self.speed)
            self.X_axis_Flip = True
            self.x_Axis_direction = -1
            self.playerDirection = -9
        if moving_right:
            XChange = self.speed
            self.X_axis_Flip = False
            self.x_Axis_direction = 1
            self.playerDirection = 3
        #vertical movement
        if moving_up:
            YChange = -(self.speed)
            self.playerDirection = 12
            self.rotate_image(self.playerDirection)
        if moving_down:
            YChange = self.speed
            self.playerDirection = 6
            self.rotate_image(self.playerDirection)

        for tile in world.obstacle_list:
            #checks collision based on the x axis
            if tile[1].colliderect(self.rect.x + XChange, self.rect.y, self.height, self.width):
                #if enemy hits an environment tile, their direction will randomly change
                directionNumbers = [3,6,9,12]
                randomSelect = random.randint(0, 3)
                self.enemyDirection = directionNumbers[randomSelect]
                XChange = 1

            #checks collision bassed on the y axis
            if tile[1].colliderect(self.rect.x + XChange, self.rect.y + YChange, self.height, self.width):
                YChange = 0
                self.enemyDirection = 12

        self.rect.x += XChange
        self.rect.y += YChange


    def enemy_shoot_gun(self, bulletImg, screen):

        if self.gunShootingSpeed == 0 and self.ammo > 0:
            # if they are going left or right and they are above the bottom level, then shoot down
            enemybullet = enemyBullets(self.rect.x + 20, self.rect.y + 50, 6,
                                           bulletImg, screen)
            enemyBulletGroup.add(enemybullet)
            self.gunShootingSpeed = 40
            self.ammo -= 1

#Setting the clock
clock = pygame.time.Clock()

#Background images
backgroundImg = pygame.image.load("Images/BG/en2k_9suf_181204.jpg")
backgroundImg = pygame.transform.scale(backgroundImg, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Creating basic player movement + actions
player_moving_left = False
player_moving_right = False
player_moving_up = False
player_moving_down = False
player_jumping = False
player_shooting = False
player_falling = False
player_attack2 = False
player_attack3 = False
player_attack4 = False

#Create start, load game buttons
start_button = Button(50, 50, newGameImg, screen)
clock_button = Button(135, 50, clockLoadingImg,screen)
control_screen_button = Button(90, 150, controlsScreenImg, screen)
back_to_main_screen_button = Button(600, 700, mainScreenImg,screen)
back_to_main_screen_button2 = Button(50,50,mainScreenImg,screen)
restart_button = Button(SCREEN_WIDTH /2-100, SCREEN_HEIGHT /2-100, restartGameImg, screen)


#filling initial list with -1 (empty)
world_data = []
for x in range(ROWS):
    r = [-1] * MAX_COLUMNS
    world_data.append(r)

#populating the world data list, might need to double check this.
with open(f'Levels/level{level}.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
    print("Level loaded")

world = World()
player, health_Bar, ammo_Bar, score_Bar = world.process_data(world_data)

gameActive = True
while (gameActive):

    #Game has not started, in main menu
    if start_game == 4:
        screen = pygame.display.set_mode((250, 250))
        pygame.display.set_caption('Main menu')
        screen.fill((0, 0, 0))
        start_button.draw()
        clock_button.draw()
        control_screen_button.draw()
        drawTextOnScreen("New Game", small_font, "Red", 40, 100)
        drawTextOnScreen("Faulkner's Clock", small_font, "Red", 120, 100)
        drawTextOnScreen("Game Controls", small_font, "Red", 70, 200)

        if start_button.has_been_clicked():
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            start_game = 1
        if clock_button.has_been_clicked():
            start_game = 0
        if control_screen_button.has_been_clicked():
            start_game = 2

    #Explanation of Faulkner's Clock and what to do with the game
    elif start_game ==0:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(clockNormalImage, (500, 150))
        drawTextOnScreen("Faulkner's Clock", font, "RED", 550, 35)
        drawTextOnScreen(f"Faulkner's Clock is an analytical tool used to ascertain which ",small_font, "RED", 45, 135)
        drawTextOnScreen(f"generic strategy an organisation is using.", small_font, "RED", 45, 155)

        #paragraph space

        drawTextOnScreen(f"In this game, you will be exposed to the four generic strategies ", small_font, "RED", 45, 185)
        drawTextOnScreen(f"in the form of an enemy and the only way to defeat the enemy ", small_font, "RED", 45, 205)
        drawTextOnScreen(f"is to use the correct weapon for that specific enemy.", small_font, "RED", 45, 225)

        # paragraph space
        drawTextOnScreen(f"Non-competitive monsters are only susceptible to non-competitive",small_font,"RED",45,275)
        drawTextOnScreen(f"attacks, which can be found by holding down the '1' key.", small_font,"RED",45,295)
        drawTextOnScreen(f"Non competitive monsters will be represented as this monster....", small_font, "RED", 45, 315)
        screen.blit(img_list[0], (400, 315))
        drawTextOnScreen(f"Non-competitive strategies can be succinctly defined as where", small_font, "RED", 45, 350)
        drawTextOnScreen(f"a company is charging too high of a price for too low of a quality product.", small_font, "RED", 45, 370)

        #paragraph space
        drawTextOnScreen(f"Price-competitive strategies are only susceptible to price-competitive attacks, ", small_font, "RED",45, 440)
        drawTextOnScreen(f"which can be found by holding down the '2' key.", small_font, "RED", 45, 460)
        drawTextOnScreen(f"Price competitive strategies will be represented as this monster....", small_font, "RED", 45, 480)
        screen.blit(img_list[7], (400, 500))
        drawTextOnScreen(f"Price-competitive strategies can be succinctly defined as where a company is ",small_font, "RED", 45, 550)
        drawTextOnScreen(f"competing on price alone, with the ultimate aim to be the cheapest option.", small_font,"RED", 45, 570)

        #paragraph space
        drawTextOnScreen(f"Hybrid strategies monsters are only susceptible to hybrid attacks, ",small_font, "RED", 845, 135)
        drawTextOnScreen(f"which can be found by holding down the '3' key. ", small_font, "RED",845, 155)
        drawTextOnScreen(f"Hybrid monsters will be represented as this monster....", small_font, "RED", 845, 175)
        screen.blit(img_list[4], (1150, 175))
        drawTextOnScreen(f"Hybrid strategies can be succinctly defined as where ", small_font,"RED", 845, 225)
        drawTextOnScreen(f"a company is competing on both low-price and offering differentiated products.", small_font, "RED", 845, 245)

        #paragraph space

        drawTextOnScreen(f"Differentiated strategies monsters are only susceptible to differentiated attacks, ", small_font, "RED", 845,340)
        drawTextOnScreen(f"which can be found by holding down the '4' key. ", small_font, "RED", 845, 360)
        drawTextOnScreen(f"Differentiated monsters will be represented as this monster....", small_font, "RED", 845, 380)
        screen.blit(img_list[2], (1200, 380))
        drawTextOnScreen(f"Differentiated strategies can be succinctly defined as where", small_font, "RED", 845, 430)
        drawTextOnScreen(f"a company is competing on the quality of its products, regardless of the price.", small_font, "RED", 845, 450)

        #paragraph space
        drawTextOnScreen(f"To complete the game, enemies must be killed with the attack ",small_font, "RED", 845, 540)
        drawTextOnScreen(f"that resonates with them.The finish line will only activate when ", small_font, "RED", 845,560)
        drawTextOnScreen(f"all of the enemies have been killed.", small_font, "RED", 845,580)
        drawTextOnScreen(f"Ensure that you crush your enemies!", small_font, "RED", 845, 620)


        back_to_main_screen_button.draw()
        drawTextOnScreen(f"Click button above to head back to the main screen", small_font, "RED", 510, 760)

        if back_to_main_screen_button.has_been_clicked():
            start_game =4

    elif start_game ==1:
        #game has now started

        #getting the time for when the game is started
        startTime = time.localtime()
        #colour of screen
        screen.fill((0, 0, 0))
        #add background image
        screen.blit(backgroundImg, (0, 0))

        #draw world_map
        world.draw()

        #showing text on screen
        drawTextOnScreen(f'HEALTH: {player.health}', font, "RED", 10, 50)
        drawTextOnScreen(f'AMMO: {player.ammo}', font, "RED", 10, 120)
        drawTextOnScreen(f'SCORE: {current_score}', font, "RED", 10, 190)
        #drawing ammo bar
        ammo_Bar.draw(player.ammo)
        #drawing health bar
        health_Bar.draw(player.health)
        score_Bar.draw(current_score)

        #drawing player onto screen
        player.draw_image()
        player.update()

        if level == 0:
        #drawing enemy onto screen
            for enemy in enemyGroup0:
                enemy.update()
                enemy.draw_image()
                enemy.enemyLogic()
                if not enemy.alive:
                    current_score+=1

            # dictates what time the enemy will shoot
            if (startTime[5]) % 5 == 0:
                enemy.enemy_shoot_gun(enemyBulletImg1,screen)

        elif level == 1:
            for boss in bossGroup1:
                boss.update()
                boss.draw_image()
                boss.enemyLogic()
                if not boss.alive:
                    current_score += 1

            # dictates what time the enemy will shoot
            if (startTime[5]) % 5 == 0:
                boss.enemy_shoot_gun(enemyBulletImg1, screen)


        elif level ==2:
        # drawing enemy onto screen
            for enemy2 in enemyGroup2:
                enemy2.update()
                enemy2.draw_image()
                enemy2.enemyLogic()
                if not enemy2.alive:
                    current_score += 1

            # dictates what time the enemy will shoot
            if (startTime[5]) % 5 == 0:
                enemy2.enemy_shoot_gun(enemyBulletImg4, screen)

        elif level == 3:
            for enemyb2 in bossGroup2:
                enemyb2.update()
                enemyb2.draw_image()
                enemyb2.enemyLogic()
                if not enemyb2.alive:
                    current_score += 1

               # dictates what time the enemy will shoot
            if (startTime[5]) % 5 == 0:
                enemyb2.enemy_shoot_gun(enemyBulletImg4, screen)


        elif level == 4:
        # drawing enemy onto screen
            for enemy in enemyGroup3:
                   enemy.update()
                   enemy.draw_image()
                   enemy.enemyLogic()
                   if not enemy.alive:
                        current_score += 1

                #dictates what bullet the enemy will shoot
            if (startTime[5]) % 5 == 0:
                   enemy.enemy_shoot_gun(enemyBulletImg3, screen)

        elif level == 5:
            for boss in bossGroup3:
                boss.update()
                boss.draw_image()
                boss.enemyLogic()
                if not boss.alive:
                    current_score += 1

            # dictates what time the enemy will shoot
            if (startTime[5]) % 5 == 0:
                boss.enemy_shoot_gun(enemyBulletImg3, screen)


        elif level == 6:
            for enemy in enemyGroup4:
                   enemy.update()
                   enemy.draw_image()
                   enemy.enemyLogic()
                   if not enemy.alive:
                        current_score += 1

            #dictates what bullet the enemy will shoot
            if (startTime[5]) % 5 == 0:
                   enemy.enemy_shoot_gun(enemyBulletImg2, screen)

        else:
            for boss in bossGroup4:
                boss.update()
                boss.draw_image()
                boss.enemyLogic()
                if not boss.alive:
                    current_score += 1

                if (startTime[5]) % 5 == 0:
                    boss.enemy_shoot_gun(enemyBulletImg2, screen)

        #update and draw groups
        itemDropsGroup.update()
        itemDropsGroup.draw(screen)
        finishFlagGroup.update()
        finishFlagGroup.draw(screen)
        enemyBulletGroup.draw(screen)
        enemyBulletGroup.update()
        bulletGroup.draw(screen)
        bulletGroup.update()
        bulletGroup2.draw(screen)
        bulletGroup2.update()
        bulletGroup3.draw(screen)
        bulletGroup3.update()
        bulletGroup4.draw(screen)
        bulletGroup4.update()


        if player.alive:
            #moving player
            screen_scroll, level_complete = player.move(player_moving_left, player_moving_right,player_moving_up,player_moving_down,player_jumping,player_falling)
            #if the player is shooting, this will cause the bullets to spawn.
            #bullets will spawn based upon the direction the player is looking

            #player has four different types of attacks, which are added to different bulletgroups.
            if player_shooting:
                player.shoot_gun(playerBulletImg1,screen,bulletGroup,1)
            if player_attack2:
                print("Shooting")
                player.shoot_gun(playerBulletImg2, screen, bulletGroup2,2)
            if player_attack3:
                print("Shooting")
                player.shoot_gun(playerBulletImg3, screen, bulletGroup3, 3)
            if player_attack4:
                print("Shooting")
                player.shoot_gun(playerBulletImg4, screen, bulletGroup4, 4)

            if level_complete:
                #The level has ended so now everything needs to be adjusted
                if level < MAX_LEVELS:
                    level += 1
                    world_data = restartLevel()
                    current_score = 0
                    with open(f'Levels/level{level}.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                        print("New level loaded!")
                    world = World()
                    player, health_Bar, ammo_Bar, score_Bar = world.process_data(world_data)
                else:
                    #No more levels to load, the player has finished the game.
                    #Shows a game winning screen
                    start_game = 6
                    pygame.display.set_caption('Game Over')
                    screen.blit(blackScreenImg, (0,0))
                    drawTextOnScreen("Congratulations, you have completed the game!", font, "RED", 400,300)

        else:
            # This is the restart section
            screen_scroll = 0
            screen.fill((0, 0, 0))
            restart_button.draw()
            drawTextOnScreen("Click image to restart level", font, "WHITE", 490, 500)
            if restart_button.has_been_clicked():
                world_data = restartLevel()
                with open(f'Levels/level{level}.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
                    print("Level restarted!")
                world = World()
                current_score = 0
                player, health_Bar, ammo_Bar, score_Bar = world.process_data(world_data)

    elif start_game ==2:
        #This will show the controls for the game and how the player can interact with the game itself.

        gameControlsImagesList = []
        gameControlButtonsList = []
        for x in range(1, 16):
            img = pygame.image.load(f'Images/Controls/{x}.png')
            img = pygame.transform.scale(img, (50, 50))
            gameControlsImagesList.append(img)

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game controls")
        screen.fill((0,0,0))

        drawTextOnScreen("Game Controls", font, "RED", 550, 50)
        rows =3
        columns = 5
        j=6
        k=11

        for i in range(columns):
            x=200
            y=100
            gameControlButton = Button((i*x)+250, 150, gameControlsImagesList[i], screen)
            gameControlButtonsList.append(gameControlButton)
            gameControlButtonsList[i].draw()

        drawTextOnScreen("The '1' key will fire a non-competitive attack", small_font, "RED", 50,210)
        drawTextOnScreen("The '2' key will fire a price-competitive attack", small_font, "RED", 330, 210)
        drawTextOnScreen("The '3' key will fire a hybrid attack", small_font, "RED", 600, 210)
        drawTextOnScreen("The '4' key will fire a differentiated attack", small_font, "RED", 800, 210)
        drawTextOnScreen("This is the player character", small_font, "RED", 1050, 210)

        for i in range(columns):
            a=200
            gameControlButton = Button((i * a) + 250, 350, gameControlsImagesList[j], screen)
            gameControlButtonsList.append(gameControlButton)
            gameControlButtonsList[j-1].draw()
            j+=1

        drawTextOnScreen("This will restore your health", small_font, "RED", 100, 410)
        drawTextOnScreen("This will restore your ammo ", small_font, "RED", 380, 410)
        drawTextOnScreen("Wait and find out...", small_font, "RED", 620, 410)
        drawTextOnScreen("This will greatly damage your health", small_font, "RED", 800, 410)
        drawTextOnScreen("This is the landscape", small_font, "RED", 1050, 410)

        for i in range(columns-1):
            a = 200
            gameControlButton = Button((i * a) + 295, 550, gameControlsImagesList[k], screen)
            gameControlButtonsList.append(gameControlButton)
            gameControlButtonsList[k - 1].draw()
            k+= 1

        drawTextOnScreen("The 'A' key will move your player to the left", small_font, "RED", 120, 610)
        drawTextOnScreen("The 'D' key will move your player to the right", small_font, "RED", 380, 610)
        drawTextOnScreen("The 'S' key will move your player to the south", small_font, "RED", 620, 650)
        drawTextOnScreen("The 'W' key will move your player to the north", small_font, "RED", 850, 610)

        back_to_main_screen_button2.draw()
        drawTextOnScreen("Click to go back ", small_font, "RED", 100, 50)
        if back_to_main_screen_button2.has_been_clicked():
            start_game =0

    # input event handler
    for event in pygame.event.get():

        #quit the game
        if event.type == pygame.QUIT:
            gameActive = False

        #keyboard presses
        if event.type == pygame.KEYDOWN:
            #quits the game if escape key pressed
            if event.key == pygame.K_ESCAPE:
                gameActive=False

            #movement + action keybinds
            if event.key == pygame.K_LEFT:
                player_moving_left = True
            if event.key == pygame.K_a:
                player_moving_left = True
            if event.key ==  pygame.K_RIGHT:
                player_moving_right = True
            if event.key == pygame.K_d:
                player_moving_right = True
            if event.key ==  pygame.K_w:
                player_moving_up = True
            if event.key ==  pygame.K_UP:
                player_moving_up = True
            if event.key ==  pygame.K_DOWN:
                player_moving_down = True
            if event.key == pygame.K_s:
                player_moving_down = True

            if event.key == pygame.K_x:
                player_jumping = True

            if event.key == pygame.K_1:
               player_shooting = True
            if event.key == pygame.K_2:
                player_attack2 = True
            if event.key == pygame.K_3:
                player_attack3 = True
            if event.key == pygame.K_4:
                player_attack4 = True
            if event.key == pygame.K_c:
                player_falling = True

        #keyboard button released
        if event.type == pygame.KEYUP:

            #movement + action keybinds
            if event.key == pygame.K_LEFT:
                player_moving_left = False
            if event.key == pygame.K_a:
                player_moving_left = False
            if event.key == pygame.K_RIGHT:
                player_moving_right = False
            if event.key == pygame.K_d:
                player_moving_right = False
            if event.key == pygame.K_UP:
                player_moving_up = False
            if event.key == pygame.K_w:
                player_moving_up = False
            if event.key == pygame.K_DOWN:
                player_moving_down = False
            if event.key == pygame.K_s:
                player_moving_down = False
            if event.key == pygame.K_x:
                player_jumping = False
            if event.key == pygame.K_c:
                player_falling = False
            if event.key == pygame.K_1:
                player_shooting = False
            if event.key == pygame.K_2:
                player_attack2 = False
            if event.key == pygame.K_3:
                player_attack3 = False
            if event.key == pygame.K_4:
                player_attack4 = False

    # updates the game
    pygame.display.update()

pygame.quit()