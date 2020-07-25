import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2

# Using an argument parser for color, bins, and width of the frame
parser = argparse.ArgumentParser()

parser.add_argument('-c', '--color', type=str, default='gray')
parser.add_argument('-b', '--bins', type=int, default=16)
parser.add_argument('-w', '--width', type=int, default=0)

args = vars(parser.parse_args())

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Define color, bins and width variables
color = args['color']
bins = args['bins']
resizeWidth = args['width']

# Plot configurations
fig, ax = plt.subplots()
ax.set_title('Histogram')
ax.set_xlabel('Bin')
ax.set_ylabel('Frequency')

# Initialize plot line object
lineGray, = ax.plot(np.arange(bins), np.zeros((bins,1)), c='k', lw=3, label='Intensity')

# Set axis limits
ax.set_xlim(0, bins-1)
ax.set_ylim(0, 1)

# Show the plot legend
ax.legend()

# Turn on interactive plotting and show plot
plt.ion()
plt.show()

# Check the camera
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()

    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame.")
        break

    # Resize frame to width if wanted
    if resizeWidth > 0:
        (height, width) = frame.shape[:2]
        resizeHeight = int(float(resizeWidth / width) * height)
        frame = cv2.resize(frame, (resizeWidth, resizeHeight),
            interpolation=cv2.INTER_AREA)

    # Normalize histograms based on number of pixels per frame
    numPixels = np.prod(frame.shape[:2])
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    histogram = cv2.calcHist([gray], [0], None, [bins], [0, 255]) / numPixels
    lineGray.set_ydata(histogram)
    fig.canvas.draw()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()