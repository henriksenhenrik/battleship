import pygame
import random

pygame.init()
WINDOW_HEIGHT = 510
WINDOW_WIDTH = 510
game_window = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
pygame.display.set_caption("Battleship")
# set the background color
hav_color = (43, 101, 236)
grid_color_skip = (67, 70, 75)
margin_color = (70, 130, 255)
skutt_color = (255, 0, 0)
grid = []
grid_bredde = 40
grid_hoyde = 40
margin = 10
antall_skip = 0
antall_skutt = 0

class Grid:
    def __init__(self):
        self.grid = grid
        self.grid_width = 40
        self.grid_height = 40
        self.margin = 10
        self.ship_count = 0
        self.hit_count = 0
        self.all_ships_set = False
        self.ships_sunk = 0


        for rad in range(10):
            self.grid.append([])
            for kolonne in range(10):
                self.grid[rad].append(0)

    def place_ship(self, rad, kolonne):
        if self.grid[rad][kolonne] == 0 and self.ship_count < 10:
            self.grid[rad][kolonne] = 1
            self.ship_count += 1
            if self.ship_count == 10:
                self.all_ships_set = True
            return True
        return False

    def shoot(self, rad, kolonne):
        if self.grid[rad][kolonne] == 1:
            self.grid[rad][kolonne] = 2
            self.hit_count += 1
            self.ships_sunk += 1
            return "Treff"
        elif self.grid[rad][kolonne] == 2:
            return "Allerede truffet"
        else:
            self.grid[rad][kolonne] = 2
            self.hit_count += 1
            return "Bommet"

    def auto_shoot(self):
        while self.ships_sunk < 10:
            rad = random.randint(0, 9)
            kolonne = random.randint(0, 9)
            result = self.shoot(rad, kolonne)
            print(f'{result} at {rad},{kolonne}')

    def display_hit_count(self, window):
        font = pygame.font.Font(None, 30)
        text = font.render(f'Maskinen brukte {self.hit_count} forsøk på å ta alle skipene!', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)  # center the text box
        window.blit(text, text_rect)

    def draw(self, window):
        for rad in range(10):
            for kolonne in range(10):
                color = hav_color
                if self.grid[rad][kolonne] == 1:
                    color = grid_color_skip
                elif self.grid[rad][kolonne] == 2:
                    color = skutt_color
                pygame.draw.rect(window, color,
                                 [(self.margin + self.grid_width) * kolonne + self.margin,
                                  (self.margin + self.grid_height) * rad + self.margin,
                                  self.grid_width, self.grid_height])


def lag_grid():
    for rad in range(10):
        grid.append([])
        for kolonne in range(10):
            grid[rad].append(0)


game_grid = Grid()
all_ships_shot = False

# create a game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.QUIT()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            posisjon = pygame.mouse.get_pos()
            kolonne = posisjon[0] // (grid_bredde + margin)
            rad = posisjon[1] // ((grid_hoyde + margin))
            if game_grid.place_ship(rad,kolonne):
                if game_grid.all_ships_set:
                    game_grid.auto_shoot()
                    all_ships_shot = True

    game_window.fill(margin_color)
    game_grid.draw(game_window)
    
    if all_ships_shot:
        game_grid.display_hit_count(game_window)

    
    pygame.display.update()
    pygame.display.flip()

pygame.QUIT()

