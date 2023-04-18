# todo: anti-spam, json for config, error handling, comments, user guidance, potentiall different key to exit

import cv2  # for video capture
import keyboard  # for keypress detection
import os  # for directory creation
import asyncio  # for async functions


debug = True  # set to True to enable debug prints

webcam_ports = [1, 2]  # list of ports for the webcams that shall be used

cwd = os.getcwd()  # current working directory

dir = cwd + "\data\\"  # directory to save the frames to

image_amount = 5  # number of different frames to save

next_image = 0  # next image number

countdown_time = 3  # time in seconds to wait before taking a picture


def debug_print(to_print):
    if debug:
        print(to_print)


async def save_frame(frame):
    global next_image
    filename = "image" + str(next_image) + ".png"  # name of the file to save
    debug_print("...to " + dir + filename)
    next_image += 1  # increment next_image
    if next_image >= image_amount:  # reset next_image if it is too high
        next_image = 0
    cv2.imwrite(dir + filename, frame)  # save the frame


async def handle_keypress(keypress, vc, webcam_amount):
    # check for keypresses for each webcam
    for i in range(webcam_amount):
        # tests a for cam 0, b for cam 1, etc.
        if keypress == chr(ord("a") + i):
            await asyncio.sleep(countdown_time)  # wait for countdown_time seconds
            debug_print("writing frame of cam " + str(i) + " to...")
            rval, frame = vc[i].read()  # read frame
            rval, frame = vc[i].read()  # read a second frame to avoid lag
            await save_frame(frame)  # save frame


# main function
async def main():
    running = True  # set to False to stop the program

    # open all video captures
    vc = []
    for port in webcam_ports:
        temp_vc = cv2.VideoCapture(port)
        if temp_vc.isOpened():
            vc.append(temp_vc)

    # check for errors in opening the video captures
    if len(webcam_ports) == 0:
        print("error: no webcams specified")
        exit()
    if len(vc) == 0:
        print("error: no video captures could be opened")
        exit()
    if len(vc) != len(webcam_ports):
        print("error: not all video captures could be opened")
        exit()

    webcam_amount = len(vc)  # amount of webcams that are being used

    # user guidance
    print("press ESC to exit or press Ctrl+C in the terminal for a hard stop")

    # main loop
    while running:
        keypress = keyboard.read_key()  # read keypress
        await handle_keypress(keypress, vc, webcam_amount)

        # exit if esc is pressed
        if keypress == "esc":
            running = False

    # close all video captures
    for i in vc:
        i.release()


asyncio.run(main())
