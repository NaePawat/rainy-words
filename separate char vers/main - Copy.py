from game.words import Word
from game.timer import Timer
from game.player import Player
from game.word_library import word_set
import random
import pygame
import re


(width, height) = (1024, 720)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)


def new_word():
    return Word(word_set[random.randint(0, len(word_set)-1)])


def draw_score(score):
    score_text = font.render('score:' + str(score), True, black)
    score_text_rect = score_text.get_rect()
    score_text_rect.topleft = (0, 0)
    screen.blit(score_text, score_text_rect)


def draw_current_stroke(current_stroke):
    score_text = font.render(current_stroke, True, black)
    score_text_rect = score_text.get_rect()
    score_text_rect.midbottom = (512, 720)
    screen.blit(score_text, score_text_rect)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))

    running = True

    font = pygame.font.Font('freesansbold.ttf', 32)

    word_mem = []

    randword = 0

    timer = Timer()

    player1 = Player('player 1')

    while running:
        framerate = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode != '\r' and event.unicode != '\b':
                    player1.keystrokes += event.unicode
                elif event.unicode == '\r':
                    player1.confirm_key = True
                elif len(player1.keystrokes) > 0:
                    player1.keystrokes = player1.keystrokes[:-1]

        screen.fill(white)
        draw_score(player1.score)
        draw_current_stroke(player1.keystrokes)

        if len(word_mem) <= 1:
            timer.tick()

        if timer.time >= 90:
            timer.reset()
            word_mem.append(new_word())
        elif len(word_mem) <= 1 and timer.time >= 90:
            word_mem.append(new_word())

        removed_words = []

        for word in word_mem:

            if player1.keystrokes == word.word and player1.confirm_key:
                pygame.draw.polygon(screen, white, [word.chars[0][1].topleft, word.chars[0][1].bottomleft, word.chars[-1][1].topright, word.chars[-1][1].bottomright])
                player1.score += 1
                removed_words.append(word)
                continue

            if player1.keystrokes == '':
                s = False
            else:
                s = re.search("^" + player1.keystrokes, word.word)

            if s:
                word.match_text(s.span())
                word.start_match = True
            elif word.start_match:
                word.start_match = False
                word.unmatch_text()

            for char in word.chars:
                screen.blit(char[0], char[1])
                char[1].move_ip(0, 1)

            if word.chars[0][1].bottomleft[1] > 720:
                removed_words.append(word)
                print('fuck1')
                continue

        if len(removed_words) > 0:
            print('removed')
            word_mem = [i for i in word_mem if i not in removed_words]
            removed_words = []

        if player1.confirm_key:
            player1.keystrokes = ''
            player1.confirm_key = False
        pygame.display.update()

