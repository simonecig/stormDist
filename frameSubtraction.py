# Program that captures a video from the camera and shows as non black pixels
# only those that have changed with respect to the previous frame.

import cv2
import numpy as np
import matplotlib.pyplot as plt

# Min change in pixel value (from #000000)
TRESHOLD_VALUE = 95

# ---------- PREPARING HISTOGRAM ----------
# Define number of bins
bins = 20

# Plot configurations
fig, ax = plt.subplots()
ax.set_title('Histogram')
ax.set_xlabel('Bin')
ax.set_ylabel('Frequency')

# Initialize plot line object
lineGray, = ax.plot(np.arange(bins), np.zeros((bins, 1)),
                    c='k', lw=3, label='Intensity')

# Set axis limits
ax.set_xlim(0, bins)
ax.set_ylim(0, 1)

# Show the plot legend
ax.legend()

# Turn on interactive plotting and show plot
plt.ion()
plt.show()

# ---------- Video capture ----------
cap = cv2.VideoCapture(0)

# Check the camera
if not cap.isOpened():
    print("Cannot open camera")
    exit()

old_gray = None     # old frame
new_gray = None  # current frame - old frame. This is what will be shown
firstFrame = True  # if true there is no old frame ---> do nothing.
while True:
    ret, frame = cap.read()

    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame.")
        break

    # get black and white frame from camera
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # if it's the first frame do nothing as there is no previous frame
    if firstFrame is True:
        new_gray = gray
        firstFrame = False
    else:
        # get absolute difference between current frame and previous frame.
        # Save result in "new_gray"
        cv2.absdiff(gray, old_gray, new_gray)
        ret, new_gray = cv2.threshold(new_gray,
                                      TRESHOLD_VALUE, 150, cv2.THRESH_BINARY)

    # shows "new_gray"
    cv2.imshow('frame', new_gray)

    # saves current frame as "old_gray"
    old_gray = gray

    # Normalize histograms based on number of pixels per frame
    numPixels = np.prod(frame.shape[:2])
    histogram = cv2.calcHist([new_gray], [0], None,
                             [bins], [0, 255]) / numPixels
    lineGray.set_ydata(histogram)
    fig.canvas.draw()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
