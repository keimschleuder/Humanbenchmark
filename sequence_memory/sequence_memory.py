import pyautogui as gui
from PIL import Image
import sys
import numpy as np
import time
import threading

gui.PAUSE = 0.00001

corners = [[(743, 290), (1217, 290)], 
           [(743, 764), (1217, 764)]]

screenshots = []
sequence = []
coordinatesOfSquares = []
numSqares = 0
memoryCheck = 0

def start_game():
    global screenshots
    screenshot = gui.screenshot()
    screenshot = screenshot.crop((929, 656, 930, 657))

    found = search_hex_color(screenshot, "#FFD154", 30)

    if found == 0:
        print("Found Start Button")
        screenshotting.start()
        memory.start()
        time.sleep(1)
        starting.start()
        time.sleep(1.5)
        screenshots = []
        print("starting to take screenshots")
        time.sleep(0.5)
        play()

def start():
    print("starting the game")
    gui.moveTo(929, 656)
    gui.leftClick()

def getNumberSqaures():
    global numSqares, coordinatesOfSquares
    screenshot = gui.screenshot()
    screenshot = screenshot.crop((743, 547, 1217, 548))

    x = search_hex_color(screenshot, '#2B87D1', 20)

    width = 474

    try:
        numSqares = int(width / x)
        print("Squares: {}*{}".format(numSqares, numSqares))
    except:
        print("Number not found")
        sys.exit()

    sqare = int(width / numSqares)

    for i in range(numSqares):
        my_x = 743 + sqare * (i + 0.5)
        for j in range(numSqares):
            my_y = 290 + sqare * (j + 0.5)
            coordinatesOfSquares.append((my_x, my_y))

def color_distance(c1, c2):
    # Calculate the Euclidean distance between two colors (RGB)
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def search_hex_color(image, hex_color, tolerance):
    # Convert hex color string to RGB tuple
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    # Convert the image to RGB mode
    rgb_image = image.convert('RGB')
    width, height = rgb_image.size

    # Search for the hex color with tolerance in the image
    found = False
    for y in range(height):
        for x in range(width):
            pixel_color = rgb_image.getpixel((x, y))
            if color_distance(pixel_color, rgb_color) <= tolerance:
                found = True
                return x
    
    if not found:
        return "Error"

def find_white_pixel():
    global coordinatesOfSquares, screenshots
    rgb_image = screenshots[0].convert('RGB')

    screenshots.pop(0)

    # Search for the first white pixel in the image
    for mySqare in coordinatesOfSquares:
        pixel_color = rgb_image.getpixel(mySqare)
        if pixel_color == (255, 255, 255):
            return mySqare  # Return coordinates of the first white pixel

    return None 

def get_screenshot():
    global screenshots, running
    while running:
        screenshots.append(gui.screenshot())

def memory_optimization():
    global screenshots, memoryCheck
    while running:
        try:
            image = screenshots[memoryCheck].crop((929, 656, 930, 657))
            image = image.convert('L')
            image = np.array(image)
            if np.sum(image == 255) == 0:
                screenshots.pop[memoryCheck]
            else:
                memoryCheck += 1
        except:
            continue

def play():
    global screenshots, memoryCheck
    for i in range(laps):
        print("Round Number {}".format(i + 1))
        getNumberSqaures()
        j = 0
        lastChange = 0
        positions = [None]
        while True:
            try:
                pos = find_white_pixel()
            except:
                break
            if positions[len(positions) - 1] != pos:
                positions.append(pos)
                print(pos)
                lastChange = j
            j += 1
            if lastChange + 20 <= j:
                break

        for myPos in positions:
            if myPos == None:
                continue
            else:
                gui.moveTo(myPos[0], myPos[1])
                gui.leftClick()
                time.sleep(0.5)
        gui.moveTo(980, 250)
        screenshots = []
        memoryCheck = 0
        if i < 3:
            sleeping = 3
        elif i < 20:
            sleeping = i
        else:
            sleeping = int(i * 0.75)
        time.sleep(sleeping)

laps = int(input("How far do you want to go? "))

# Threads
running = True
starting = threading.Thread(target = start)
screenshotting = threading.Thread(target = get_screenshot)
memory = threading.Thread(target = memory_optimization)

time.sleep(2)
start_game()

print("Finished")
running = False