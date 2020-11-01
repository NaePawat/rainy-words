from game.words import Word
from game.timer import Timer
from game.player import Player
from game.word_library import word_set
from game.png_sprite import *
import random
import pygame
import re


def new_word():
    return Word(random.choice(list(word_set)))


class Game:

    def __init__(self):
        pygame.init()
        self.width = 1024
        self.height = 720
        self.font = pygame.font.Font('Assets/font/pixelart.ttf', 32)
        self.player_me = Player('Mon')
        self.player_bongo = bongo_sprite
        self.player_x = 50
        self.player_y = 420
        self.num_sprite = 0
        # self.ani_state = False
        # self.ani_clock = Timer()
        self.draw_main_state = 0
        self.draw_index = 0
        self.draw_vfx_status = 0
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_bongo_cat(self, png):
        self.screen.blit(pygame.transform.scale(png, (300, 300)), (self.player_x, self.player_y))

    def draw_bongo_cat_flip(self, png):
        self.screen.blit(pygame.transform.flip(pygame.transform.scale(png, (300, 300)), True, False), (670, 420))

    # def check_ani_state(self):
    #    if not self.ani_state:
    #       self.draw_bongo_cat(self.player_bongo[0])
    #    if self.ani_state:
    #        self.ani_clock.tick()
    #        for event in pygame.event.get():
    #            self.bongo_animation(self.player_bongo, event)
    #        if self.ani_clock.time >= 3:
    #            self.ani_clock.reset()
    #            self.ani_state = False
    def draw_bongo_cat_flip(self, png):
        self.screen.blit(pygame.transform.flip(pygame.transform.scale(png, (300, 300)), True, False), (670, 420))


    def bongo_animation(self, state, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.draw_main_state = 2
                self.draw_bongo_cat(state[2])
            else:
                if self.draw_index % 2 == 0:
                    self.draw_main_state = 4
                    self.draw_bongo_cat(state[4])
                    self.draw_bongo_cat_flip(state[4])
                if self.draw_index % 2 == 1:
                    self.draw_main_state = 6
                    self.draw_bongo_cat_flip(state[6])
                    self.draw_bongo_cat(state[6])
                self.draw_index += 1

    #def boom_animation(self, state ):
       # if event.type == pygame.KEYDOWN:
         #   if self.player_me.keystrokes == word.word and self.player_me.confirm_key and event.key == pygame.K_ENTER:
              #  self.draw_boom(state[1])



    def draw_text(self, text, xpos, ypos):
        text_a = self.font.render(text, True, pygame.Color('black'))
        text_a_rect = text_a.get_rect()
        text_a_rect.topright = (xpos, ypos)
        self.screen.blit(text_a, text_a_rect)

    def draw_text_waiting(self, text, xpos, ypos):
        font = pygame.font.Font("Fonts/pixelart.ttf", 35)
        #font = pygame.font.Font("pixelfont", 40, bold = True)
        text_a = font.render(text, True, pygame.Color(102, 0, 102))

        text_a_rect = text_a.get_rect()
        text_a_rect.topright = (xpos, ypos)
        self.screen.blit(text_a, text_a_rect)

    def draw_timer(self, time):
        time_text = self.font.render(str(time), True, pygame.Color('black'))
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (1010, 10)
        self.screen.blit(time_text, time_text_rect)

    def draw_score(self, score):
        score_text = self.font.render('score ' + str(score), True, pygame.Color('black'))
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, 10)
        self.screen.blit(score_text, score_text_rect)

    def draw_current_stroke(self, current_stroke):
        score_text = self.font.render(current_stroke, True, pygame.Color('black'))
        score_text_rect = score_text.get_rect()
        score_text_rect.midbottom = (512, 710)
        self.screen.blit(score_text, score_text_rect)

    def draw_name_stroke(self, current_stroke):
        name_text = self.font.render(current_stroke, True, pygame.Color('black'))
        name_text_rect = name_text.get_rect()
        name_text_rect.topleft = (230, 250)
        self.screen.blit(name_text, name_text_rect)

    def print_move_word(self, w):
        self.screen.blit(w.text, w.text_rect)
        w.text_rect.move_ip(0, w.fall_speed)
        w.y_pos += w.fall_speed

    def print_move_matching_word(self, w):
        self.screen.blit(w.matching_text, w.matching_text_rect)
        w.matching_text_rect.move_ip(0, w.fall_speed)
        self.display_select_word(w)

    def erase_word(self, w):
        pass

    def draw_player(self, state):
        self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bg_sprite[1], (200, 100)), 2), (70, 570))
        self.draw_main_state = True
        for event in pygame.event.get():
            self.bongo_animation(self.player_bongo, event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if self.draw_main_state:
            self.draw_bongo_cat(self.player_bongo[0])

    def insert_name(self):
        running = True
        type_state = False
        backspace_clock = Timer()
        while running:
            backspace_clock.tick()
            keys = pygame.key.get_pressed()
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(pygame.transform.scale(bg_sprite[3], (self.width, self.height)), (0, 0))
            if keys[pygame.K_BACKSPACE] and len(self.player_me.keystrokes) > 0 and backspace_clock.time >= 2 and type_state:
                backspace_clock.reset()
                self.player_me.keystrokes = self.player_me.keystrokes[:-1]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 230 <= mouse_pos[0] <= 830 and 250 <= mouse_pos[1] <= 325:
                        pygame.draw.rect(self.screen, (255, 0, 255), (230, 250, 600, 75))  # text button
                        print('text button clicked!')
                        type_state = True
                    elif 410 <= mouse_pos[0] <= 610 and 350 <= mouse_pos[1] <= 400:
                        if type_state and len(self.player_me.keystrokes) > 0:
                            print('confirm button clicked!')
                            self.player_me.name = self.player_me.keystrokes
                            print('Meow '+self.player_me.name+' has joined the fray!')
                            self.player_me.keystrokes = ''
                            self.lobby()
                        else:
                            print('hey fucker, what is your name?')
                    else:
                        type_state = False
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha() and type_state:
                        if len(self.player_me.keystrokes) == 20:
                            pass
                        else:
                            self.player_me.keystrokes += event.unicode
            mouse_pos = pygame.mouse.get_pos()
            self.draw_text('Please insert your name:', 768, 200)
            pygame.draw.rect(self.screen, (255, 255, 255), (410, 350, 200, 50))  # confirm button
            self.screen.blit(pygame.transform.scale(button_sprite[0], (600, 75)), (230, 250))  # text button texture
            self.draw_text('confirm', 595, 360)
            self.draw_name_stroke(self.player_me.keystrokes)
            pygame.display.update()

    def lobby(self):
        intro = True
        while intro:
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(pygame.transform.scale(bg_sprite[2], (self.width, self.height)), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.draw_text('Player 1: '+ self.player_me.name, 120, 240)
            self.draw_text('Player 2:', 760, 240)
            # set 1
            # self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 12.5),
            #                 (-40, 40))  # mid bottom
            # self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), -4),
            #                 (-390, 125))  # bottom left
            # self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 35.5),
            #                (240, -70))  # bottom right
            # self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 105),
            #                (350, -300))  # right
            # set 2
            # self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 192.5),
            #                 (-110, -550))  # mid top
            # self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 176),
            #                 (350, -500))  # top right
            # self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 205.5),
            #                 (-620, -610))  # top left
            # self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), -80),
            #                 (-550, -180))  # left


            pygame.display.update()


    def waiting(self):
        intro = True
        while intro:
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(pygame.transform.scale(bg_sprite[3], (self.width, self.height)), (0, 0))
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bg_sprite[4], (750,400)), 0), (40,50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.draw_text_waiting('Hello ! , ', 300, 120)
            self.draw_text_waiting('Waiting for your opponent...', 750, 200)
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 12.5),
                             (120, 40))
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bg_sprite[5], (300, 300)), -12.5),
                             (600, 300))

            pygame.display.update()

    def display_select_word(self, w):
        y_offset = w.y_pos - 100
        self.screen.blit(pygame.transform.scale(self.player_bongo[3], (100, 100)), (w.x_offset, y_offset))

    def display_VFX(self, w, frame):
        self.screen.blit(pygame.transform.scale(self.player_bongo[frame], (300, 300)), (w.x_offset,w.y_pos))


    def display_select_word(self, w):
        y_offset = w.y_pos - 100
        self.screen.blit(pygame.transform.scale(self.player_bongo[3], (100, 100)), (w.x_offset, y_offset))

    def display_VFX(self, w, frame):
        self.screen.blit(pygame.transform.scale(self.player_bongo[frame], (300, 300)), (w.x_offset,w.y_pos))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        word_mem = []
        record_remove_words = []
        timer = Timer()
        backspace_clock = Timer()
        vfx_clock = Timer()
        game_clock = Timer()
        game_timer = 300
        while running:
            # clock
            clock.tick(30)
            backspace_clock.tick()
            game_clock.tick()
            keys = pygame.key.get_pressed()
            if game_clock.time == 30:
                game_clock.reset()
                game_timer -= 1
                if game_timer == 0:
                    self.end_state()
                    continue

            # redraw per frame
            self.draw_main_state = 0
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(pygame.transform.scale(bg_sprite[0], (self.width, self.height)), (0, 0))
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bg_sprite[1], (200, 100)), 2), (70, 570))
            self.screen.blit(
                pygame.transform.flip(pygame.transform.rotate(pygame.transform.scale(bg_sprite[1], (200, 100)), 2),
                                      True, False), (750, 570))

            # self.draw_bongo_cat(self.player_bongo[0])
            # self.check_ani_state()

            # event listen
            if keys[pygame.K_BACKSPACE] and len(self.player_me.keystrokes) > 0 and backspace_clock.time >= 2:
                backspace_clock.reset()
                self.player_me.keystrokes = self.player_me.keystrokes[:-1]
            for event in pygame.event.get():
                self.bongo_animation(self.player_bongo, event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        self.player_me.keystrokes += event.unicode
                    elif event.unicode == '\r' or event.key == pygame.K_RETURN:
                        self.player_me.confirm_key = True

            # draw
            self.draw_score(self.player_me.score)
            self.draw_current_stroke(self.player_me.keystrokes)
            self.draw_timer(game_timer)

            # algo
            if len(word_mem) <= 1:
                timer.tick()
            if 2 == random.randint(1, 60):
                word_mem.append(new_word())
            if len(word_mem) <= 1 and timer.time >= 90:
                word_mem.append(new_word())
                timer.reset()

            removed_words = []

            for word in word_mem:

                if self.player_me.keystrokes == word.word and self.player_me.confirm_key:
                    self.erase_word(word)
                    self.draw_boom(word)
                    self.player_me.score += 1
                    removed_words.append(word)
                    record_remove_words.append(word)
                    continue

                if self.player_me.keystrokes == '':
                    s = False
                else:
                    s = re.search("^" + self.player_me.keystrokes, word.word)

                if s:
                    word.match_text(s.span())
                    word.start_match = True
                    self.print_move_word(word)
                    self.print_move_matching_word(word)
                elif word.start_match:
                    word.start_match = False
                    word.unmatch_text()
                    self.print_move_word(word)
                else:
                    self.print_move_word(word)

                if word.text_rect.topleft[1] > 720:
                    removed_words.append(word)
                    continue

            for word in record_remove_words:
                print(word.word)
                self.display_VFX(word, word.draw_vfx)
                if word.draw_vfx == 6:
                    word.draw_vfx = 0
                    record_remove_words.remove(word)
                    print("finish " + word.word)
                word.draw_vfx += 1

            if len(removed_words) > 0:
                print('removed')
                word_mem = [i for i in word_mem if i not in removed_words]

            # update object state
            if self.player_me.confirm_key:
                self.player_me.keystrokes = ''
                self.player_me.confirm_key = False

            if self.draw_main_state == 0:
                self.draw_bongo_cat(self.player_bongo[0])
                self.draw_bongo_cat_flip(self.player_bongo[0])

            # update frame
            pygame.display.update()

    def end_state(self):
        summary = True
        while summary:
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 12.5),
                             (-40, 40))
            pygame.display.update()
