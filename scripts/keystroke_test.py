# test to see if a keypress can be registered

import keyboard

while True:
    if keyboard.is_pressed("a"):  # test if 'a' is pressed
        print("'a' was pressed")
        break  # end loop/program
