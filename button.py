import pygame
import math

class Button:

    def __init__(self, xcoordinate, ycoordinate, imageToLoad, screen):
        self.x_coordinate = xcoordinate
        self.y_coordinate = ycoordinate
        self.img = imageToLoad
        self.windowscreen = screen
        self.clicked = False
        self.rect = self.img.get_rect()
        self.rect.x = xcoordinate
        self.rect.y = ycoordinate

    def draw_image(self, labelName):
        self.windowscreen.blit(self.img, (self.x_coordinate, self.y_coordinate))
        self.draw_label(labelName)

    def draw_label(self, labelName):
        font = pygame.font.Font('freesansbold.ttf', 32)
        labelName = font.render(labelName, True, (90,74,74))
        self.windowscreen.blit(labelName, (self.x_coordinate-250, self.y_coordinate+50))

    def draw_label_coords(self, labelName, xcoord, ycoord):
        font = pygame.font.Font('freesansbold.ttf', 16)
        labelName = font.render(labelName, True, (90, 74, 74))
        self.windowscreen.blit(labelName, (xcoord, ycoord))

    def draw(self):
        self.windowscreen.blit(self.img,(self.x_coordinate, self.y_coordinate))

    def has_been_clicked(self):
        #Check if mouse is hovering over and user is clicking
        self.clicked = False
        mouse_pos = pygame.mouse.get_pos()
        distance = math.sqrt((((mouse_pos[0] - self.x_coordinate) ** 2)) + ((mouse_pos[1] - self.y_coordinate) ** 2))
        if distance <= 45:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                return True








