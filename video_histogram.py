import numpy as np
import matplotlib.pyplot as plt
import cv2

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Define number of bins 
bins = 17

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