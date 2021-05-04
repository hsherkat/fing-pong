from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sound, bounce


SCREEN_RES = (1280, 720)


class GameObject:
    def __init__(self, position, sprite, velocity=0):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        return

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)
        return

    def move(self):
        self.position = self.position + self.velocity
        return

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Ball(GameObject):
    def __init__(self, position, sprite, velocity):
        self.sprite = rotozoom(sprite, 0, 0.05)
        super().__init__(position, self.sprite, velocity)
        self.click_sound = load_sound("click_new2")
        self.bounces = 0
        self.clipping = 0
        return

    ####

    def reflect_v_vertical(self):
        vx, vy = self.velocity
        self.velocity = Vector2(vx, -vy)
        return

    def reflect_v_horizontal(self):
        vx, vy = self.velocity
        self.velocity = Vector2(-vx, vy)
        return

    def is_oob_vertical(self):
        x, y = self.position
        return y <= 0 or y >= SCREEN_RES[1]

    def is_oob_horizontal(self):
        x, y = self.position
        return x <= 0 or x >= SCREEN_RES[0]

    ####

    def handle_wall_collision(self):
        if self.is_oob_vertical():
            self.reflect_v_vertical()
            self.click_sound.play()
        # if self.is_oob_horizontal(): # can experiment w/o losing by uncommenting
        #     self.reflect_v_horizontal()
        #     self.click_sound.play()
        return

    def handle_paddle_collision(self, finger_coords):
        if self.clipping:  # avoid multiple hits in consecutive frames
            self.clipping -= 1
            return
        for finger_pair in finger_coords:
            tip1, tip2 = map(Vector2, finger_pair)
            if any(  # lerp gives line along tip1 to tip2
                (tip1.lerp(tip2, frac).distance_to(self.position) < 25)
                for frac in [0.1 * n for n in range(11)]
            ):
                v_paddle = Vector2(finger_pair[0]) - Vector2(finger_pair[1])
                self.velocity = bounce(self.velocity, v_paddle)
                self.click_sound.play()
                self.bounces += 1
                self.clipping = 10
                return
