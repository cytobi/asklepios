# asklepios

a tool to grab frames from a webcam and put them into an obs slideshow

developed for windows with python 3.11.3

## detailed usage guide

- download & install [python](https://www.python.org/downloads/): tick add to PATH, then click install now
- open terminal (win+r, then type cmd and hit enter)
- install numpy: `pip install numpy`
- install opencv: `pip install opencv-python`
- install keyboard: `pip install keyboard`
- navigate to install location: `cd <path to install location>`
- clone this repository: `git clone https://github.com/cytobi/asklepios.git`
- navigate into repository folder: `cd asklepios`
- run desired scripts via: `python scripts/<scriptname.py>`
  - test which ports your webcams use: `python scripts/webcam_test.py`
  - run the main script: `python scripts/main.py`
- if you wish to change some config (e.g. the ports your webcams use, the countdown time, etc) open the config.json file in the config folder with your editor of choice and change the desired values

## contributors
- [cytobi](https://github.com/cytobi)

## license

[MIT](https://choosealicense.com/licenses/mit/)
