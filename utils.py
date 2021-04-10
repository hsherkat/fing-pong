import cv2
import numpy as np
from random import random, randrange
from math import pi, sin, cos
import mediapipe as mp


from pygame import Color
from pygame.image import load, frombuffer
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame.transform import rotozoom


def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)
    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def print_text_middle(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)


def print_text_bottom(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    x, y = Vector2(surface.get_size())
    rect.center = Vector2(int(x // 2), y - 30)
    surface.blit(text_surface, rect)


def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)


def random_velocity(lo, hi):
    """Direction random. Speed random between lo and hi.
    """
    r = randrange(lo, hi)
    theta = 2 * pi * random()
    return Vector2(r * cos(theta), r * sin(theta))


def print_text_middle(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)
    return


def get_webcam_img(webcam):
    """Reading frame from cv2.VideoCapture stream.
    """
    success = False
    while not success:
        success, img = webcam.read()
    img_flipped = cv2.flip(img, 1)
    return img_flipped


def cv2_img_to_surface(img):
    """Converts img from cv2 format to pygame format.
    """
    format = "RGB"
    size = img.shape[1::-1]
    img[:, :, [0, 2]] = img[:, :, [2, 0]]
    surface = frombuffer(img.flatten(), size, format)
    return surface.convert()


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand_detector = mp_hands.Hands(
    min_detection_confidence=0.75
)  # default has fingertips being found all over


def process_hands(img):
    """Uses mediapipe hand detector to detect hands in img.
    Draws hand landmarks on the img (in place).
    Returns coords of thumb and pointer finger tip.
    """
    h, w, _ = img.shape
    results = hand_detector.process(img)
    out = []
    if detected_hands := results.multi_hand_landmarks:
        for hand_landmarks in detected_hands:
            out.append(get_fingertip_coords(hand_landmarks.landmark, h, w))
            # mp_drawing.draw_landmarks(img, hand_landmarks)  # remove eventually
    return out


def get_fingertip_coords(hand_landmarks, h, w):
    """Unnormalizes [0,1] to image dimensions,
    since mediapipe detector returns normalized coords.
    Landmark #4 and landmark #8 are the fingertips we care about.
    """
    thumb_tip = hand_landmarks[4]
    thumb_coords = int(w * thumb_tip.x), int(h * thumb_tip.y)
    pointer_tip = hand_landmarks[8]
    pointer_coords = int(w * pointer_tip.x), int(h * pointer_tip.y)
    return thumb_coords, pointer_coords


def bounce(v_in, v_floor):
    """Reflect component of v_in that is perpendicular to v_floor.
    v_in = v_parallel + v_perp
    """
    v_floor = v_floor.normalize()
    v_parallel = v_in.dot(v_floor) * v_floor
    v_perp = v_in - v_parallel
    return v_parallel - v_perp


##############

# def cv2_img_to_surface(img):
#     if img.dtype.name == "uint16":
#         img = (img / 256).astype("uint8")
#     size = img.shape[1::-1]
#     if len(img.shape) == 2:
#         img = np.repeat(img.reshape(size[1], size[0], 1), 3, axis=2)
#         format = "RGB"
#     else:
#         format = "RGBA" if img.shape[2] == 4 else "RGB"
#         img[:, :, [0, 2]] = img[:, :, [2, 0]]
#     flipped = cv2.flip(img, 1)
#     surface = frombuffer(flipped.flatten(), size, format)
#     return surface.convert_alpha() if format == "RGBA" else surface.convert()
