import cv2
import numpy as np

# Step 1: Read the image and convert it to grayscale
add_path = "hacky_test_aleksis/"
input_image = add_path + 'input_image_3.png'
output_image = add_path + 'output_image.png'
img = cv2.imread(input_image)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Step 2: Apply Gaussian blur to the grayscale image
kernel_size = 5
blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 1)

# Step 3: Perform edge detection using the Canny method
low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
cv2.imshow("edges", edges)
# Step 4: Detect lines using the HoughLinesP method
rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 200  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 20  # minimum number of pixels making up a line
max_line_gap = 20  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on

lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)

# Step 5: Draw the detected lines on a blank image
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 2)

# Step 6: Subtract the lines from the original image
inverted_line_image = cv2.bitwise_not(line_image)
lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
inverted_img = cv2.bitwise_not(img)

cv2.imshow("invert", inverted_line_image)
cv2.imshow("inverted_img", inverted_img)

inverted_img = cv2.cvtColor(inverted_img, cv2.COLOR_BGRA2BGR)

print(inverted_line_image.shape)
print(inverted_img.shape)
test = cv2.bitwise_and(inverted_img, inverted_line_image)
inverted_test = cv2.bitwise_not(test)
cv2.imshow('test', inverted_test)
cv2.imshow("uninverted", cv2.bitwise_not(inverted_img))
# Save the result image
cv2.imwrite(output_image, inverted_test)


cv2.waitKey(0)
cv2.destroyAllWindows()