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
blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

# Step 3: Perform erosion on the blurred image
erosion_kernel = np.ones((5, 5), np.uint8)
eroded_image = cv2.erode(blur_gray, erosion_kernel, iterations=1)


# Step 4: Perform dilation on the eroded image
dilation_kernel = np.ones((5, 5), np.uint8)
dilated_image = cv2.dilate(eroded_image, dilation_kernel, iterations=1)

# Step 5: Display the results
cv2.imshow("Original Image", img)
cv2.imshow("Grayscale Image", gray)
cv2.imshow("Blurred Image", blur_gray)
cv2.imshow("Eroded Image", eroded_image)
cv2.imshow("Dilated Image", dilated_image)

# Save the result image
cv2.imwrite(output_image, dilated_image)

cv2.waitKey(0)
cv2.destroyAllWindows()