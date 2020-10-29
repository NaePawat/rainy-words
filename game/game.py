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
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.player_me = Player('Mon')
        self.player_bongo = bongo_sprite
        self.player_x = 50
        self.player_y = 420
        # self.ani_state = False
        # self.ani_clock = Timer()
        self.draw_main_state = True
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_bongo_cat(self, png):
        self.screen.blit(pygame.transform.scale(png, (300, 300)), (self.player_x, self.player_y))

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

    def bongo_animation(self, state, event):
        if event.type == pygame.KEYDOWN:
            self.draw_main_state = False
            if event.key == pygame.K_SPACE:
                self.draw_bongo_cat(state[2])
            else:
                self.draw_bongo_cat(state[1])

    def draw_text(self, text, xpos, ypos):
        text_a = self.font.render(text, True, pygame.Color('black'))
        text_a_rect = text_a.get_rect()
        text_a_rect.topright = (xpos, ypos)
        self.screen.blit(text_a, text_a_rect)

    def draw_timer(self, time):
        time_text = self.font.render(str(time), True, pygame.Color('black'))
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (1010, 10)
        self.screen.blit(time_text, time_text_rect)

    def draw_score(self, score):
        score_text = self.font.render('score:' + str(score), True, pygame.Color('black'))
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, 10)
        self.screen.blit(score_text, score_text_rect)

    def draw_current_stroke(self, current_stroke):
        score_text = self.font.render(current_stroke, True, pygame.Color('black'))
        score_text_rect = score_text.get_rect()
        score_text_rect.midbottom = (512, 710)
        self.screen.blit(score_text, score_text_rect)

    def print_move_word(self, w):
        self.screen.blit(w.text, w.text_rect)
        w.text_rect.move_ip(0, w.fall_speed)

    def print_move_matching_word(self, w):
        self.screen.blit(w.matching_text, w.matching_text_rect)
        w.matching_text_rect.move_ip(0, w.fall_speed)

    def erase_word(self, w):
        pygame.draw.polygon(self.screen, pygame.Color('white'),
                            [w.text_rect.topleft, w.text_rect.bottomleft, w.text_rect.topright,
                             w.text_rect.bottomright])

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

    def lobby(self):
        intro = True
        while intro:
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(pygame.transform.scale(bg_sprite[2], (self.width, self.height)), (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.draw_text('Player 1:', 120, 240)
            self.draw_text('Player 2:', 760, 240)
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 12.5),
                             (-40, 40))
            pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        word_mem = []
        timer = Timer()
        backspace_clock = Timer()
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
            self.draw_main_state = True
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(pygame.transform.scale(bg_sprite[0], (self.width, self.height)), (0, 0))
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bg_sprite[1], (200, 100)), 2), (70, 570))
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
                    self.player_me.score += 1
                    removed_words.append(word)
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

            if len(removed_words) > 0:
                print('removed')
                word_mem = [i for i in word_mem if i not in removed_words]

            # update object state
            if self.player_me.confirm_key:
                self.player_me.keystrokes = ''
                self.player_me.confirm_key = False
            if self.draw_main_state:
                self.draw_bongo_cat(self.player_bongo[0])

            # update frame
            pygame.display.update()

    def end_state(self):
        summary = True
        while summary:
            self.screen.fill(pygame.Color('white'))
            self.screen.blit(pygame.transform.rotate(pygame.transform.scale(bongo_sprite[1], (1024, 1024)), 12.5),
                             (-40, 40))
            pygame.display.update()
