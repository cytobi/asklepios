import cv2

cv2.namedWindow("preview")

possible_sources = []
test_amount = 5  # test this many sources
try:
    test_amount = int(
        input("How many sources to test? (default: " + str(test_amount) + "): ")
    )
except:
    print("using default amount of sources to test: " + str(test_amount))

# test a few possible video sources
print("testing possible sources")
for i in range(test_amount):
    vc = cv2.VideoCapture(i)
    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
        if rval:
            possible_sources.append(i)
            print("Source found: " + str(i))
    else:
        rval = False

print("possible sources: " + str(possible_sources))

if len(possible_sources) == 0:
    print("no sources found")
    exit()

# open the first source found
try:
    src_to_use = int(input("Which source should be used?: "))
except:
    print("using default source: " + str(possible_sources[0]))
    src_to_use = possible_sources[0]

vc = cv2.VideoCapture(src_to_use)
if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
    print("error opening source")

print(
    "press ESC to exit (while tabbed into the video window) or press Ctrl+C in the terminal for a hard stop"
)

# display the video
while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")
