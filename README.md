# asklepios

a tool to grab frames from a webcam and put them into an already running obs slideshow without having to refresh the slideshow

developed for windows with python 3.11.3

## detailed usage guide

### notes

- this guide assumes you already have [git](https://git-scm.com/) installed
- everything in pointy brackets `<>` including the brackets themselves should be replaced with your desired values
- some of the scripts are interactive and may request user input via the console
  - e.g. webcam_test.py requests the number of webcam ports to test: `How many sources to test? (default: 5):`
  - you can either enter a number or just directly hit enter to use the default
- all frames you save with the main script will be saved in `<install location>\asklepios\data`

### instructions

- download & install [python](https://www.python.org/downloads/): tick add to PATH, then click install now
- open terminal (win+r, then type cmd and hit enter)
- install numpy: `pip install numpy`
- install opencv: `pip install opencv-python`
- install keyboard: `pip install keyboard`
- navigate to the desired install location for asklepios: `cd <path to asklepios' install location>`
  - you may first have to change drives if the desired install location is not on the C: drive
  - e.g. `D:` and then `cd D:\Programs\`
- clone this repository: `git clone https://github.com/cytobi/asklepios.git`
- navigate into repository folder: `cd asklepios`
- run desired scripts via: `python scripts/<scriptname.py>`
  - test which ports your webcams use: `python scripts/webcam_test.py`
  - run the main script to save frames: `python scripts/main.py`
- if you wish to change some config (e.g. the ports your webcams use, the countdown time, etc) open the config.json file in the config folder with your text editor of choice and change the desired values
  - the default keybinds to save frames are a and b (if `use_custom_webcam_keys` is set to `false`)
  - to change this behavior set `use_custom_webcam_keys` to `true` and specify your custom webcam keybinds in `custom_webcam_keys`
  - you will probably have to change `webcam_ports` to whichever ports your webcams use. you can find out by running the webcam_test.py script and copying the possible sources over
- creating an obs slideshow with this
  - before you create the slideshow make sure there are already images in the data folder (e.g. by taking them with the main script or manually adding image0.png to imageX.png)
  - in obs create an "Image Slide Show" source and configure as desired
  - in the "Image Files" field add the data directory
  - now whenever the main script updates the images in the data folder they show up in your slide show

## contributors

- [cytobi](https://github.com/cytobi)

## license

[MIT](https://choosealicense.com/licenses/mit/)
