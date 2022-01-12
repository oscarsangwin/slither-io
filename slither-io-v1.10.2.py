import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame as pg
import math
import time
import threading
import random

WIDTH = 850
HEIGHT = 550

WHITE  =  (255, 255, 255)
GREY   =  (150, 150, 150)
BLACK  =  (0,   0,   0  )

RED    =  (255, 0,   0  )
GREEN  =  (0,   255, 0  )
BLUE   =  (0,   0,   255)

YELLOW =  (255, 255, 0  )
MAGENTA = (255, 0  , 255)
CYAN =    (0  , 255, 255)

BACKGROUND_SHADE = (22, 33, 34)

def update_screen():
    screen.fill(WHITE)

    if in_game:
        mygame.render()
    else:
        menu.render()

    # Draw custom cursor
    if pg.mouse.get_focused():
        pg.mouse.set_visible(False)
        screen.blit(cursor_img, pg.mouse.get_pos())

    pg.display.update()

def draw_text(text, x, y, col=BLACK, pos='center'):
    if not fonts_loaded:
        set_window_title('(loading fonts...)')
        return
    else:
        set_window_title()

    textsurface = myfont.render(text, True, col)
    if pos == 'center':
        text_center = textsurface.get_rect(center=(x, y))
    elif pos == 'left':
        text_center = textsurface.get_rect(center=(x, y))
        text_center.left = x
    elif pos == 'right':
        text_center = textsurface.get_rect(center=(x, y))
        text_center.right = x
    screen.blit(textsurface, text_center)

def set_window_title(txt=''):
    if txt:
        pg.display.set_caption(f'Slither.io v1.10.2 - {txt}')
    else:
        pg.display.set_caption('Slither.io v1.10.2')

class SlitherGame:
    def __init__(self):
        self.space = False

        self.slider_pos = WIDTH
        self.in_transition = False

        self.map_x = 0
        self.map_y = 0

        self.map_angle = 0
        self.angle_turn_speed = 5

        self.map_zoom = 150
        self.new_map_zoom = 100

        self.map_width = 2000
        self.map_height = 2000

        self.player_speed = 5
        self.player_speed_boost = 8
        self.player_length = 15
        self.player_head_rad = 35

        self.player_base_col = GREY

        self.collision = False

        self.end_game_countdown = None

        self.eye_radius = 13
        self.eye_angle_split = 38
        self.eye_distance = 20

        self.background_image = pg.image.load('./Images/background.jpeg')
        self.border_thickness = 15

        self.max_agar = 200
        self.agar = []
        self.agar_rad = 20

        for _ in range(self.max_agar-1):
            self.gen_new_agar()

        # First node of trail is the head
        self.trail = []

        # Space between each node in the trail (Horizontal)
        self.trail_space = 20

        # Add the first node of the snake trail
        self.trail.insert(0, (-self.map_x, -self.map_y))

    def gen_new_agar(self, from_small=False, x=None, y=None):
        if not x and not y:    
            x = int(random.randint(0, self.map_width - self.agar_rad * 2) - self.map_width / 2 + int(self.agar_rad))
            y = int(random.randint(0, self.map_height - self.agar_rad * 2) - self.map_height / 2 + int(self.agar_rad))
        col = random.choice((RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA))
        col = tuple(map(lambda x : max(x - 100, 0), col))
        offset = random.randint(0, 10)
        if from_small:
            size = 2
        else:
            size = self.agar_rad
        self.agar.append((x, y, col, offset, size))
    
    def update_trail(self):
        # Take note of the very last node in the trail
        end_node = self.trail[-1]

        # New trail which will update the current trail
        new_trail = []

        # Know if we are dealing with the head node
        head_node = True

        # Iterate through the trail nodes, starting from the head (the first node)
        for current_node in self.trail:
            if head_node:
                # Head node must be set to the new map position (list is so that it is editable later)
                new_node = [-self.map_x, -self.map_y]
                head_node = False
            else:
                # If not the head node...
                # (new_node will already be set ... the last inserted node)
                
                # What you add to the current node to get to the new node
                diff_x = new_node[0] - current_node[0]
                diff_y = new_node[1] - current_node[1]

                # Horizontal distance between two nodes
                diff = math.sqrt(diff_x**2 + diff_y**2)

                # Scale factor to know how much smaller the difference should be
                sf = self.trail_space / diff

                if diff < self.trail_space:
                    # Do not move snake if the distance between the two nodes is smaller than the spacing required
                    new_node = list(current_node)
                else:
                    # Now, the new node to set is the old position minus the difference multiplied by the scale factor
                    new_node[0] = new_node[0] - (diff_x * sf)
                    new_node[1] = new_node[1] - (diff_y * sf)
                    
            # Append the new position, as a tuple
            new_trail.append(tuple(new_node))

        # Update the old trail
        self.trail = new_trail.copy()

        # Add back the very last node to increase the snake trail length if it is smaller than the player length score
        if len(self.trail) < self.player_length:
            # Check the last node is not too close
            diff_x = abs(end_node[0] - self.trail[-1][0])
            diff_y = abs(end_node[1] - self.trail[-1][1])
            diff = math.sqrt(diff_x**2 + diff_y**2)
            if diff > 2:
                self.trail.append(end_node)

    def rotate_snake(self, speed):
        # Move map according to mouse position
        mouse = pg.mouse.get_pos()
        diff_x = mouse[0] - int(WIDTH / 2)
        diff_y = mouse[1] - int(HEIGHT / 2)

        # Calculate the angle that the mouse is facing
        mouse_angle = math.degrees(math.atan2(diff_x, diff_y))
        mouse_angle = 360 - (mouse_angle + 180)

        if mouse_angle != self.map_angle:
            if mouse_angle > self.map_angle:
                # Mouse angle bigger (further around compass)
                clockwise = mouse_angle - self.map_angle
                anti_clockwise = self.map_angle + (360 - mouse_angle)
            elif mouse_angle < self.map_angle:
                # Mouse angle smaller (behind on compass)
                clockwise = mouse_angle + (360 - self.map_angle)
                anti_clockwise = self.map_angle - mouse_angle
        
            if clockwise <= anti_clockwise:
                # Turn clockwise
                if clockwise <= self.angle_turn_speed:
                    self.map_angle = mouse_angle
                else:
                    self.map_angle = (self.map_angle + self.angle_turn_speed) % 360
            else:
                # Turn anti-clockwise
                if anti_clockwise <= self.angle_turn_speed:
                    self.map_angle = mouse_angle
                else:
                    self.map_angle -= self.angle_turn_speed
                    if self.map_angle < 0:
                        self.map_angle += 360

        move_x = math.sin(math.radians(self.map_angle)) * speed
        move_y = math.cos(math.radians(self.map_angle)) * speed

        # Change x and y by the differences
        self.map_x -= move_x
        self.map_y += move_y
        
    def update_agar(self):
        # Check if any agar eaten and draw in nearby agar
        new_agar = []

        for agar in self.agar:
            agar_x_diff = -self.map_x - agar[0]
            agar_y_diff = -self.map_y - agar[1]
            dist = math.sqrt(agar_x_diff**2 + agar_y_diff**2)

            if dist <= self.player_head_rad: # Checks for overlap, as opposed to complete intersection
                self.player_length += 1
            elif dist <= 50:
                agar = list(agar)
                agar[0] += agar_x_diff / 5
                agar[1] += agar_y_diff / 5
                new_agar.append(tuple(agar))
            else:
                agar = list(agar)
                agar[4] = min(agar[4] + 2, self.agar_rad)
                new_agar.append(agar)
        self.agar = new_agar.copy()

        # Add back any taken agar
        for _ in range(self.max_agar - len(self.agar)):
            self.gen_new_agar(from_small=True)

    def update(self, space=False):
        if int(self.slider_pos) != 0 and not self.in_transition:
            self.slider_pos = int(self.slider_pos / 1.12)

        if not self.collision:
            # Space bar set to class attribute
            self.space = space
            if self.space:
                speed = self.player_speed_boost
            else:
                speed = self.player_speed

            if not int(self.slider_pos):
                self.update_trail()
                self.rotate_snake(speed)

            # Set scale depending on snake length
            if self.player_length < 50:
                self.new_map_zoom = 100
            elif self.player_length < 100:
                self.new_map_zoom = 80
            elif self.player_length < 200:
                self.new_map_zoom = 60
            else:
                self.new_map_zoom = 40

            # Smooth zoom
            self.map_zoom -= (self.map_zoom-self.new_map_zoom) / 10

            self.check_collision()

        else:
            # If the snake is collided
            if self.trail:
                # Fade out snake, replacing with agar
                for _ in range(int(self.player_length / 10)):
                    try:
                        x, y = self.trail[0]
                        self.trail.pop(0)
                        if random.randint(0, 2) == 0:
                            self.gen_new_agar(from_small=True, x=x, y=y)
                    except IndexError:
                        self.trail = []

            elif not self.end_game_countdown:
                # If timer has not been started, start it
                # (Timer gives a few seconds before returning to the main menu screen)
                self.end_game_countdown = time.time()

            else:
                # Check if number of seconds has passed since the timer was set
                if time.time() - self.end_game_countdown > 0.7:
                    self.in_transition = True

                    if int(self.slider_pos) + 1 >= WIDTH:
                        global in_game
                        in_game = False
                        menu.reset()

                        global high_score, last_score
                        last_score = self.player_length
                        if last_score > high_score:
                            high_score = last_score
                            with open('./Highscore/score.txt', 'w') as f:
                                f.write(str(high_score))

                    else:
                        self.slider_pos = self.slider_pos + ((WIDTH - self.slider_pos) / 3)

        self.update_agar()

    def check_collision(self):
        # --- Check for overlap of it's own trail ---
        x, y = self.trail[0]
        
        # Work out how many nodes away from the snake head to start checking
        # If the trail space is small and the head size large, then it means false collisions would be avoided
        # int() + 1 rounds the number always UP
        first_node_index = int(self.player_head_rad / self.trail_space) + 1

        # Add one to the index to skip the first head node too
        first_node_index += 1

        self.collision = False

        for node in self.trail[first_node_index:]:
            dist_x = node[0] - x
            dist_y = node[1] - y
            dist = abs(math.sqrt(dist_x**2 + dist_y**2))

            if dist < self.player_head_rad:
                self.collision = True
                return

        # --- Check world overlap ---
        if x + self.border_thickness > self.map_width / 2 or x - self.border_thickness < -self.map_width / 2:
            # X axis check
            self.collision = True
            return
        elif y + self.border_thickness > self.map_height / 2 or y - self.border_thickness < -self.map_height / 2:
            # Y axis check
            self.collision = True
            return

    def draw_eyes(self):
        # White part of eyes
        head_x, head_y = WIDTH / 2, HEIGHT / 2
        left_eye_pos_x = int(-math.sin(math.radians(self.map_angle + 180 - self.eye_angle_split)) * self.eye_distance * (self.map_zoom / 100) + head_x)
        left_eye_pos_y = int(math.cos(math.radians(self.map_angle + 180 - self.eye_angle_split)) * self.eye_distance * (self.map_zoom / 100) + head_y)
        right_eye_pos_x = int(-math.sin(math.radians(self.map_angle + 180 + self.eye_angle_split)) * self.eye_distance * (self.map_zoom / 100) + head_x)
        right_eye_pos_y = int(math.cos(math.radians(self.map_angle + 180 + self.eye_angle_split)) * self.eye_distance * (self.map_zoom / 100) + head_y)

        pg.draw.circle(screen, WHITE, (left_eye_pos_x, left_eye_pos_y), int(self.eye_radius * (self.map_zoom / 100)))
        pg.draw.circle(screen, WHITE, (right_eye_pos_x, right_eye_pos_y), int(self.eye_radius * (self.map_zoom / 100)))

        # --- Repeat, but for the pupils ---
        mouse = pg.mouse.get_pos()

        # Left eye - get mouse angle from the old left eye center
        diff_x = mouse[0] - left_eye_pos_x
        diff_y = mouse[1] - left_eye_pos_y
        mouse_angle = math.degrees(math.atan2(diff_x, diff_y))
        mouse_angle = 360 - (mouse_angle + 180)

        # Work out position of left eye
        left_eye_pos_x = int(-math.sin(math.radians(mouse_angle + 180)) * (self.eye_distance/4) * (self.map_zoom / 100) + left_eye_pos_x)
        left_eye_pos_y = int(math.cos(math.radians(mouse_angle + 180)) * (self.eye_distance/4) * (self.map_zoom / 100) + left_eye_pos_y)

        # Right eye - get mouse angle from the old right eye center
        diff_x = mouse[0] - right_eye_pos_x
        diff_y = mouse[1] - right_eye_pos_y
        mouse_angle = math.degrees(math.atan2(diff_x, diff_y))
        mouse_angle = 360 - (mouse_angle + 180)

        # Work out position of right eye
        right_eye_pos_x = int(-math.sin(math.radians(mouse_angle + 180)) * (self.eye_distance/4) * (self.map_zoom / 100) + right_eye_pos_x)
        right_eye_pos_y = int(math.cos(math.radians(mouse_angle + 180)) * (self.eye_distance/4) * (self.map_zoom / 100) + right_eye_pos_y)

        # Draw both pupils of each eye
        pg.draw.circle(screen, BLACK, (left_eye_pos_x, left_eye_pos_y), int((self.eye_radius/1.5) * (self.map_zoom / 100)))
        pg.draw.circle(screen, BLACK, (right_eye_pos_x, right_eye_pos_y), int((self.eye_radius/1.5) * (self.map_zoom / 100)))

    def render(self):
        self.draw_background()
        self.draw_borders()

        # Test agar circles
        for agar in self.agar:
            val = int(math.sin(time.time() * 3 + agar[3]) * 35)
            col = tuple(map(lambda x : max(min(x + val, 255), 0), agar[2]))
            self.draw_circle_at(agar[0], agar[1], agar[4], col=col)

        # Draw snake and eyes
        if self.collision:
            col = RED
        else:
            col = self.player_base_col
        self.draw_snake(base_col=col)

        if not self.collision:
            self.draw_eyes()

        # Info bar at top:
        #   Coordinates:

        #   FPS:
        pg.draw.rect(screen, WHITE, (0, 0, 120, 30))
        fps = int(int(clock.get_fps()) / 2 + 1) * 2
        draw_text(f'FPS: {str(fps)}', 10, 15, pos='left')

        #   Length:
        pg.draw.rect(screen, WHITE, (WIDTH - 185, 0, 185, 30))
        draw_text('Length:', WIDTH - 175, 15, pos='left')
        draw_text(str(self.player_length), WIDTH - 10, 15, pos='right')

        if self.slider_pos:
            pg.draw.rect(screen, BACKGROUND_SHADE, (0, 0, int(self.slider_pos) + 1, HEIGHT))

    def draw_snake(self, base_col=GREEN):
        node_count = 0
        to_plot = self.trail

        for snake_node in to_plot[::-1]:

            node_count += 1
            col = tuple(map(lambda x : max(min(int(x + math.sin((len(self.trail) - node_count) / 8) * 60) + self.space * 30, 255), 0), base_col))

            self.draw_circle_at(*snake_node, self.player_head_rad, col=col)

    def draw_circle_at(self, pos_x, pos_y, radius, col=RED):
        # Input position of the circle on map and radius at 100% scale
        # The function will plot the circle at the right relative positon with the right scale

        # Calculation explanation: (Half the width plus the circle distance from the center all 
        # multiplied by the zoom factor as a decimal and then shifted according to the map position)
        rel_x = int(WIDTH / 2 + (pos_x - WIDTH/2) * (self.map_zoom / 100) + self.map_x * (self.map_zoom / 100)) + int(WIDTH/2) * self.map_zoom/100
        rel_y = int(HEIGHT / 2 + (pos_y - HEIGHT/2) * (self.map_zoom / 100) + self.map_y * (self.map_zoom / 100)) + int(HEIGHT/2) * self.map_zoom/100
        rad = int(radius * self.map_zoom / 100)

        rel_x = int(rel_x)
        rel_y = int(rel_y)

        # Only render if actually on the screen
        if rel_x + rad > 0 and rel_x - rad < WIDTH and rel_y + rad > 0 and rel_y - rad < HEIGHT:
            pg.draw.circle(screen, col, (int(rel_x), int(rel_y)), rad)
    
    def get_rel_coords(self, x, y):
        rel_x = int(WIDTH / 2 + (x - WIDTH/2) * (self.map_zoom / 100) + self.map_x * (self.map_zoom / 100)) + int(WIDTH/2) * self.map_zoom/100
        rel_y = int(HEIGHT / 2 + (y - HEIGHT/2) * (self.map_zoom / 100) + self.map_y * (self.map_zoom / 100)) + int(HEIGHT/2) * self.map_zoom/100
        return rel_x, rel_y

    def draw_borders(self):
        # --- Thin red border ---
        # Left border
        pos_x, pos_y = self.get_rel_coords(int(-self.map_width/2), int(-self.map_height/2))
        pg.draw.rect(screen, RED, (int(pos_x), 0, -self.border_thickness, HEIGHT))

        # Right border
        pos_x, pos_y = self.get_rel_coords(int(self.map_width/2), int(self.map_height/2))
        pg.draw.rect(screen, RED, (int(pos_x), 0, self.border_thickness, HEIGHT))

        # Top border
        pos_x, pos_y = self.get_rel_coords(int(-self.map_width/2), int(-self.map_height/2))
        pg.draw.rect(screen, RED, (0, int(pos_y), WIDTH, -self.border_thickness))

        # Bottom border
        pos_x, pos_y = self.get_rel_coords(int(self.map_width/2), int(self.map_height/2))
        pg.draw.rect(screen, RED, (0, int(pos_y), WIDTH, self.border_thickness))

        # --- Outer maroon border ---
        maroon = tuple(map(lambda x : max(0, x - 170), RED))

        # Left border
        pos_x, pos_y = self.get_rel_coords(int(-self.map_width/2), int(-self.map_height/2))
        length = int(-pos_x-WIDTH)
        if length < 0:
            pg.draw.rect(screen, maroon, (int(pos_x)-self.border_thickness, 0, length, HEIGHT))

        # Right border
        pos_x, pos_y = self.get_rel_coords(int(self.map_width/2), int(self.map_height/2))
        length = int(WIDTH-pos_x) + 1
        if length > 0:
            pg.draw.rect(screen, maroon, (int(pos_x)+self.border_thickness, 0, length, HEIGHT))

        # Top border
        pos_x, pos_y = self.get_rel_coords(int(-self.map_width/2), int(-self.map_height/2))
        length = int(-pos_y-HEIGHT)
        if length < 0:
            pg.draw.rect(screen, maroon, (0, int(pos_y)-self.border_thickness, WIDTH, length))

        # Bottom border
        pos_x, pos_y = self.get_rel_coords(int(self.map_width/2), int(self.map_height/2))
        length = int(HEIGHT-pos_y) + 1
        if length > 0:
            pg.draw.rect(screen, maroon, (0, int(pos_y)+self.border_thickness, WIDTH, length))

    def draw_background(self):
        # Scale the image down to the correct size according to the map zoom
        old_width, old_height = self.background_image.get_size()
        new_width = int(old_width*(self.map_zoom/100))
        new_height = int(old_height*(self.map_zoom/100))
        self.blit_image = pg.transform.scale(self.background_image, (new_width, new_height))

        # Calculate how many images to blit in each directon
        img_width, img_height = self.blit_image.get_size()
        img_x_amt = int(WIDTH / img_width) + 3
        img_y_amt = int(HEIGHT / img_height) + 3

        for y in range(img_y_amt):
            for x in range(img_x_amt):
                # Image position is offset to make a grid
                pos_x = x * img_width
                pos_y = y * img_height

                # Image coords are shifted so that their zoom center matches with the center of the screen
                pos_x += WIDTH / 2
                pos_y += HEIGHT / 2

                # Image coords are changed according to the map position (and modulo to fit on screen)
                pos_x += self.map_x * (self.map_zoom / 100) % img_width
                pos_y += self.map_y * (self.map_zoom / 100) % img_height

                # Image coords are moved back by half the screen
                pos_x -= img_width * (int(img_y_amt / 2) + 1)
                pos_y -= img_height * (int(img_y_amt / 2) + 1)

                # Image is displayed on screen
                screen.blit(self.blit_image, (int(pos_x), int(pos_y)))

class SlitherMenu:
    def __init__(self):
        self.music_started = False

        # Load images:
        self.load_image = pg.image.load('./Images/loading.png')
        self.load_image_size = self.load_image.get_rect()[2:4]

        self.background = pg.image.load('./Images/background.jpeg')
        self.background_size = self.background.get_rect()[2:4]

        self.slither_img = pg.image.load('./Images/slither-text.png')
        self.slither_size = self.slither_img.get_rect()[2:4]

        self.play_button = pg.image.load('./Images/play-button.png')
        self.play_button_size = self.play_button.get_rect()[2:4]
        self.play_button_hover = False
        self.hover_increase = 0

        self.nevwin_img = pg.image.load('./Images/nevwin-game.png')
        self.nevwin_img_size = self.nevwin_img.get_rect()[2:4]

        self.by_name_img = pg.image.load('./Images/by-name.png')
        self.by_name_img_size = self.by_name_img.get_rect()[2:4]

        self.slider_pos = 0
        self.in_transition = False

    def reset(self):
        self.in_transition = False

    def update(self):
        if fonts_loaded:
            # --- Main menu ---

            if not self.music_started:
                pg.mixer.music.play(-1)
                self.music_started = True

            # Get mouse position
            mouse_x, mouse_y = pg.mouse.get_pos()

            # WIDTH/2, HEIGHT/4*2.7
            if mouse_x > int(WIDTH/2-80) and mouse_x < int(WIDTH/2+80) and mouse_y > int(HEIGHT/4*2.7-80) and mouse_y < int( HEIGHT/4*2.7+80):
                self.play_button_hover = True

                # Start game if mouse down
                if pg.mouse.get_pressed()[0] and fonts_loaded:
                    self.in_transition = True

                if int(self.slider_pos) + 1 == WIDTH:
                    global in_game
                    in_game = True

                    global mygame
                    mygame = SlitherGame()

            else:
                self.play_button_hover = False

            if self.in_transition:
                self.slider_pos += (WIDTH - self.slider_pos) / 3
            else:
                self.slider_pos = int(self.slider_pos / 1.12)

    def render(self):
        if fonts_loaded:
            # Main menu

            # Background texture
            x_amt = int(WIDTH / self.background_size[0]) + 1
            y_amt = int(HEIGHT / self.background_size[1]) + 1
            for x in range(x_amt):
                for y in range(y_amt):
                    screen.blit(self.background, (x * self.background_size[0], y * self.background_size[1]))
                
            # --- Slither.io Title ---
            # Scale
            slither_img_new = pg.transform.scale(self.slither_img, (
                self.slither_size[0] + int(math.sin(time.time() * 2) * 10),
                self.slither_size[1] + int(math.sin(time.time() * 2) * 10)))

            # Rotate
            slither_img_new = pg.transform.rotate(slither_img_new, math.sin(time.time() * 2.1) * 2)

            # Center position
            x = int(WIDTH / 2)
            y = int(HEIGHT / 4)
            rect = slither_img_new.get_rect(center=slither_img_new.get_rect(center=(x, y)).center)

            # Blit
            screen.blit(slither_img_new, rect.topleft)

            # --- Play button ---

            if self.play_button_hover:
                self.hover_increase = min(self.hover_increase + 3, 20)
            else:
                self.hover_increase = max(self.hover_increase - 3, 0)

            # Scale
            play_button_new = pg.transform.scale(self.play_button, (
                int(self.play_button_size[0] / 4 + self.hover_increase) + int(math.sin(time.time() * 1.8) * 15),
                int(self.play_button_size[1] / 4 + self.hover_increase + int(math.sin(time.time() * 1.8) * 15))))

            # Center
            rect = play_button_new.get_rect(center=play_button_new.get_rect(center=(int(WIDTH/2), int(HEIGHT/4*2.7))).center)

            # Blit
            screen.blit(play_button_new, rect.topleft)

            # Left credits
            screen.blit(self.nevwin_img, (10, HEIGHT-10-self.nevwin_img_size[1]))

            # Right credits
            screen.blit(self.by_name_img, (WIDTH-10-self.by_name_img_size[0], HEIGHT-10-self.by_name_img_size[1]))

            # Last score and High score
            pg.draw.rect(screen, WHITE, (int(WIDTH/2-230), HEIGHT-50, 460, 50))

            draw_text(f'Last score: {last_score}', int(WIDTH/2-215), HEIGHT-25, pos='left')
            draw_text(f'High score: {high_score}', int(WIDTH/2+215), HEIGHT-25, pos='right')

            # Slider Transition
            if self.slider_pos:
                pg.draw.rect(screen, BACKGROUND_SHADE, (0, 0, int(self.slider_pos) + 1, HEIGHT))

        else:
            screen.fill(BACKGROUND_SHADE)

            deg = (time.time() - start_load_time) * 250

            pg.draw.arc(screen, WHITE, (int(WIDTH/2)-100, int(HEIGHT/2)-100, 200, 200), math.radians(deg), math.radians(deg + 40))
            pg.draw.arc(screen, WHITE, (int(WIDTH/2)-100, int(HEIGHT/2)-100, 200, 200), math.radians(deg + 180), math.radians(deg + 220))

            deg = (time.time() - start_load_time) * -250

            pg.draw.arc(screen, WHITE, (int(WIDTH/2)-90, int(HEIGHT/2)-90, 180, 180), math.radians(deg), math.radians(deg + 40))
            pg.draw.arc(screen, WHITE, (int(WIDTH/2)-90, int(HEIGHT/2)-90, 180, 180), math.radians(deg + 180), math.radians(deg + 220))
            
            screen.blit(self.load_image, (int(WIDTH/2 - self.load_image_size[0]/2), int(HEIGHT/2 - self.load_image_size[1]/2)))

menu = SlitherMenu()

pg.init()
set_window_title()
screen = pg.display.set_mode((WIDTH, HEIGHT))

# Load and scale custom cursor
cursor_img = pg.image.load('./Images/cursor2.png')
cursor_img_size = cursor_img.get_size()
cursor_img = pg.transform.scale(cursor_img, (int(cursor_img_size[0]/5), int(cursor_img_size[1]/5)))

# Load Music
pg.mixer.music.load('./Music/sunny.wav')

last_score = 0

with open('./Highscore/score.txt', 'r') as f:
    try:
        high_score = int(f.read())
    except ValueError:
        print('Failed to load highscore')
        high_score = 0

fonts_loaded = False
def load_font_module():
    global start_load_time, myfont, fonts_loaded
    start_load_time = time.time()

    # Average font loading time: 10 seconds
    try:
        # SKIP FONT LOADING (TEMPORARY):
        # fonts_loaded = True

        pg.font.init()
        # myfont = pg.font.SysFont('microsoftsansserif', 35)
        # myfont = pg.font.Font('./Fonts/TESLA.ttf', 23)
        myfont = pg.font.Font('./Fonts/coolfont2.ttf', 23)

        # Minimum 2 seconds load time
        while time.time() - start_load_time < 3:
            pass
        fonts_loaded = True
    except pg.error:
        print('Failed to load fonts.')

t = threading.Thread(target=load_font_module)
t.start()

clock = pg.time.Clock()

in_game = False

running = True
loop_counter = 0
while running:
    loop_counter += 1
    clock.tick(60)

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    if pg.key.get_pressed()[pg.K_SPACE]:
        space = True
    else:
        space = False

    if in_game:
        mygame.update(space=space)
    else:
        menu.update()

    update_screen()

pg.quit()