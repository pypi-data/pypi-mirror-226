import pyautogui
import random
import time
from util import KEY_NAMES


SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

start_time = time.time()


def monkey_test(duration):
    while time.time() - start_time < duration:
        # Random mouse movement
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        pyautogui.moveTo(x, y, duration=0.1)

        # Random click
        if random.random() < 0.1:
            pyautogui.click()
        else:
            pyautogui.doubleClick()

        # Random keypress
        if random.random() < 0.5:
            pyautogui.press(random.choice(KEY_NAMES))
