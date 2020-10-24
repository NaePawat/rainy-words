import random
import pygame

black = (0, 0, 0)
green = (0, 255, 0)


class Word:

    def __init__(self, word):
        pygame.init()
        font = pygame.font.Font('freesansbold.ttf', 32)
        self.start_match = False
        self.fall_speed = random.randint(2,5)
        self.word = word
        self.chars = []
        self.text_width, self.text_height = font.size(word)
        self.x_offset = random.randint(0, 1024 - self.text_width)
        for c in word:
            char = font.render(c, True, black)
            char_rect = char.get_rect()
            self.x_offset = self.x_offset + font.size(c)[0]
            char_rect.topleft = (self.x_offset, 0)
            self.chars.append([char, char_rect])

    def match_text(self, span):
        font = pygame.font.Font('freesansbold.ttf', 32)
        start, end = span
        for i in range(start, end):
            self.chars[i][0] = font.render(self.word[i], True, green)

    def unmatch_text(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        for i in range(0, len(self.word)):
            self.chars[i][0] = font.render(self.word[i], True, black)