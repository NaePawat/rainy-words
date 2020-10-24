import random
import pygame

black = (0, 0, 0)
green = (0, 255, 0)


class Word:

    def __init__(self, word):
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.start_match = False
        self.fall_speed = random.randint(4, 8)
        self.word = word
        self.text_width, self.text_height = self.font.size(word)
        self.x_offset = random.randint(0, 1024 - self.text_width)
        self.matching_text = self.font.render("", True, black)
        self.matching_text_rect = self.matching_text.get_rect()

        self.text = self.font.render(word, True, black)
        self.text_rect = self.text.get_rect()
        self.text_rect.topleft = (self.x_offset, 0)

    def match_text(self, span):
        start, end = span
        matching_word = self.word[start:end]
        self.matching_text = self.font.render(matching_word, True, green)
        self.matching_text_rect = self.matching_text.get_rect()
        self.matching_text_rect.topleft = self.text_rect.topleft

    def unmatch_text(self):
        self.matching_text = self.font.render("", True, black)
        self.matching_text_rect = self.matching_text.get_rect()