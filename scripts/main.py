# todo: error handling
# issue: if button is continuously pressed, cpu usage is high. could be solved with sleep, but then the button might not be recognized

import cv2  # for video capture
import keyboard  # for keypress detection
import os  # for directory creation
import time  # to check time between pictures
import json  # for config
import threading  # for multi-threading


debug = True  # set to True to enable debug prints

webcam_ports = []  # list of ports for the webcams that shall be used
image_amount = 5  # number of different frames to save, default is 5
countdown_time = 3  # time in seconds to wait before taking a picture, default is 3
time_between_pictures = 20  # time in seconds between pictures, default is 20
exit_button = "esc"  # key to exit the program, default is "esc"
custom_webcam_keys = []  # list of custom keys, must be same order as webcam_ports
use_custom_webcam_keys = False  # set to True to use custom keys, default is False

cwd = os.getcwd()  # current working directory
dir = cwd + "\data\\"  # directory to save the frames to

next_image = 0  # next image number

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


def handle_one_webcam(i, vc, time_of_last_picture, custom_key):
    global running
    debug_print("started thread for webcam " + str(i))
    if custom_key != "":  # check if custom key is set
        key_to_observe = custom_key  # use custom key
    else:
        key_to_observe = chr(ord("a") + i)  # calculate key to observe for this webcam
    while True:
        # check for keypress on observed key
        if keyboard.is_pressed(key_to_observe):
            debug_print("key " + key_to_observe + " was pressed")
            # check if the time between pictures is long enough
            if abs(time.time() - time_of_last_picture[i]) > time_between_pictures:
                debug_print(
                    "picture will be taken in " + str(countdown_time) + " seconds"
                )
                time.sleep(countdown_time)  # wait for countdown_time seconds
                debug_print("writing frame of cam " + str(i) + " to...")
                rval, frame = vc[i].read()  # read frame
                rval, frame = vc[i].read()  # read a second frame to avoid lag
                save_frame(frame)  # save frame
                # set time_of_last_picture to current time
                time_of_last_picture[i] = time.time()

        # check if program should terminate, if so, break out of loop and terminate thread
        if not running:
            debug_print("thread for webcam " + str(i) + " is terminating")
            break
        # time.sleep(0.05)  # wait shortly to reduce cpu usage


# main function
def main():
    global webcam_ports, image_amount, countdown_time, time_between_pictures, exit_button, custom_webcam_keys, use_custom_webcam_keys, time_of_last_picture, running

    print("starting...")

    # create data directory if it does not exist
    if not os.path.exists(dir):
        debug_print("creating data directory...")
        os.makedirs(dir)

    # load config
    debug_print("loading config...")
    config_file = open(cwd + "\config\config.json")  # open config file
    config = json.load(config_file)  # load config file
    config_file.close()  # close config file
    # set variables from config
    webcam_ports = config["webcam_ports"]
    image_amount = config["image_amount"]
    countdown_time = config["countdown_time"]
    time_between_pictures = config["time_between_pictures"]
    exit_button = config["exit_button"]
    use_custom_webcam_keys = config["use_custom_webcam_keys"]
    if use_custom_webcam_keys:
        custom_webcam_keys = config["custom_webcam_keys"]

    # open all video captures
    debug_print("opening video captures...")
    vc = []
    for port in webcam_ports:
        temp_vc = cv2.VideoCapture(port)
        if temp_vc.isOpened():
            vc.append(temp_vc)

            # add 0 to time_of_last_picture for each webcam
            time_of_last_picture.append(0)

            if not use_custom_webcam_keys:
                # add none to custom_webcam_keys for each webcam if custom keys are not used
                custom_webcam_keys.append("")

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

    # check if correct amount of custom keys is specified

    if len(custom_webcam_keys) != webcam_amount:
        if use_custom_webcam_keys:
            print("error: wrong amount of custom keys specified")
        else:
            print("error: appending '' to custom keys failed")
        exit()

    # register threads for each webcam
    debug_print("registering threads...")
    threads = []
    for i in range(webcam_amount):
        threads.append(
            threading.Thread(
                target=handle_one_webcam,
                args=(i, vc, time_of_last_picture, custom_webcam_keys[i]),
            )
        )

    # start all threads
    debug_print("starting threads...")
    for i in threads:
        i.start()

    # user guidance
    print("started")
    print(
        "press "
        + exit_button.upper()
        + " to exit or press Ctrl+C in the terminal for a hard stop"
    )

    # main loop
    while running:
        # exit if esc is pressed
        if keyboard.is_pressed(exit_button):
            running = False

    print("exiting...")

    # wait for all threads to finish
    debug_print("waiting for threads to finish...")
    for i in threads:
        i.join()

    # close all video captures
    debug_print("closing video captures...")
    for i in vc:
        i.release()


main()
