import pygame as pg
import random as rnd

# Game settings;
Singleplayer = True  # if False: 2nd Player uses right mouse button
Player1_starts = True  # if True: Much easier on Singleplayer

# Variables for screen size:
Columns = 3
Rows = 3
Tile_size = 75
Width = Columns * Tile_size
Height = Rows * Tile_size
Screen_Size = (Width, Height)

# Other variables:
X = 0
Y = 0
Player1_Symbols_Drawn = 0
Player2_Symbols_Drawn = 0
Go = True
Game_Over = False
Screen_Filled = False

# List holding the values of the playing field:
grid = [0 for n in range(9)]
Field_List = pg.sprite.Group()
# List of grid-index-combinations that form lines of length 3:
winning_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                  (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


class Field(pg.sprite.Sprite):
    """One part of the game field with a picture
    (blank, cross or circle)
    """
    def __init__(self, x, y, pic_id):
        super().__init__()

        self.image = pg.transform.scale(
            pg.image.load(f"TTT_{pic_id}.png"), (Tile_size, Tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# start the game:
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(Screen_Size)
pg.display.set_caption("Tic Tac Toe")

while Go:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            Go = False

        if Player1_starts:
            if Player1_Symbols_Drawn <= Player2_Symbols_Drawn:
                Player1_Turn = True
            else:
                Player1_Turn = False
        else:
            if Player2_Symbols_Drawn <= Player1_Symbols_Drawn:
                Player1_Turn = False
            else:
                Player1_Turn = True

        # Draw the Background:
        while not Screen_Filled\
                and not Game_Over:
            for n in range(len(grid)):
                Field0 = Field(X, Y, 0)
                X += Tile_size
                Field_List.add(Field0)
                Field_List.draw(screen)
                if X > Width:
                    X = 0
                    Y += Tile_size
                if Y >= Height:  # end of screen reached
                    Screen_Filled = True

        # Draw Player1 symbol:
        if Player1_Turn \
                and not Game_Over \
                and event.type == pg.MOUSEBUTTONDOWN \
                and event.button == 1:  # left mouse button
            pos = pg.mouse.get_pos()
            xpart = pos[0] // Tile_size  # calc. grid_id from mouse x and y
            ypart = pos[1] // Tile_size
            index = xpart + (Columns * ypart)
            if grid[index] == 0:
                new_symbol = Field(xpart * Tile_size, ypart * Tile_size, 1)
                Field_List.add(new_symbol)
                grid[index] = 1
                Player1_Symbols_Drawn += 1
                Field_List.draw(screen)

        if not Singleplayer \
                and not Game_Over \
                and not Player1_Turn \
                and event.type == pg.MOUSEBUTTONDOWN \
                and event.button == 3:  # right mouse button
            pos = pg.mouse.get_pos()
            xpart = pos[0] / Tile_size  # calc. grid_id from mouse x and y
            ypart = pos[1] / Tile_size
            index = xpart + (Columns * ypart)
            if grid[index] == 0:
                new_symbol = Field(xpart * Tile_size, ypart * Tile_size, 2)
                Field_List.add(new_symbol)
                grid[index] = 2
                Player2_Symbols_Drawn += 1
                Field_List.draw(screen)

        # Rules for computer to place symbols:
        if Singleplayer \
                and not Game_Over \
                and not Player1_Turn:
            position_found = False
            while not position_found:
                if 2 in grid:  # i.e. 2nd turn or more

                    # Prio 1: if PC has two fields in a row, fill the row:
                    for n in range(len(winning_combos)):
                        if grid[winning_combos[n][0]] == 2\
                                and grid[winning_combos[n][1]] == 2\
                                and grid[winning_combos[n][2]] == 0\
                                and not position_found:
                            pc_index = winning_combos[n][2]
                            position_found = True
                        if grid[winning_combos[n][1]] == 2\
                                and grid[winning_combos[n][2]] == 2\
                                and grid[winning_combos[n][0]] == 0\
                                and not position_found:
                            pc_index = winning_combos[n][0]
                            position_found = True
                        if grid[winning_combos[n][0]] == 2\
                                and grid[winning_combos[n][2]] == 2\
                                and grid[winning_combos[n][1]] == 0\
                                and not position_found:
                            pc_index = winning_combos[n][1]
                            position_found = True

                    # Prio 2: Block player from filling row
                    if not position_found:
                        for n in range(len(winning_combos)):
                            if grid[winning_combos[n][0]] == 1\
                                    and grid[winning_combos[n][1]] == 1\
                                    and grid[winning_combos[n][2]] == 0\
                                    and not position_found:
                                pc_index = winning_combos[n][2]
                                position_found = True
                            if grid[winning_combos[n][1]] == 1\
                                    and grid[winning_combos[n][2]] == 1\
                                    and grid[winning_combos[n][0]] == 0\
                                    and not position_found:
                                pc_index = winning_combos[n][0]
                                position_found = True
                            if grid[winning_combos[n][0]] == 1\
                                    and grid[winning_combos[n][2]] == 1\
                                    and grid[winning_combos[n][1]] == 0\
                                    and not position_found:
                                pc_index = winning_combos[n][1]
                                position_found = True

                    # if victory not possible yet
                    # and nothing to block try to form a line of 2:
                    if not position_found:
                        for n in range(len(winning_combos)):
                            if grid[winning_combos[n][0]] == 2\
                                    and grid[winning_combos[n][1]] == 0\
                                    and grid[winning_combos[n][2]] == 0\
                                    and not position_found:
                                pc_index = winning_combos[n][1]
                                position_found = True
                            if grid[winning_combos[n][1]] == 2\
                                    and grid[winning_combos[n][0]] == 0\
                                    and grid[winning_combos[n][2]] == 0\
                                    and not position_found:
                                pc_index = winning_combos[n][0]
                                position_found = True
                            if grid[winning_combos[n][2]] == 2\
                                    and grid[winning_combos[n][0]] == 0\
                                    and grid[winning_combos[n][1]] == 0\
                                    and not position_found:
                                pc_index = winning_combos[n][1]
                                position_found = True

                    # if above conditions are False choose random field:
                    if not position_found:
                        empty_fields = []
                        for n in range(Rows * Columns):
                            if grid[n] == 0:
                                empty_fields.append(n)
                        pc_index = rnd.choice(empty_fields)
                        position_found = True

                else:  # if PC has no field yet
                    empty_fields = []
                    for n in range(Rows * Columns):
                        if grid[n] == 0:
                            empty_fields.append(n)
                    pc_index = rnd.choice(empty_fields)
                    position_found = True
            if position_found:
                grid[pc_index] = 2
                xpart = pc_index % Columns
                ypart = pc_index // Rows
                new_symbol = Field(xpart * Tile_size, ypart * Tile_size, 2)
                Field_List.add(new_symbol)
                grid[pc_index] = 2
                Player2_Symbols_Drawn += 1
                Field_List.draw(screen)
            else:
                print("No position found")  # should not happen

    if 1 in grid:
        for n in range(len(winning_combos)):
            if grid[winning_combos[n][0]] == 1\
                    and grid[winning_combos[n][1]] == 1\
                    and grid[winning_combos[n][2]] == 1:
                textsurface = pg.font.SysFont("Arial", 20).render(
                    "Player 1 wins!", False, (255, 255, 255), (0, 0, 0))
                screen.blit(textsurface, (
                    (Width // 2 - textsurface.get_width() // 2), 0))
                Game_Over = True

    if 2 in grid:
        for n in range(len(winning_combos)):
            if grid[winning_combos[n][0]] == 2\
                    and grid[winning_combos[n][1]] == 2\
                    and grid[winning_combos[n][2]] == 2:
                textsurface = pg.font.SysFont("Arial", 20).render(
                    "Player 2 wins!", False, (255, 255, 255), (0, 0, 0))
                screen.blit(textsurface, (
                    (Width // 2 - textsurface.get_width() // 2), 0))
                Game_Over = True

    if 0 not in grid\
            and not Game_Over:
        textsurface = pg.font.SysFont("Arial", 20).render(
            "Draw!", False, (255, 255, 255), (0, 0, 0))
        screen.blit(textsurface, (
            (Width // 2 - textsurface.get_width() // 2), 0))
        Game_Over = True

    pg.display.flip()
