import pygame
import cv2
import sys
from random import randint
from pygame.math import Vector2

from models import GameObject, Ball
from utils import (
    load_sound,
    load_sprite,
    random_velocity,
    print_text_middle,
    print_text_bottom,
    cv2_img_to_surface,
    get_webcam_img,
    process_hands,
)

SCREEN_RES = (1280, 720)


class FingPong:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode(SCREEN_RES)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.ball = Ball(
            Vector2(SCREEN_RES) / 2, load_sprite("ball"), random_velocity(15, 30)
        )
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 1280)
        self.camera.set(4, 720)
        self.frame = None
        self.finger_coords = []

    def main_loop(self):
        while True:
            self._handle_input()
            self._update_frame()
            self._process_game_logic()
            self._draw()
        return

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Fing Pong")
        return

    def _update_frame(self):
        img = get_webcam_img(self.camera)
        self.finger_coords = process_hands(img)
        for finger_pair in self.finger_coords:  # no. of pairs = no. of hands detected
            for fingertip_coords in finger_pair:
                cv2.circle(img, fingertip_coords, 5, (255, 0, 255), cv2.FILLED)
            cv2.line(img, finger_pair[0], finger_pair[1], (222, 22, 222), 2)
        self.frame = img
        return

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                self.camera.release()
                cv2.destroyAllWindows()
                sys.exit()
        return

    def _process_game_logic(self):
        self.ball.move()
        self.ball.handle_wall_collision()
        self.ball.handle_paddle_collision(self.finger_coords)
        self.message = f"{self.ball.bounces} bounces"
        # if self.ball.out_of_bounds_horizontal():
        #     self.message = f"You lost! {self.ball.bounces} bounces"
        return

    def _draw(self):
        img_fmtd = cv2_img_to_surface(self.frame)
        self.screen.blit(img_fmtd, (0, 0))
        self.ball.draw(self.screen)
        if self.message:
            print_text_bottom(self.screen, self.message, self.font)
        pygame.display.flip()
        self.clock.tick(60)

        return
