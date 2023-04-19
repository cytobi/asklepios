# todo: more debug prints, error handling, user guidance, potentially different key to exit

import cv2  # for video capture
import keyboard  # for keypress detection
import os  # for directory creation
import time  # to check time between pictures
import json  # for config
import threading  # for multi-threading


debug = True  # set to True to enable debug prints

webcam_ports = []  # list of ports for the webcams that shall be used

cwd = os.getcwd()  # current working directory

dir = cwd + "\data\\"  # directory to save the frames to

image_amount = 5  # number of different frames to save, default is 5

next_image = 0  # next image number

countdown_time = 3  # time in seconds to wait before taking a picture, default is 3

time_between_pictures = 20  # time in seconds between pictures, default is 20

time_of_last_picture = []  # time of last picture

running = True  # set to False to stop the program


def debug_print(to_print):
    if debug:
        print(to_print)


def save_frame(frame):
    global next_image
    filename = "image" + str(next_image) + ".png"  # name of the file to save
    debug_print("...to " + dir + filename)
    next_image += 1  # increment next_image
    if next_image >= image_amount:  # reset next_image if it is too high
        next_image = 0
    cv2.imwrite(dir + filename, frame)  # save the frame


def handle_one_webcam(i, vc, time_of_last_picture):
    global running
    key_to_observe = chr(ord("a") + i)  # key to observe for this webcam
    while True:
        # check for keypress on observed key
        if keyboard.is_pressed(key_to_observe):
            # check if the time between pictures is long enough
            if abs(time.time() - time_of_last_picture[i]) > time_between_pictures:
                time.sleep(countdown_time)  # wait for countdown_time seconds
                debug_print("writing frame of cam " + str(i) + " to...")
                rval, frame = vc[i].read()  # read frame
                rval, frame = vc[i].read()  # read a second frame to avoid lag
                save_frame(frame)  # save frame
                # set time_of_last_picture to current time
                time_of_last_picture[i] = time.time()

        # check if program should terminate, if so, break out of loop and terminate thread
        if not running:
            break


# main function
def main():
    global webcam_ports, image_amount, countdown_time, time_between_pictures, time_of_last_picture, running

    # load config
    config_file = open(cwd + "\config\config.json")  # open config file
    config = json.load(config_file)  # load config file
    config_file.close()  # close config file
    # set variables from config
    webcam_ports = config["webcam_ports"]
    image_amount = config["image_amount"]
    countdown_time = config["countdown_time"]
    time_between_pictures = config["time_between_pictures"]

    # open all video captures
    vc = []
    for port in webcam_ports:
        temp_vc = cv2.VideoCapture(port)
        if temp_vc.isOpened():
            vc.append(temp_vc)

            # add 0 to time_of_last_picture for each webcam
            time_of_last_picture.append(0)

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

    # register threads for each webcam
    threads = []
    for i in range(webcam_amount):
        threads.append(
            threading.Thread(
                target=handle_one_webcam, args=(i, vc, time_of_last_picture)
            )
        )

    # start all threads
    for i in threads:
        i.start()

    # user guidance
    print("press ESC to exit or press Ctrl+C in the terminal for a hard stop")

    # main loop
    while running:
        # exit if esc is pressed
        if keyboard.is_pressed("esc"):
            running = False

    # wait for all threads to finish
    for i in threads:
        i.join()

    # close all video captures
    for i in vc:
        i.release()


main()
