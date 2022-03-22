import pygame
from button import Button
import csv

pygame.init()
clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
SIDE_MARGIN = 200
screen = pygame.display.set_mode((SCREEN_WIDTH-SIDE_MARGIN, SCREEN_HEIGHT))
pygame.display.set_caption('Level Editor')

#game variables
ROWS = 17
MAX_COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 16
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
current_tile = 0
level = 0

#load images
firstImg = pygame.image.load("Images/BG/en2k_9suf_181204.jpg")
firstImg = pygame.transform.scale(firstImg, (SCREEN_WIDTH, SCREEN_HEIGHT))
saveImg = pygame.image.load("Images/floppy-disk.png")
saveImg = pygame.transform.scale(saveImg, (50,50))
loadImg = pygame.image.load("Images/loading.png")
loadImg = pygame.transform.scale(loadImg, (50,50))

#loading tiles
Tiles = []
for x in range(16):
    img = pygame.image.load(f'Images/Tiles/{x}.png')
    img = pygame.transform.scale(img, (50, 50))
    Tiles.append(img)

#define background colours
Green = (144, 201, 120)
White = (255, 255, 255)
Red = (200,25,25)

#create empty tile list
# This will create a list within a list, which will all be -1 (to show that the tile is empty)
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLUMNS
    world_data.append(r)

#function for drawing BG
def draw_BG():
    screen.fill(Green)
    width = firstImg.get_width()
    for x in range(3):
         screen.blit(firstImg, ((x * width)-scroll*0.8, 0))

def draw_grid():
    #vertical lines
    for i in range(MAX_COLUMNS+1):
        pygame.draw.line(screen, White, (i * TILE_SIZE-scroll, 0), (i * TILE_SIZE-scroll, SCREEN_HEIGHT))
    #horizontal lines
    for i in range (ROWS+1):
        pygame.draw.line(screen, White, (0,i * TILE_SIZE),(SCREEN_WIDTH,i * TILE_SIZE))

#function for drawing world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >=0:
                screen.blit(Tiles[tile], ((x * TILE_SIZE-scroll, y* TILE_SIZE)))

def draw_label_coords(labelName, xcoord, ycoord):
    font = pygame.font.Font('freesansbold.ttf', 16)
    labelName = font.render(labelName, True, (90, 74, 74))
    screen.blit(labelName, (xcoord, ycoord))

#save and load buttons
saveButton = Button(50,625,saveImg, screen)
loadButton = Button(125,625, loadImg, screen)

#list of buttons
listOfButtons = []
buttonColumn = 0
buttonRow = 0

for j in range(len(Tiles)):
    TileButton = Button(50+(75*buttonColumn),25 + (buttonRow * 75),Tiles[j], screen)
    listOfButtons.append(TileButton)
    buttonColumn+=1
    if buttonColumn == 2:
        buttonRow +=1
        buttonColumn =0

windowActive = True
while(windowActive):
    clock.tick(FPS)
    #draws the background images onto screen
    draw_BG()
    draw_grid()
    draw_world()

    #draw panel rectangle
    pygame.draw.rect(screen, Green, (0, 0, 200, SCREEN_HEIGHT))

    #drawing save and load buttons
    saveButton.draw()
    saveButton.draw_label_coords("Save", 55,680)
    if saveButton.has_been_clicked():
        with open(f'Levels/level{level}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile,delimiter=',')
            for row in world_data:
                writer.writerow(row)
        print("Saved!")


    loadButton.draw()
    loadButton.draw_label_coords("Load", 130, 680)
    if loadButton.has_been_clicked():
      scroll = 0
      with open(f'Levels/level{level}.csv', newline='') as csvfile:
          reader = csv.reader(csvfile, delimiter=',')
          for x,row in enumerate(reader):
              for y,tile in enumerate(row):
                  world_data[x][y] = int(tile)
      print(world_data)
      print("Level loaded")


    #drawing level label
    draw_label_coords("Level: "+ str(level), 50, 725)
    draw_label_coords("Up / down changes level", 5, 760)

    #user clicking and choosing a tile
    button_number = 0
    for button_number, i in enumerate(listOfButtons):
        i.draw()
        if i.has_been_clicked():
            current_tile = button_number
            #visual identifier for the tile that has been chosen
    pygame.draw.rect(screen, "RED", listOfButtons[current_tile].rect,3)

    #scroll the map
    if scroll_left == True and scroll > 0:
        scroll -=5 * scroll_speed
    if scroll_right == True and scroll < SCREEN_WIDTH:
        scroll +=5 * scroll_speed

    #add new tiles to screen and get the x+y for mouse co-ordinates
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    #check that the coordinates are within the game area, not the area which is not part of game loop
    if pos[0] >200 and pos[1] > 0:

        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile

        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        # quit the level editor
        if event.type == pygame.QUIT:
            windowActive = False

        # keyboard presses
        if event.type == pygame.KEYDOWN:
               # quits the game if escape key pressed
               if event.key == pygame.K_UP:
                   level += 1
               if event.key == pygame.K_ESCAPE:
                    windowActive = False
               if event.key == pygame.K_LEFT:
                    scroll_left = True
               if event.key == pygame.K_RIGHT:
                   scroll_right = True
               if event.key == pygame.K_F1:
                   scroll_speed = 5
               if event.key == pygame.K_DOWN:
                   if level >0:
                       level -=1


        # keyboard button released
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    scroll_left = False
                if event.key == pygame.K_RIGHT:
                    scroll_right = False
                if event.key == pygame.K_F1:
                    scroll_speed = 1



    pygame.display.update()

pygame.quit()