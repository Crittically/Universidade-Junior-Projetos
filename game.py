import pygame
from random import randint
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

def load_safe_surface():
    surface = pygame.Surface((hole_width, hole_width))  #the size of safe zone surface
    surface.set_alpha(128)                              # alpha (transparency) level
    surface.fill((171, 84, 209))                        #fills the entire surface with an RGB color
    return surface

height = screen.get_height()
width = screen.get_width()
player_pos = pygame.Vector2(width / 2, height / 2)
player_vel = pygame.Vector2(0, 0)
horizontal_hole_pos = pygame.Vector2(-65, 0) #left corner of the horizontal incoming hole, this is also the x position of the wall
vertical_hole_pos = pygame.Vector2(0, height + 65) #left corner of the vertical incoming hole, """
floor = height - 40
jumped = False
gameover = False
game_font = pygame.font.SysFont("Arial", 36)
insane_font = pygame.font.SysFont("Arial", 36, True)
score = -1
score_surface = game_font.render("Score: 0", True, "black")
difficulty = -1
modifiers = [(350, 720, 300, 5, 0.8), (550, 1400, 230, 4, 0.5), (550, 1400, 200, 3.2, 0.5), (550, 1700, 170, 2.2, 0.2)] #jump velocity, gravity, hole width, wall time for a full scroll and seconds before scroll, respectively
konami = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a]
konami_index = 0
bonus_speed_mult = 1
flappy = pygame.image.load("flappy.png").convert_alpha()
flappy_half_width = flappy.get_width() // 2
flappy_half_height = flappy.get_height() // 2
background_surface = pygame.image.load("background.png").convert()
background = pygame.transform.smoothscale_by(background_surface, height / background_surface.get_height())
pipe_surface = pygame.image.load("pipe.png").convert_alpha()
pipe = pygame.transform.smoothscale_by(pipe_surface, 62 / pipe_surface.get_width())
pipe_height = pipe.get_height()
pipe_width = pipe.get_width()
pipe_down = pygame.transform.rotate(pipe, 180)
pipe_left = pygame.transform.rotate(pipe, 90)
pipe_right = pygame.transform.rotate(pipe, 270)


while running:   
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

    if difficulty == -1:
        screen.fill("black")
        surface_list = ["Choose a difficulty:", "Easy", "Medium", "Hard"]
        surface_list = [game_font.render(text, True, "white") for text in surface_list]
        y_mult_list = [0.2, 0.37, 0.57, 0.77]
        rect_list = []
        for surface, y_mult in zip(surface_list, y_mult_list):
            screen.blit(surface, ((screen.get_width() - surface.get_width()) // 2, screen.get_height() * y_mult - surface.get_height() // 2))
            if  surface != surface_list[0]:
                rect_list.append(pygame.Rect((screen.get_width() - surface.get_width()) // 2, screen.get_height() * y_mult - surface.get_height() // 2, surface.get_width(), surface.get_height()))
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP:
                for rect in rect_list:
                    if rect.collidepoint(event.pos):
                        difficulty = rect_list.index(rect)
                        jump_vel, gravity, hole_width, walltime, safe_seconds = modifiers[difficulty]
                        safe_surface = load_safe_surface()
                        break
                if konami_index == 10:
                    if insane_rect.collidepoint(event.pos):
                        difficulty = 3
                        jump_vel, gravity, hole_width, walltime, safe_seconds = modifiers[difficulty]
                        bonus_speed_mult = 1.2
                        safe_surface = load_safe_surface()
            elif event.type == pygame.KEYUP:
                if konami_index <= 9 and event.key == konami[konami_index]:
                    konami_index += 1
                else:
                    konami_index = 0
        if konami_index == 10:
            insane_surface = game_font.render("INSANE", True, "red")
            screen.blit(insane_surface, ((screen.get_width() - insane_surface.get_width()) // 2, screen.get_height() * 0.9 - insane_surface.get_height() // 2))
            insane_rect = pygame.Rect((screen.get_width() - insane_surface.get_width()) // 2, screen.get_height() * 0.9 - insane_surface.get_height() // 2, insane_surface.get_width(), insane_surface.get_height())


    elif not gameover:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_pos.x -= 400 * dt * bonus_speed_mult
        if keys[pygame.K_d]:
            player_pos.x += 400 * dt * bonus_speed_mult
        if keys[pygame.K_SPACE]:
            if not jumped: #if you hadnt jumped before
                player_vel.y = -jump_vel
                jumped = True #disable jump
        else: #reenable jump when space is released
            jumped = False

        player_vel.y += gravity * dt #accellerates the player down a constant amount
        player_pos += player_vel * dt #add current velocities as movement
        player_hitpixels = [(player_pos.x-40, player_pos.y), (player_pos.x-28, player_pos.y-28), (player_pos.x, player_pos.y-40), (player_pos.x+28, player_pos.y-28), (player_pos.x+40, player_pos.y), (player_pos.x+28, player_pos.y+28), (player_pos.x, player_pos.y-40), (player_pos.x-28, player_pos.y+28)]


        if horizontal_hole_pos.x <= -100 and vertical_hole_pos.y >= height + 100:
            horizontal_hole_pos.y = randint(200, height)
            horizontal_hole_pos.x = width + safe_seconds * width / walltime
            vertical_hole_pos.x = randint(0, width - 200)
            vertical_hole_pos.y = -safe_seconds * height / walltime
            score += 1
            score_surface = game_font.render("Score: %d" % score, True, "black")
        screen.blit(score_surface, (score_surface.get_width() * 0.2, score_surface.get_height() // 2 ))
        if dt != 0:
            horizontal_hole_pos.x -= width * dt / walltime
            vertical_hole_pos.y += height * dt / walltime

        #draw background
        screen.blit(background, (0, 0))
        #simpole method to simulate blinking by checking wall position
        if horizontal_hole_pos.x > width and (horizontal_hole_pos.x - width) // (width / walltime / 10) % 2 == 0: #safe_seconds * width / walltime :
            #draw safe zone
            screen.blit(safe_surface, (vertical_hole_pos.x, horizontal_hole_pos.y - hole_width))
        #draw horizontal walls
        screen.blit(pipe, (horizontal_hole_pos.x, horizontal_hole_pos.y))
        screen.blit(pipe_down, (horizontal_hole_pos.x, horizontal_hole_pos.y - hole_width - pipe_height))
        #draw vetical walls
        screen.blit(pipe_right, (vertical_hole_pos.x-pipe_height, vertical_hole_pos.y - 60))
        screen.blit(pipe_left, (vertical_hole_pos.x + hole_width, vertical_hole_pos.y - 60))
        #draw player
        screen.blit(flappy, (player_pos.x - flappy_half_width, player_pos.y - flappy_half_height))

        #gameover when hitting the ground
        if player_pos.y >= floor:
            gameover = True
        #iterate every hitpixel
        for x, y in player_hitpixels:
            #gameover when colliding with horizontal walls
            if (x >= horizontal_hole_pos.x and x <= horizontal_hole_pos.x + 60) and (y >= horizontal_hole_pos.y or y <= horizontal_hole_pos.y - hole_width):
                gameover = True
                break
            #gameover when colliding with vertical walls
            if (y <= vertical_hole_pos.y and y >= vertical_hole_pos.y - 60) and (x <= vertical_hole_pos.x or x >= vertical_hole_pos.x + hole_width):
                gameover = True
                break
        

    else:
        screen.fill("black")
        gameover_surface = game_font.render("GAME OVER!", True, "white")
        score_surface = game_font.render("Score: %d" % score, True, "white")
        screen.blit(gameover_surface, ((screen.get_width() - gameover_surface.get_width()) // 2, (screen.get_height() - gameover_surface.get_height()) // 2 - score_surface.get_height() // 2))
        screen.blit(score_surface, ((screen.get_width() - score_surface.get_width()) // 2, (screen.get_height() - score_surface.get_height()) // 2 + gameover_surface.get_height() // 2))
     
     # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000



pygame.quit()