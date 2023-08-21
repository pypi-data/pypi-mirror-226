# Dino Game Ai Bot

# IMPORTS
import pyautogui as gui
import keyboard
from PIL import Image, ImageGrab
import time
import math

# GLOBAl
DINO_GAME_URL = 'https://elgoog.im/dinosaur-game/'


# BOT

class bot:
    def __init__(self):
        self.creator = 'Akmal Riyas'
        self.version = '1.0'
        self.modules_used = ['Pillow', 'Pyautogui', 'Keyboard', 'Time', 'Math']

    def get_pixel(self, image, x, y):
        px = image.load()
        return px[x, y]  # RETURN PIXEL

    def start(self):
        # IMG
        x, y, width, height = 0, 102, 1920, 872

        # CALC DINO TIME
        jumping_time = 0
        last_jumping_time = 0
        current_jumping_time = 0
        last_interval_time = 0

        # FIND OBSTACLES
        y_search1, y_search2, x_start, x_end = 557, 486, 400, 415
        y_search_for_bird = 460

        print("Initializing Bot \n")
        print('Press Q Key To Shut Down Bot \n')
        time.sleep(1)
        print('Bot Initializing In 3 Seconds( Please Switch Dino Game )')
        time.sleep(3)

        while True:
            t1 = time.time()

            # Exit
            if keyboard.is_pressed('q'):
                print('Your last score has been screenshotted in the local directory.')
                break

            sct_img = gui.screenshot(region=(x, y, width, height))
            sct_img.save("dino.jpg")
            bg_color = self.get_pixel(sct_img, 100, 100)

            try:
                for i in reversed(range(x_start, x_end)):

                    if self.get_pixel(sct_img, i, y_search1) != bg_color \
                            or self.get_pixel(sct_img, i, y_search2) != bg_color:
                        keyboard.press('up')
                        jumping_time = time.time()
                        current_jumping_time = jumping_time
                        break

                    if self.get_pixel(sct_img, i, y_search_for_bird) != bg_color:
                        keyboard.press("down")
                        time.sleep(0.4)

                        keyboard.release("down")
                        break

                interval_time = current_jumping_time - last_jumping_time

                if last_interval_time != 0 and math.floor(interval_time) != math.floor(last_interval_time):
                    x_end += 4
                    if x_end >= width:
                        x_end = width

                last_jumping_time = jumping_time
                last_interval_time = interval_time

            except:
                print("Error")
                break
